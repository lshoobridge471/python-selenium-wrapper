# Python Selenium Browser with Random Agents
## selenium-browser-random-agent

Wrapper of [Selenium With python](https://selenium-python.readthedocs.io/).

Install:
```sh
pip install selenium-browser-random-agent
```
Create ```config.ini``` file with content:
```ini
[BROWSER]
# Chrome data folder (cookies)
data_dir=chrome-data
# Window size (in this case, mobile)
window_size=360,640
# Sleep on load pages.
time_sleep=5
[AGENTS]
# Custom agent
custom_agent=Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36
# Limit of random agents
limit=100
# Random agents enabled
random=False
[REMOTE]
# Enabled remote browser
enabled=False
# Remote browser config
protocol=http
host=localhost
port=4444
```
Python parse ```config.ini``` file:
```python
from configparser import ConfigParser
import json
# Init config parser
config = ConfigParser()
# Read configuration file
config.read('selenium.ini')
# Get the default section
browser = config['BROWSER']
# Get the default section
agents = config['AGENTS']
# Get the remote section
remote = config['REMOTE']

# Settings object
_SELENIUM_SETTINGS = {
    'browser': {
        'data_dir': browser.get('data_dir', None),
        'window_size': browser.get('window_size', '1420,1080'),
        'time_sleep': browser.getint('time_sleep', 5),
    },
    'agents': {
        'custom': browser.get('custom', None),
        'limit': browser.getint('limit', 100),
        'random': browser.getboolean('random', False),
    },
    'remote': {
        'enabled': json.loads(remote.get('enabled', 'False').lower()),
        'protocol': remote.get('protocol', 'http'),
        'host': remote.get('host', 'localhost'),
        'port': int(remote.get('port', 4444)),
    },
}
```
Python implementation:
```python
# Import Selenium Browser
from selenium_browser_random_agent.browser import Browser as SeleniumWrapper
# Instance the SeleniumBrowser
selenium_wrapper = SeleniumWrapper(**_SELENIUM_SETTINGS)
```
Navigation example:
```python
# Native methods of Selenium
selenium_wrapper.browser.get('https://www.google.com.ar/')
```

Class Methods:
```python
# Close browser
selenium_wrapper.close()
# Set custom agent
selenium_wrapper.set_agent(agent)
# Set random agent
selenium_wrapper.set_random_agent()
# Get current agent
selenium_wrapper.get_agent()
# Sleep time
selenium_wrapper.sleep(time=None)
# Scroll to bottom
selenium_wrapper.scroll_to_bottom(times=5, sleep_time=1)
```