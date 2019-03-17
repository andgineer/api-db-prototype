from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class AppMixin:
    pass


class WebDriverAugmented(RemoteWebDriver, AppMixin):
    """
    Web driver, augmented with application specific logic.
    """
    pass
