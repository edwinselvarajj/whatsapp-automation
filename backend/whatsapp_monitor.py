import threading
import asyncio
import requests
from playwright.async_api import async_playwright
import os
from backend.models import PerformanceMarketingGroupMessaages
from asgiref.sync import sync_to_async
import time

async def whatsapp_monitor():
    async with async_playwright() as playwright:
        # Start a second browser in persistent context for monitoring
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir=os.path.join(os.getcwd(), "whatsapp_monitor_data"),  # Separate data directory
            headless=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        )
        page = await browser.new_page()

        
        await page.goto("https://web.whatsapp.com/")
        print("Playwright monitor browser started and running.")
        
        time.sleep(10)
        h1_element = await page.query_selector("xpath=//h1")

        is_logged_in = False

        if h1_element:
            try:
                h1_element = await h1_element.inner_text()
                if h1_element == 'Chats':
                    print('already logged in')
                    await page.screenshot(path="whatsapp_screenshot_2.png")
                    is_logged_in = True
            except Exception:
                pass
        
        if not is_logged_in:
                print('not logged in')
                qr_code_canvas = 'xpath=//canvas'
                await page.wait_for_selector(qr_code_canvas, timeout=300000)
                
                print('qr found')
                
                time.sleep(6)
                # Take a screenshot after the page is fully loaded
                await page.screenshot(path="whatsapp_screenshot_2.png")
                print("Playwright monitor session started and running and took ss2.")

                time.sleep(120)

        # time.sleep(6)
        # # time.sleep(30)
        # # # Take a screenshot after the page is fully loaded
        # # await page.screenshot(path="whatsapp_screenshot_1.png")
        # # print("Screenshot taken and saved as 'whatsapp_screenshot_1.png'")

        # # time.sleep(120)
        # await page.screenshot(path="whatsapp_screenshot_1.png")
        # print("Screenshot taken and saved as 'whatsapp_screenshot_1.png again'")

        # time.sleep(120)


        # Step 1: Wait for the "New Chat" button to be visible after the page reload
        new_chat_button_selector = 'xpath=/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        await page.wait_for_selector(new_chat_button_selector, timeout=10000)
        if await page.is_visible(new_chat_button_selector):
            await page.click(new_chat_button_selector)
            print("Clicked New Chat button")
        else:
            raise Exception("New Chat button not visible")

        # Step 2: Search for the performance marketing in the search field
        search_box_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p"
        await page.wait_for_selector(search_box_selector, timeout=10000)
        if await page.is_visible(search_box_selector):
            await page.fill(search_box_selector, "")  # Clear existing search
            await page.fill(search_box_selector, 'performance marketing')  # Enter the search text
            print(f"Filled search text: {'performance marketing'}")
        else:
            raise Exception("Search box not visible")

        # Step 4: Click the first contact that appears
        first_contact_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]"
        await page.wait_for_selector(first_contact_selector, timeout=10000)
        if await page.is_visible(first_contact_selector):
            await page.click(first_contact_selector)
            print(f"Clicked first contact: {'performance marketing'}")
        else:
            raise Exception("First contact not visible")

        # Function to check for unread messages
        async def check_for_unread_messages():
            try:
                # XPath to the last message and its timestamp
                message_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span"
                timestamp_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/span"

                # Retrieve the last message and timestamp
                message_element = await page.query_selector(f"xpath={message_xpath}")
                timestamp_element = await page.query_selector(f"xpath={timestamp_xpath}")

                if message_element and timestamp_element:
                    message_text = await message_element.inner_text()
                    timestamp_text = await timestamp_element.inner_text()

                    # Check if this message and timestamp are already stored in the database
                    message_exists = await sync_to_async(PerformanceMarketingGroupMessaages.objects.filter(message=message_text, timestamp=timestamp_text).exists)()

                    if not message_exists:
                        # Store the new message and timestamp
                        await sync_to_async(PerformanceMarketingGroupMessaages.objects.create)(message=message_text, timestamp=timestamp_text)
                        print(f"Stored new message: {message_text} at {timestamp_text}")

                        # Make GET request to the API with the message received
                        url = f"https://marketingapi.mim-essay.com/api/marketingchatapp/process-user-message?command={message_text}"
                        response = requests.get(url)

                        # Check if the request was successful
                        if response.status_code == 200:
                            response_data = response.json()  # Parse the response JSON
                            last_message = response_data.get('last_message')  # Get the 'last_message' from the response

                            # Send the message
                            # Wait for the input box to be available
                            input_box_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"
                            await page.wait_for_selector(input_box_selector, timeout=10000)  # Wait for the input box
                            
                            # Fill in the message
                            await page.fill(input_box_selector, last_message)
                            
                            # Wait for the send button to appear and then click it
                            send_button_selector = "xpath=/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"
                            await page.wait_for_selector(send_button_selector, timeout=10000)  # Wait for the send button
                            
                            # Click the send button
                            await page.click(send_button_selector)
                            
                            print(f"Sent last message: {last_message}")
                        else:
                            print(f"Error: Failed to get response from API. Status code: {response.status_code}")
                    else:
                        # print(f"Message already exists: {message_text} at {timestamp_text}")
                        None
                else:
                    print("Message or timestamp not found.")
            except Exception as e:
                print(f"Error fetching unread messages: {e}")

        # Main loop for continuous monitoring
        while True:
            await check_for_unread_messages()  # Await the async function

            # Sleep for 1 second between checks
            await asyncio.sleep(1)


# Running the monitor asynchronously
async def run_monitor():
    await whatsapp_monitor()


# Start the Playwright monitor thread
monitor_thread = threading.Thread(target=lambda: asyncio.run(run_monitor()))
monitor_thread.daemon = True  # This ensures the thread stops when the main program exits
monitor_thread.start()
