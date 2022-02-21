# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Random user agent
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from webdriver_manager.chrome import ChromeDriverManager

# Another imports
from time import sleep
import json

class Browser(object):

    def __init__(self, **kwargs):
        """
            Init the Selenium Scrapper object.
        """
        # Get the settings
        remote_settings = kwargs.get('remote')
        browser_settings = kwargs.get('browser')
        agent_settings = kwargs.get('agents')
        # Set remote variables
        is_remote = bool(remote_settings.get('enabled', False))
        remote_protocol = remote_settings.get('protocol', 'http')
        remote_host = remote_settings.get('host', 'localhost')
        remote_port = int(remote_settings.get('port', 4444))
        # Set variables from settings values
        browser_window_size = browser_settings.get('window_size')
        browser_data_dir = browser_settings.get('data_dir')
        # Defines time sleep
        self.time_sleep = int(browser_settings.get('time_sleep'))

        agent_custom = agent_settings.get('custom')
        agents_limit = int(agent_settings.get('limit'))
        agents_random = bool(agent_settings.get('random'))
        # Init User agent rotator
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        
        self.user_agent_rotator = UserAgent(software_names=software_names,
                                        operating_systems=operating_systems,
                                        limit=agents_limit)
        # Init Chrome options
        browser_options = ChromeOptions()
        browser_options.add_argument('--headless')
        browser_options.add_argument('--no-sandbox')
        browser_options.add_argument('--disable-dev-shm-usage')
        browser_options.add_argument('--ignore-certificate-errors')
        #browser_options.add_argument('--disable-infobars')
        #browser_options.add_argument('--disable-extensions')
        #browser_options.add_argument("--disable-setuid-sandbox")
        #browser_options.add_argument('--disable-gpu')
        #browser_options.add_argument('--disable-notifications')
        browser_options.add_argument(f'--window-size={browser_window_size}')
        # Prevent detect automation
        #browser_options.add_argument('--disable-blink-features=AutomationControlled')
        #browser_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #browser_options.add_experimental_option('useAutomationExtension', False)

        if browser_data_dir:
            # Browser data-dir
            browser_options.add_argument(f'--user-data-dir={browser_data_dir}')

        if agent_custom:
            # Set custom user agent
            browser_options.add_argument(f'--user-agent={agent_custom}')
        try:
            # If not a remote driver
            if not is_remote:
                # Init the browser
                self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)
                # Assert browser instance.
                assert self.browser._is_remote == False
            else:
                # Init the remote driver.
                self.browser = webdriver.Remote(
                    command_executor = f'{remote_protocol}://{remote_host}:{remote_port}/wd/hub',
                    desired_capabilities = DesiredCapabilities.CHROME,
                )
                # If specified custom agent
                if agent_custom:
                    # Set custom agent
                    self.set_agent(agent_custom)
                # Assert browser instance.
                assert self.browser._is_remote == True
            # Remove webdriver get function.
            self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # If apply random user agents
            if agents_random and not agent_custom:
                self.set_random_agent()
        except Exception as error:
            raise Exception(f'Error on browser open: {error}')

    def close(self):
        """
            Close browser
        """
        return self.browser.close()

    def set_agent(self, agent):
        """
            Set user agent.
            Params:
                - Agent: user agent
        """
        # Override browser user agent
        if not self.browser._is_remote:
            self.browser.execute_cdp_cmd('Network.setUserAgentOverride', { 'userAgent': agent })
        else:
            value = self.send_remote_browser_command('Network.setUserAgentOverride', { 'userAgent': agent })
        # Returns browser agent.
        return self.get_agent()

    def set_random_agent(self):
        """
            Set random user agent.
        """
        # Override browser user agent
        agent = self.user_agent_rotator.get_random_user_agent()
        if not self.browser._is_remote:
            self.browser.execute_cdp_cmd('Network.setUserAgentOverride', { 'userAgent': agent })
        else:
            self.send_remote_browser_command('Network.setUserAgentOverride', { 'userAgent': agent })
        # Returns browser agent.
        return self.get_agent()

    def get_agent(self):
        """
            Get navigator user agent.
        """
        return self.browser.execute_script("return navigator.userAgent;")

    def sleep(self, time=None):
        sleep(time or self.time_sleep)

    def scroll_to_bottom(self, times, sleep_time=None):
        """
            Scroll to bottom of page.
        """
        # Scroll to bottom
        for i in range(times):
            ActionChains(self.browser).send_keys(Keys.END).perform()
            sleep(sleep_time or self.time_sleep)

    def send_remote_browser_command(self, cmd, params={}):
        """
            Workaround for remote webdriver.
            Replace execute_cdp_cmd command.
            Params:
                - cmd: command to execute
                - params: params.
        """
        # Ge resource URL
        resource = f"/session/{self.browser.session_id}/chromium/send_command_and_get_result"
        # Parse URL
        url = self.browser.command_executor._url + resource
        # Body to send POST request.
        body = json.dumps({'cmd': cmd, 'params': params})
        # Send POST request.
        response = self.browser.command_executor._request('POST', url, body)
        # If get status key (error)
        if response.get('status', False):
            # Raise exception with error.
            raise Exception('Error: {error}'.format(error=response.get('value')))
        # Defaults returns value
        return response.get('value')
