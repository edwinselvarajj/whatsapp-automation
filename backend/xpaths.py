def get_qr_code_xpath():
    return '//canvas'

def get_logged_in_title():
    return '//h1'

def new_chat_button():
    return '/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'

def search_for_chat_field():
    return '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p'

def first_contact_item_post_search():
    return '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]'

def title_of_chat():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div[1]/div/span'

def self_message_content():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'

def self_message_timestamp():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/span'

def others_message_content():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/span[1]/span'

def others_message_timestamp():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div[last()]/div/div/div[1]/div[2]/div[1]/div/div[3]/div/span'

def chat_input_box():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'

def send_message_button():
    return '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'