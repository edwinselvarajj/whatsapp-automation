import threading
from playwright.sync_api import sync_playwright
import os
import time
from queue import Queue

# Create a global thread-safe task queue
task_queue = Queue()
result_queue = Queue()  # Queue to send results back


def playwright_worker():
    with sync_playwright() as playwright:
        # Start browser in persistent context
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir=os.path.join(os.getcwd(), "whatsapp_data"),
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com/")
        print("Playwright browser started and running in a separate thread.")

        time.sleep(15)
        # Take a screenshot after the page is fully loaded
        page.screenshot(path="whatsapp_screenshot_2.png")
        print("Playwright monitor session started and running and took ss2.")

        time.sleep(120)

        # def check_for_new_messages():
        #     try:
        #         # Selector for unread messages (modify based on WhatsApp's DOM structure)
        #         unread_message_selector = "xpath=//span[contains(@aria-label, 'unread message')]"
        #         new_messages = page.query_selector_all(unread_message_selector)
                
        #         if new_messages:
        #             for message in new_messages:
        #                 # Get the contact name and message content
        #                 contact_name = message.evaluate('el => el.closest("[data-testid=cell-frame-title]").innerText')
        #                 last_message = message.evaluate('el => el.closest("[data-testid=last-msg-status]").innerText')
                        
        #                 # Print the contact name and message
        #                 print(f"New message from {contact_name}: {last_message}")

        #     except Exception as e:
        #         print(f"Error checking for new messages: {e}")
        
        while True:
            task = task_queue.get()  # Wait for tasks to be added to the queue

            # check_for_new_messages()
            
            if task['command'] == "check_h1":  # Check the 'Chats' header task
                h1_element = page.query_selector("xpath=//h1")
                if h1_element:
                    result_queue.put(h1_element.inner_text())  # Send result back
                else:
                    result_queue.put("not found")
            
            elif task['command'] == "get_chats":  # Example task to get chat titles
                chats = page.query_selector_all("xpath=//span[contains(@class, 'chat-title')]")
                chat_titles = [chat.inner_text() for chat in chats]
                result_queue.put(chat_titles)

            elif task['command'] == "send_message":  # Task to search for a contact and click the first one
                contact = task['contact']
                message = task['message']
                
                try:
                    # Step 1: Refresh the page to reset the chat view
                    page.reload()
                    print("Page reloaded")

                    # Step 2: Wait for the "New Chat" button to be visible after the page reload
                    new_chat_button_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span"
                    page.wait_for_selector(new_chat_button_selector, timeout=10000)
                    if page.is_visible(new_chat_button_selector):
                        page.click(new_chat_button_selector)
                        print("Clicked New Chat button")
                    else:
                        raise Exception("New Chat button not visible")

                    # Step 3: Search for the contact in the search field
                    search_box_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p"
                    page.wait_for_selector(search_box_selector, timeout=10000)
                    if page.is_visible(search_box_selector):
                        page.fill(search_box_selector, "")  # Clear existing search
                        page.fill(search_box_selector, contact)  # Enter the search text
                        print(f"Filled search text: {contact}")
                    else:
                        raise Exception("Search box not visible")

                    # Step 4: Click the first contact that appears
                    first_contact_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]"
                    page.wait_for_selector(first_contact_selector, timeout=10000)
                    if page.is_visible(first_contact_selector):
                        page.click(first_contact_selector)
                        print(f"Clicked first contact: {contact}")
                        result_queue.put(f"contact_selected: {contact}")
                    else:
                        raise Exception("First contact not visible")
                    
                    # Wait for the input box to be available
                    input_box_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"
                    page.wait_for_selector(input_box_selector, timeout=10000)  # Wait for up to 10 seconds for input box
                    
                    # Fill in the message
                    page.fill(input_box_selector, message)
                    
                    # Wait for the send button to appear and then click it
                    send_button_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"
                    page.wait_for_selector(send_button_selector, timeout=10000)  # Wait for up to 10 seconds for send button
                    
                    # Click the send button
                    page.click(send_button_selector)
                    
                    result_queue.put("message_sent")


                except Exception as e:
                    # Step 6: If no contact appears or there’s any error, return a 401 error
                    result_queue.put(f"error_searching_contact: {str(e)}")


            elif task['command'] == "stop":
                break  # Stop the thread safely

# Start Playwright worker thread
playwright_thread = threading.Thread(target=playwright_worker)
playwright_thread.daemon = True  # This ensures the thread stops when the main program exits
playwright_thread.start()
