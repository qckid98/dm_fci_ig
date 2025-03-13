import os
import sys
from threading import Thread
from time import sleep

from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from backend import SELECTORS, Session
from ui.components import MessageConfirmDialog, twofaPopup


class ProgressScreen(Screen):
    messages = []
    """
    Stores the messages to be sent. Each message is a dictionary representing the
    message type and the message content
    """

    accounts = []
    """
    Stores the target accounts to send the messages to
    """

    session = None
    """
    Stores the backend Session Data
    """

    password = None
    """
    Stores the password entered by the user. This variable is erased when this screen is destroyed
    """

    def __init__(self, messages, accounts, **kw):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            # Running as a bundled executable (PyInstaller)
            kv_file_path = os.path.join(sys._MEIPASS, "ui/progressscreen/progressscreen.kv")
        else:
            # Inside a normal Python environment
            kv_file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "progressscreen.kv")
            )
        # Load the .kv file
        Builder.load_file(kv_file_path)
        super().__init__(**kw)
        self.messages = messages
        self.accounts = accounts
        self.session = Session()
        self.create_datatable()
        # reverse the messages list
        self.messages.reverse()

    def on_enter(self):
        """
        Starts the message sending process
        """
        self.confirm_start()

    def create_datatable(self):
        """
        Adds the MDTable to the Screen
        """
        table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            column_data=[
                ("S.No", dp(30)),
                ("Status", dp(30)),
                ("Account Name", dp(50)),
                ("Account Source", dp(40)),
            ],
            check=True,
            rows_num=10,
        )
        self.table = table
        self.table.bind(on_check_press=self.edit_selection)
        self.ids.table_container.add_widget(table)
        self.set_table_data()

    def set_table_data(self):
        """
        Sets the initial data of the MDTable
        Adds a red clock icon to the status column
        """
        temp = []
        for account in self.accounts:
            temp.append(
                [
                    account[0],
                    ("clock-outline", [0.8, 0.3, 0.3, 1], "Pending"),
                    account[1],
                    account[2],
                ]
            )
        self.table.row_data = temp

    def edit_selection(self, instance_table, current_row):
        """
        Enables the remove button when a row is selected
        """
        if (len(self.table.get_row_checks())) > 0:
            self.ids.Remove.disabled = False

    def confirm_remove(self):
        """
        Confirms the removal of the selected accounts
        """
        self.confirm_remove_menu = MDDialog()
        ok_button = MDFlatButton(text="Remove", on_release=self.remove_from_queue)
        cancel_button = MDFlatButton(
            text="Cancel", on_release=self.confirm_remove_menu.dismiss
        )
        self.confirm_remove_menu = MDDialog(
            title="Dequeue Accounts",
            text="Are you sure you want to remove the selected accounts from the queue? NOTE: Only the accounts that are not currently being processed will be removed",
            buttons=[ok_button, cancel_button],
        )

        self.confirm_remove_menu.open()

    def remove_from_queue(self, *args):
        """
        Removes the accounts from queue. Only removes the accounts that are not currently being processed or the accounts that are completed
        """
        self.confirm_remove_menu.dismiss()
        for row in self.table.get_row_checks():
            self.table.remove_row(self.table.row_data[int(row[0]) - 1])

    def confirm_stop(self):
        """
        Confirms the stopping of the message sending process
        """
        self.confirm_stop_menu = MDDialog()
        ok_button = MDFlatButton(text="Stop", on_release=self.stop_messages)
        cancel_button = MDFlatButton(
            text="Cancel", on_release=self.confirm_stop_menu.dismiss
        )
        self.confirm_stop_menu = MDDialog(
            title="Stop Sending Messages",
            text="Are you sure you want to stop sending messages? NOTE: The messages that are currently being sent will be completed",
            buttons=[ok_button, cancel_button],
        )
        self.confirm_stop_menu.buttons = [ok_button, cancel_button]
        self.confirm_stop_menu.open()

    def stop_messages(self, *args):
        """
        Stops the message sending process
        """
        self.confirm_stop_menu.dismiss()
        self.session.driver.quit()

    def set_account_to_processing(self, count):
        """
        Sets the status of the account to processing. Sets the icon to an orange icon
        """
        self.table.update_row(
            self.table.row_data[count],
            [
                count + 1,
                (
                    "alert-circle",
                    [0.8, 0.5, 0.3, 1],
                    "Messaging",
                ),
                self.table.row_data[count][2],
                self.table.row_data[count][3],
            ],
        )

    def set_account_to_completed(self, count):
        """
        Sets the status of the account to completed. Sets the icon to a green icon
        """
        self.table.update_row(
            self.table.row_data[count],
            [
                count + 1,
                ("check-circle", [0.3, 0.8, 0.3, 1], "Completed"),
                self.table.row_data[count][2],
                self.table.row_data[count][3],
            ],
        )
    
    def set_account_to_invalid(self, count):
        """
        Sets the status of the account to invalid. Sets the icon to a red icon.
        """
        self.table.update_row(
            self.table.row_data[count],
            [
                count + 1,
                ("close-circle", [0.8, 0.3, 0.3, 1], "Invalid"),
                self.table.row_data[count][2],
                self.table.row_data[count][3],
            ],
        )

    def confirm_start(self):
        """
        Shows a confirm start menu along with request for the password again
        """
        self.confirm_start_menu = MessageConfirmDialog(
            callback=self.start_messages, text="Send Messages"
        )
        self.confirm_start_menu.open()

    def start_messages(self, password):
        """
        Starts Sending Messages in new thread
        """
        self.confirm_start_menu.dismiss()
        self.password = password
        Thread(target=self._start_messages).start()

    def _start_messages(self):
        # start the selenium driver and start sending messages
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Required for headless mode
        chrome_options.add_argument("--window-size=1920,1080")  # Avoid element visibility issues
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Helps prevent detection
        chrome_options.add_argument("--no-sandbox")  # Good for running in containers
        chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents resource issues in Docker
        self.session.driver = webdriver.Chrome(options=chrome_options)
        self.session.driver.implicitly_wait(30)
        # go to instagram login
        self.session.driver.get("https://www.instagram.com/accounts/login/")
        # Enter the username
        self.find_element(SELECTORS["login_username_field"]).send_keys(
            self.session.username
        )
        # Enter the password
        self.find_element(SELECTORS["login_password_field"]).send_keys(self.password)
        # Press enter key to login
        self.find_element(SELECTORS["login_password_field"]).send_keys(Keys.ENTER)
        # Check if the save login info button is present
        sleep(8)
        # check if the password was entered correctly again
        if self.check_if_element_exists(SELECTORS["login_error"]):
            self.wrong_password()
            return
        if self.check_if_element_exists("//div[text()='Enter a 6-digit login code generated by an authentication app.']"):
            self.two_factor_check(self)
        else:
            self.notification_disable()
    
    @mainthread    
    def two_factor_check(self, *args):
        if self.check_if_element_exists("//div[text()='Enter a 6-digit login code generated by an authentication app.']"):
            popup = twofaPopup()
            popup.open()
            popup.ok_button.bind(on_release=lambda instance: self.process_two_factor_code(popup))
            
    def process_two_factor_code(self, popup, *args):
        code = popup.content_cls.ids.twofa.text.strip()

        if not code:
            toast("Please enter the 2FA code!")  # Show a message if the field is empty
            return  # Don't close the popup yet

        popup.dismiss()  # Close the popup
        
        Thread(target=self._process_two_factor_code, args=(code,)).start()
        
    def _process_two_factor_code(self, code):
        """
        Runs the actual 2FA verification on a separate thread.
        """
        self.find_element("//input[@name='verificationCode']").send_keys(code)
        self.find_element("//input[@name='verificationCode']").send_keys(Keys.ENTER)
        sleep(5)  # This sleep no longer freezes the UI
        self.notification_disable()
        
    def notification_disable(self, *args):
        if self.check_if_element_exists(SELECTORS["save_login_info"]):
            # Click the save login info button
            self.find_element(SELECTORS["save_login_info"]).click()
        # Wait for the page to load
        sleep(3)
        
        # Check to see if the turn on notifications button is present
        # navigate to the messages page
        self.session.driver.get("https://www.instagram.com/direct/inbox/")
        if self.check_if_element_exists(SELECTORS["dm_notification_disable"]):
            # Click the turn on notifications button
            self.find_element(SELECTORS["dm_notification_disable"]).click()
        # sleep for some time
        sleep(2)
        self.start_message_loop()

    def start_message_loop(self, *args):
        """
        Starts the message loop
        """
        count = 0
        for user in self.accounts:
            self.session.driver.get("https://www.instagram.com/"+user[1])
            sleep(5)
            if self.check_if_element_exists("//div[@role='button' and .//*[local-name()='svg' and @aria-label='Options']]"):
                pass
            else:
                self.set_account_to_invalid(count)
                count += 1
                continue
            status_account = self.check_if_element_exists("//div[text()='Message']")
            if status_account != True:
                self.find_element("//div[@role='button' and .//*[local-name()='svg' and @aria-label='Options']]").click()
                sleep(1)
                self.find_element("//button[text()='Send message']").click()
                sleep(5)
            elif status_account == True:
                self.find_element("//div[text()='Message']").click()
            self.set_account_to_processing(count)
            sleep(5)
            self.find_element(SELECTORS["dm_msg_field"]).click()
            sleep(1)
            for message in self.messages:
                # start typing the message
                self.simulate_human(message["content"])
                # send the message
                actions = webdriver.ActionChains(self.session.driver)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                sleep(5)
            # set the account to completed
            self.set_account_to_completed(count)
            count += 1
            sleep(15)
            # set the account to processing
            # self.set_account_to_processing(count)
            # # open the user chat
            # self.find_element(SELECTORS["new_dm_btn"]).click()
            # sleep(3)
            # # Find the user search field and enter the keys
            # self.find_element(SELECTORS["dm_type_username"]).send_keys(user[1])
            # xpath_current_account_name = self.find_element(SELECTORS["current_account_name"])
            # current_account_name = xpath_current_account_name.text
            # if current_account_name in user_already:
            # # # We press teh back key and enter the last key again to fix a bug on insta that causes the account names to not show up
            #     self.find_element(SELECTORS["dm_type_username"]).send_keys(Keys.BACKSPACE)
            #     sleep(2)
            #     self.find_element(SELECTORS["dm_type_username"]).send_keys(user[1][-1])
            #     sleep(5)
            # # find the user and click on it
            #     self.find_element(SELECTORS["dm_select_next_user"].format(user[1])).click()
            #     sleep(2)
            # else:
            # # # We press teh back key and enter the last key again to fix a bug on insta that causes the account names to not show up
            #     self.find_element(SELECTORS["dm_type_username"]).send_keys(Keys.BACKSPACE)
            #     sleep(2)
            #     self.find_element(SELECTORS["dm_type_username"]).send_keys(user[1][-1])
            #     sleep(5)
            # # find the user and click on it
            #     self.find_element(SELECTORS["dm_select_user"].format(user[1])).click()
            #     sleep(2)
            # # click the chat button
            # self.find_element(SELECTORS["dm_start_chat_btn"]).click()
            # # select the message field
            # self.find_element(SELECTORS["dm_msg_field"]).click()
            # sleep(1)
            # account_name = self.find_element(SELECTORS['account_name'])
            # user_already.append(account_name.text)
            # for message in self.messages:
            #     # start typing the message
            #     self.simulate_human(message["content"])
            #     # send the message
            #     actions = webdriver.ActionChains(self.session.driver)
            #     actions.send_keys(Keys.ENTER)
            #     actions.perform()
            #     sleep(5)
            # # set the account to completed
            # self.set_account_to_completed(count)
            # count += 1
            # sleep(15)
        self.session.driver.quit()

    def simulate_human(self, text):
        """
        Simulates human typing
        """
        for char in text:
            sleep(0.05)
            if char != "\n":
                actions = webdriver.ActionChains(self.session.driver)
                actions.send_keys(char)
                actions.perform()
            elif char == "\n":
                actions = webdriver.ActionChains(self.session.driver)
                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
                actions.perform()

    @mainthread
    def wrong_password(self):
        """
        Executed when the user enters the wrong password.
        Clears this screen and navigates back to the message screen
        """
        toast("Incorrect Password")
        self.manager.current = "messagescreen"
        self.manager.remove_widget(self)
        self.session.driver.quit()

    def find_element(self, XPATH):
        """
        Finds an element by XPATH
        """
        return self.session.driver.find_element(By.XPATH, XPATH)

    def find_element_css(self, CSS):
        """
        Finds an element by CSS Selector
        """
        return self.session.driver.find_element(By.CSS_SELECTOR, CSS)

    def check_if_element_exists(self, XPATH):
        """
        Checks if an element exists by XPATH
        """
        self.session.driver.implicitly_wait(3)
        try:
            self.find_element(XPATH)
            self.session.driver.implicitly_wait(10)
            return True
        except Exception:
            self.session.driver.implicitly_wait(10)
            return False
