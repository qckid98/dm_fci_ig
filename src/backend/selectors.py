"""
_summary_: This file contains all the selectors for the backend.
"""

SELECTORS = {
    "login_username_field": "//input[@name='username']",
    "login_password_field": "//input[@name='password']",
    "new_dm_btn": "//div[@role= 'button'][.//div//*//*[text()='New message']]",
    "dm_type_username": "//input[@placeholder='Search...']",
    "dm_select_user": '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div/div/div[3]/div/label/div/input',
    "dm_start_chat_btn": "//div/div[text()='Chat' and @role='button']",
    "dm_msg_field": "//div[@role='textbox' and @aria-label='Message']",
    "save_login_info": "//button[text()='Save info']",
    "account_name": "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/section/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div[2]/div/div/h2/span",
    "current_account_name": "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div[1]/div[1]/div/div/div[2]/div/div/div/span/span/span",
    "login_error": "//div[text()='Sorry, your password was incorrect. Please double-check your password.']",
    "dm_notification_disable": "//button[text()='Not Now']",
    "dm_select_next_user": "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div/label/div/input"
    
}
