import os
import unittest
from subprocess import Popen

import ckan.logic as logic
import pexpect
from ckan.config.environment import load_environment
from paste.deploy import appconfig
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class TestSelenium(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conf = appconfig('config:/etc/ckan/default/production.ini', relative_to='.')
        load_environment(conf.global_conf, conf.local_conf)
        env = os.environ.copy()
        env['DEBUG'] = 'True'
        env['OAUTHLIB_INSECURE_TRANSPORT'] = 'True'
        cls._process = Popen(['paster', 'serve', 'test.ini'], env=env)

    @classmethod
    def tearDownClass(cls):
        child = pexpect.spawn('paster', ['--plugin=ckan', 'dataset', 'purge', '01', '-c', '/etc/ckan/default/production.ini'])
        child.expect('01 purged')
        child = pexpect.spawn('paster', ['--plugin=ckan', 'dataset', 'purge', '02', '-c', '/etc/ckan/default/production.ini'])
        child.expect('02 purged')
        logic.get_action('organization_purge')({'ignore_auth': True}, {'id': 'testorg'})
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

    def tearDown(self):
        self.driver.quit()

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
            # Sysadmin probably exists already
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

        self.create_organization('testorg', 'test')
        self.create_dataset('01', 'description', '01',
                            'resource_name', 'resource_description', 'html')

        self.driver.get(self.base_url + 'dataset/01')
        actions = ActionChains(self.driver)
        twitter = self.driver.find_element_by_link_text('Twitter')
        actions.key_down(Keys.COMMAND).click(twitter).key_up(Keys.COMMAND).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        assert 'Share a link' in self.driver.title
        bla = self.driver.find_element_by_id('status')

        assert "Check out " in bla.text
        assert "01" in bla.text
        assert "description" in bla.text

    def test_resource_title_in_share_text_twitter(self):

        self.register()
        self.login('selenium_admin', 'selenium')

        self.create_organization('testorg', 'test')
        self.create_dataset('02', 'description', '02',
                            'resource_name', 'resource_description', 'html')

        self.driver.get(self.base_url + 'dataset/02')
        self.driver.find_element_by_xpath("//a[@title='resource_name']").click()
        twitter = self.driver.find_element_by_link_text('Twitter')
        actions = ActionChains(self.driver)
        actions.key_down(Keys.COMMAND).click(twitter).key_up(Keys.COMMAND).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        assert 'Share a link' in self.driver.title
        bla = self.driver.find_element_by_id('status')

        assert "Check out \"this great resource" in bla.text
        assert "resource_name" in bla.text


if __name__ == '__main__':
    unittest.main()
