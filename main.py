# This program will submit email addresses into the
# drawing for the 2022 HGTV Dream Home Sweepstakes
# (https://www.hgtv.com/sweepstakes/hgtv-dream-home)
# Pre reqs:
#   - You must have already done the initial entry for the email address to submit as this requires some manual information (Name, Cable Provider, Etc)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def enterSweeps(email):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get("https://www.hgtv.com/sweepstakes/hgtv-dream-home/sweepstakes")

    # Give the browser time to load
    time.sleep(6)

    # HGTV has the email element bundled in an iframe, so we have to switch to that frame
    browser.switch_to.frame(browser.find_element_by_id('ngxFrame207341'))

    emailField = browser.find_element_by_name('xReturningUserEmail')
    emailField.send_keys(email)
    time.sleep(1)
    emailField.submit()

    time.sleep(6)

    # Back out of the iframe where we enter the email

    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(2)

    enterButton = browser.find_element_by_xpath('/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
    enterButton.click()

    time.sleep(5)

    ## Food Network
    browser.get("https://www.foodnetwork.com/sponsored/sweepstakes/hgtv-dream-home-sweepstakes")

    # Give the browser time to load
    time.sleep(6)

    # HGTV has the email element bundled in an iframe, so we have to switch to that frame
    browser.switch_to.frame(browser.find_element_by_id('ngxFrame207345'))

    emailField = browser.find_element_by_name('xReturningUserEmail')
    emailField.send_keys(email)
    time.sleep(1)
    emailField.submit()

    time.sleep(6)

    # Back out of the iframe where we enter the email

    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(2)

    enterButton = browser.find_element_by_xpath('/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
    enterButton.click()

    time.sleep(5)

    browser.quit()

# Check for emails to submit
emailFile = open('emails.txt')
emails = emailFile.readlines()
emailFile.close()

for e in emails:
    if (e != ""):
        print('Entering sweeps with: ' + e)
        enterSweeps(e)
