import pytest
import allure
from allure.constants import AttachmentType


@pytest.allure.issue('https://github.com/masterandrey/api-db-prototype/issues/1')
@pytest.allure.feature('End-to-end test suit')
@pytest.allure.story('Test selenium grid is alive')
@pytest.allure.testcase('hhttps://github.com/masterandrey/api-db-prototype/issues/2')
#@pytest.mark.create-objects
def test_selenium(browser):
    """
    Test that test infrastructure (selenium grid, allure reporter) is working
    """
    with allure.step('Test access to python.org'):
        browser.get("http://www.python.org")  # Use host.docker.internal to go to local host from selenium grid docker
        assert "Python" in browser.title
    with allure.step('Taking screenshot'):
        allure.attach('screenshot',
                      browser.get_screenshot_as_png(),
                      type=AttachmentType.PNG)