# -*- coding: utf-8 -*-
# Copyright (c) 2016 CoNWeT Lab., Universidad Politécnica de Madrid
# This file is part of CKAN Data Requests Extension.
# CKAN Data Requests Extension is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# CKAN Data Requests Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with CKAN Data Requests Extension.  If not, see <http://www.gnu.org/licenses/>.


import os
import unittest
from subprocess import Popen
import pexpect
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class TestSelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env = os.environ.copy()
        env['DEBUG'] = 'True'
        env['OAUTHLIB_INSECURE_TRANSPORT'] = 'True'
        cls._process = Popen(['paster', 'serve', 'test.ini'], env=env)

    @classmethod
    def tearDownClass(cls):
        cls._process.terminate()

    def setUp(self):
        if 'WEB_DRIVER_URL' in os.environ and 'CKAN_SERVER_URL' in os.environ:
            self.driver = webdriver.Remote(os.environ['WEB_DRIVER_URL'], webdriver.DesiredCapabilities.FIREFOX.copy())
            self.base_url = os.environ['CKAN_SERVER_URL']
        else:
            self.driver = webdriver.Chrome()
            self.base_url = 'http://127.0.0.1:5000/'
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1024, 768)

    def logout(self):
        self.driver.delete_all_cookies()
        self.driver.get(self.base_url)

    def register(cls):
        try:
            cls.sysadmin = 'selenium_admin'
            cls.sysadmin_pwd = 'selenium'
            child = pexpect.spawn('paster', ['--plugin=ckan', 'sysadmin', 'add', cls.sysadmin, '-c', '/etc/ckan/default/production.ini'])
            child.expect('Create new user: .+')
            child.sendline('y')
            child.expect('Password: ')
            child.sendline(cls.sysadmin_pwd)
            child.expect('Confirm password: ')
            child.sendline(cls.sysadmin_pwd)
            child.expect('Added .+ as sysadmin')
        except pexpect.EOF:
            # Sysadmin already exists
            pass
        cls.logout()

    def login(self, username, password):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Log in').click()
        driver.find_element_by_id('field-login').clear()
        driver.find_element_by_id('field-login').send_keys(username)
        driver.find_element_by_id('field-password').clear()
        driver.find_element_by_id('field-password').send_keys(password)
        driver.find_element_by_id('field-remember').click()
        driver.find_element_by_css_selector('button.btn.btn-primary').click()

    def create_organization(self, name, description):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Organizations').click()
        driver.find_element_by_link_text('Add Organization').click()
        driver.find_element_by_id('field-name').clear()
        driver.find_element_by_id('field-name').send_keys(name)
        driver.find_element_by_id('field-description').clear()
        driver.find_element_by_id('field-description').send_keys(description)
        driver.find_element_by_name('save').click()

    def create_dataset(self, name, description, resource_url, resource_name, resource_description, resource_format):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_link_text('Datasets').click()
        driver.find_element_by_link_text('Add Dataset').click()
        # FIRST PAGE: Dataset properties
        driver.find_element_by_id('field-title').clear()
        driver.find_element_by_id('field-title').send_keys(name)
        driver.find_element_by_id('field-notes').clear()
        driver.find_element_by_id('field-notes').send_keys(description)
        driver.find_element_by_name('save').click()
        # SECOND PAGE: Add Resources
        try:
            # The link button is only clicked if it's present
            driver.find_element_by_link_text('Link').click()
        except Exception:
            pass
        driver.find_element_by_id('field-image-url').clear()
        driver.find_element_by_id('field-image-url').send_keys(resource_url)
        driver.find_element_by_id('field-name').clear()
        driver.find_element_by_id('field-name').send_keys(resource_name)
        driver.find_element_by_id('field-description').clear()
        driver.find_element_by_id('field-description').send_keys(resource_description)
        driver.find_element_by_id('s2id_autogen1').clear()
        driver.find_element_by_id('s2id_autogen1').send_keys(resource_format + '\n')
        driver.find_element_by_css_selector('button.btn.btn-primary').click()

    def test_dataset_description_in_share_text_twitter(self):
        self.register()
        self.login('selenium_admin', 'selenium')

        self.create_dataset('this_dataset', 'description', 'this_dataset',
                            'resource_name', 'resource_description', 'html')

        self.driver.get(self.base_url + 'dataset/this_dataset')
        actions = ActionChains(self.driver)
        twitter = self.driver.find_element_by_link_text('Twitter')
        actions.key_down(Keys.COMMAND).click(twitter).key_up(Keys.COMMAND).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        assert 'Share a link' in self.driver.title
        bla = self.driver.find_element_by_id('status')

        assert "Check out " in bla.text
        assert "15" in bla.text
        assert "description" in bla.text


if __name__ == '__main__':
    unittest.main()