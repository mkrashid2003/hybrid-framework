import pytest
from selenium import webdriver

@pytest.fixture()
def setup(browser):
    driver=webdriver.Chrome()
    return driver
    #if browser=="chrome":
        #driver=webdriver.Chrome()
    #elif browser=="firefox":
       # driver=webdriver.Firefox()
   # else:
       # driver=webdriver.Edge()
    #return driver

#def pytest_addoption(parser):
   # parser.addoption("--browser", action="store", default="chrome", help="Type in browser name")

#@pytest.fixture()
#def browser(request):
#    return request.config.getoption("--browser")
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
   metadata.pop("JAVA_HOME",None)
   metadata.pop("plugins",None)
   metadata.pop("platforms",None)
   metadata.pop("Packages",None)
@pytest.hookimpl(optionalhook=True)
def pytest_sessionFinish(session,exitstatus):
     session.config._metadata["project Name"] = "Mercury Tours"



