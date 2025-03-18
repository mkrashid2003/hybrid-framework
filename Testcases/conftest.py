import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser name")


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture()
def setup(browser):
    if browser.lower() == "chrome":
        driver = webdriver.Chrome()
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Edge()

    yield driver
    driver.quit()


def pytest_configure(config):
    # Use config.metadata if available (pytest-html sets this attribute)
    if hasattr(config, "metadata"):
        config.metadata["project Name"] = "Mercury Tours"
    else:
        # Fallback if metadata isn't available
        config._metadata = {"project Name": "Mercury Tours"}


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    # Remove unwanted metadata keys
    metadata.pop("JAVA_HOME", None)
    metadata.pop("plugins", None)
    metadata.pop("platforms", None)
    metadata.pop("Packages", None)
