import os
import urllib
from datetime import datetime
import pytest
import allure
from allure.constants import AttachmentType
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
import settings
from webdriver_augmented import WebDriverAugmented


test_browsers = ['chrome']


class WebDriverCreator(object):
    """
    Create web driver.
    """
    _webdrv = None

    def get_web_driver(self):
        if self._webdrv is not None:
            return self._webdrv
        try:
            self._webdrv = WebDriverAugmented(
                command_executor=settings.config.webdriver_host,
                desired_capabilities={
                    'browserName': 'chrome'
                })
            self._webdrv.page_timer.start()
        except WebDriverException as e:
            print('\nFail to connect to selenium webdriver remote host: \n\n{}'.format(e))
        except urllib.error.URLError as e:
            print('\nFail to connect to selenium webdriver remote host.\nCheck it is running on {}: \n\n{}'.format(
                settings.config.webdriver_host, e))
        return self._webdrv


@pytest.fixture(scope='session', params=test_browsers, ids=lambda x: 'Браузер: {}'.format(x))
def browser(request):
    """
    Returns all browsers to test with
    """
    if request.config.getoption('--no-selenium'):
        return None
    webdrv = WebDriverCreator().get_web_driver()
    request.addfinalizer(lambda *args: webdrv.quit())
    #driver.implicitly_wait(Config().WEB_DRIVER_IMPLICITE_WAIT)
    webdrv.maximize_window()
    webdrv.get(settings.config.api_host)
    return webdrv


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    def local_screenshot_file_name():
        return os.path.join(settings.config.local_screenshot_folder,
                            datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f') + '.png')

    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'web_driver' in item.fixturenames:
                    web_driver = item.funcargs['web_driver']
                elif 'web_driver_factory'in item.fixturenames:
                    web_driver = item.funcargs['web_driver_factory'].last()
                else:
                    print('Fail to take screen-shot')
                    return
             # WebDriverFactory().get_web_driver()
            allure.attach('screenshot',
                          web_driver.get_screenshot_as_png(),
                          type=AttachmentType.PNG)
            web_driver.get_screenshot_as_file(local_screenshot_file_name())
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))
