# -*- coding: utf-8 -*-
import time
from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
        self.fail("could not find window")

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def test_login_with_persona(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Edith logs in with her email address
        ## Use qq.com for test email
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('649038269@qq.com')
        self.browser.find_element_by_tag_name('button').click()
        self.wait_for_element_with_id('authentication_password')
        self.browser.find_element_by_id(
            'authentication_password'
        ).send_keys('123456asdf')
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('649038269@qq.com', navbar.text)
