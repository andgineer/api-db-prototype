import pytest
import allure
from allure.constants import AttachmentType


@pytest.allure.issue('https://github.com/masterandrey/api-db-prototype/issues/1')
@pytest.allure.feature('End-to-end test suit')
@pytest.allure.story('Test selenium hub is life')
@pytest.allure.testcase('hhttps://github.com/masterandrey/api-db-prototype/issues/2')
@pytest.mark.agentticketsapi
def test_selenium(browser):
    """
    Test that test infrastructure (selenium hub, allur reporter) is working
    """
    with allure.step('Test access to python.org'):
        browser.get("http://www.python.org")
        assert "Python" in browser.title
    with allure.step('Taking screenshot'):
        allure.attach('screenshot',
                      browser.get_screenshot_as_png(),
                      type=AttachmentType.PNG)