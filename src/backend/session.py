from instaloader import Instaloader, Profile, TwoFactorAuthRequiredException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class Session:
    """
    Maintains data about the current web sessions
    """

    _instance = None

    logged_in: bool = False
    loader: Instaloader = None
    driver: webdriver.Chrome = None
    username: str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.loader = Instaloader()
        return cls._instance

    def login(self, username: str, password: str) -> Profile:
        """
        Login to Instagram using Instaloader
        """
        self.username = username
        self.loader.login(username, password)
        self.logged_in = True
        
    def two_factor_login(self, username: str, password: str, code: int):
        self.logged_in = False
        try:
            self.loader.login(username, password)
        except TwoFactorAuthRequiredException:
            self.loader.two_factor_login(code)
        self.logged_in = True

    def clear(self):
        """
        Clears the current session
        """
        self.logged_in = False
        self.loader = Instaloader()
        self.driver = None
        self.username = None
