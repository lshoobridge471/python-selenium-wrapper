from setuptools import setup

setup(
    name='selenium_wrapper',
    version='0.0.2',
    description='Selenium browser with random agents, with remote and local autoinstall chromedriver.',
    url='https://bitbucket.org/pergadev/python-selenium-wrapper/',
    author='Lucas Shoobridge',
    author_email='shoobridgelucas@gmail.com',
    license='MIT',
    packages=['selenium_wrapper'],
    zip_safe=False,
    install_requires=[
        'configparser==5.2.0',
        'random-user-agent==1.0.1',
        'selenium==4.1.0',
        'webdriver-manager==3.5.2'
    ],
)
