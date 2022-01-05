# This program will submit email addresses into the
# drawing for the 2022 HGTV Dream Home Sweepstakes
# (https://www.hgtv.com/sweepstakes/hgtv-dream-home)
# Pre reqs:
#   - You must have already done the initial entry for the email address to submit as this requires some manual information (Name, Cable Provider, Etc)
#   - Any emails must be in a file named "emails.txt" in the same directory. One email address per line

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

    # The email element is bundled in an iframe, so we have to switch to that frame
    browser.switch_to.frame(browser.find_element_by_id('ngxFrame207341'))

    emailField = browser.find_element_by_name('xReturningUserEmail')
    emailField.send_keys(email)
    time.sleep(2)
    emailField.submit()

    time.sleep(6)

    # Back out of the iframe where we enter the email

    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(2)

    # Submit to HGTV
    enterButton = browser.find_element_by_xpath('/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
    enterButton.click()

    time.sleep(3)

    # Check for success
    feedbackElem = browser.find_element_by_xpath('/html/body/section/div[3]/div[3]/div/div[2]/div[1]/div/div[3]/div[1]/section/p/b')
    feedbackText = feedbackElem.text.strip()
    print(feedbackText)

    if (feedbackText == "Thank You for Entering!"):
        print("Successfully entered on HGTV site")
    else:
        print("Error: Submission to HGTV site failed")

    time.sleep(1)
    
    ## Food Network
    browser.get("https://www.foodnetwork.com/sponsored/sweepstakes/hgtv-dream-home-sweepstakes")

    # Give the browser time to load
    time.sleep(6)

    # The email element is bundled in an iframe, so we have to switch to that frame
    browser.switch_to.frame(browser.find_element_by_id('ngxFrame207345'))

    emailField = browser.find_element_by_name('xReturningUserEmail')
    emailField.send_keys(email)
    time.sleep(2)
    emailField.submit()

    time.sleep(6)

    # Back out of the iframe where we enter the email

    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    time.sleep(2)

    enterButton = browser.find_element_by_xpath('/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
    enterButton.click()

    time.sleep(3)

    # Check for success
    feedbackElem = browser.find_element_by_xpath('/html/body/section/div[3]/div[3]/div/div[2]/div[1]/div/div[3]/div[1]/section/p/b')
    feedbackText = feedbackElem.text.strip()
    print(feedbackText)

    if (feedbackText == "Thank You for Entering!"):
        print("Successfully entered on FoodNetwork site")
    else:
        print("Error: Submission to FoodNetwork site failed")

    browser.quit()

# Check for emails to submit
emailFile = open('emails.txt')
emails = emailFile.readlines()
emailFile.close()

for e in emails:
    e = e.strip()
    if (e != ""):
        print('Entering sweeps with: ' + e)
        enterSweeps(e)
