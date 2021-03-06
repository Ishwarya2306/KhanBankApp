import time

import allure
from allure_commons.types import AttachmentType
from behave import *
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PageObjects.login import Login
from PageObjects.selectPassword import SelectPwd
from PageObjects.mongolianCustomerPassword import MongolianCustomerPassword
from Utilities.constants import Constants
from Utilities.customLogger import LogGen

myLogger = LogGen.logGen()

@given(u'I launch the Khan Bank application')
def step_impl(context):
    context.driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    myLogger.info("*****Driver Initialized*****")
    try:

        context.driver.get(Constants.BASE_URL)
        context.driver.maximize_window()
        context.driver.find_element_by_xpath("//button[@id='details-button']").click()
        DownLink = context.driver.find_element_by_xpath("//a[@id='proceed-link']")
        context.driver.execute_script("arguments[0].scrollIntoView();", DownLink)
        DownLink.click()
        #Add wait - Find an element in the application page
        if context.driver.title == Constants.HOMEPAGE_TITLE:
            assert True
            context.driver.save_screenshot(".\\Screenshots\\"+"LoginPage.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank LoginPage",attachment_type = AttachmentType.PNG)
            myLogger.info("*****Homepage title matches*****")
        else:
            assert False
            context.driver.save_screenshot(".\\Screenshots\\" + "LoginPage.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank LoginPage",
                          attachment_type=AttachmentType.PNG)
            myLogger.info("*****Homepage title does not match*****")
    except:
        #myLogger.exception("Error occured during execution: %s", e.message)
        myLogger.info("*****Unable to launch the application")

@when(u'I click on Forgot Password link')
def step_impl(context):
    global login_page
    login_page = Login(context.driver)
    global select_password_page
    select_password_page = SelectPwd(context.driver)

    try:
        login_page.clickOnForgotPassword()
        if select_password_page.title_selectPasswordType_className.text == Constants.SELECT_PASSWORD_TITLE:
            assert True
            context.driver.save_screenshot(".\\Screenshots\\" + "SelectPasswordPage.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank Select Password Page",
                      attachment_type=AttachmentType.PNG)
            myLogger.info("*****Select Password Type title matches*****")
        else:
            assert False
            context.driver.save_screenshot(".\\Screenshots\\" + "SelectPasswordPage.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank Select Password Page",
                      attachment_type=AttachmentType.PNG)
            myLogger.info("*****Select Password Type title does not match*****")
    except:
        # myLogger.exception("Error occured during execution: %s", e.message)
        myLogger.info("*****Unable to click on Forgot Password Link******")


@when(u'I select the login password to be reset')
def step_impl(context):
    global select_password_page
    select_password_page = SelectPwd(context.driver)
    select_password_page.selectLoginPassword()
    select_password_page.clickOnContinue()


@then(u'I should be displayed with the Forgot password page for Mongolian Customer')
def step_impl(context):
    global mongolian_customer_password_page
    mongolian_customer_password_page = MongolianCustomerPassword(context.driver)
    try:
        if context.driver.title == Constants.HOMEPAGE_TITLE:
            assert True
            context.driver.save_screenshot(".\\Screenshots\\" + "ForgotPWDPageMongolian.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank Forgot Password Page for Mongolian Customers",
                          attachment_type=AttachmentType.PNG)
            myLogger.info("*****Homepage title matches*****")
        else:
            context.driver.save_screenshot(".\\Screenshots\\" + "ForgotPWDPageMongolian.png")
            allure.attach(context.driver.get_screenshot_as_png(),
                          name="Khan Bank Forgot Password Page for Mongolian Customers",
                          attachment_type=AttachmentType.PNG)
            myLogger.info("*****Homepage title does not match*****")
    except:
        #myLogger.exception("Error occured during execution: %s", e.message)
        myLogger.info("*****Unable to verify the title*****")

@then(u'I click on Continue button without selecting a password')
def step_impl(context):
    global select_password_Page
    select_password_Page = SelectPwd(context.driver)
    select_password_Page.clickOnContinue()
    time.sleep(3)

@then(u'Warning message should be displayed')
def step_impl(context):
    try:
        warning_select_password_msg = context.driver.find_element_by_xpath("//div[@role='alert']").text
        if warning_select_password_msg == "???????? ?????????? ?????????? ?????????????? ????":
            assert True
            context.driver.save_screenshot(".\\Screenshots\\" + "SelectPWDTypeWarning.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank Select Password Type Warning",
                          attachment_type=AttachmentType.PNG)
            myLogger.info("Warning message - Select Password Type is displayed")
        else:
            assert False
            context.driver.save_screenshot(".\\Screenshots\\" + "NoSelectPWDTypeWarning.png")
            allure.attach(context.driver.get_screenshot_as_png(), name="Khan Bank Select Password Type Warning",
                          attachment_type=AttachmentType.PNG)
            myLogger.info("Warning message - Select Password Type is not displayed")
    except:
        context.driver.close()
        myLogger.info("Unable to test the negative test - Without selecting a password type ")


@then(u'I close the browser')
def step_impl(context):
    context.driver.close()
    myLogger.info("Browser is closed")

