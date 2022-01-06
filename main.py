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

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def navAndEnter(site, em):
    url = ""
    frameID = ""

    if (site == "HGTV"):
        url = "https://www.hgtv.com/sweepstakes/hgtv-dream-home/sweepstakes"
        frameID = "ngxFrame207341"
    elif (site == "FoodNetwork"):
        url = "https://www.foodnetwork.com/sponsored/sweepstakes/hgtv-dream-home-sweepstakes"
        frameID ="ngxFrame207345"
    else:
        print("Error: Unknown site...")
        quit()

    # Navigate to the URL
    browser.get(url)

    # Give the browser time to load
    time.sleep(5)

    # The email element is bundled in an iframe, so we have to switch to that frame
    browser.switch_to.frame(browser.find_element_by_id(frameID))

    # Submit the email address
    emailField = browser.find_element_by_name('xReturningUserEmail')
    emailField.send_keys(em)

    # The site appears to do some validation in the background so if you submit too
    # quickly, you will receive an error message instead of proceeding on the form
    time.sleep(2)
    emailField.submit()

    # Wait for the next screen / ads to load after submission
    time.sleep(3)

    # We need to go to the bottom of the outter page to be able to see the enter button
    html = browser.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(1)

    # Click the Enter Button
    enterButton = browser.find_element_by_xpath('/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
    enterButton.click()
    time.sleep(2)

    # Check for success
    feedbackElem = browser.find_element_by_xpath('/html/body/section/div[3]/div[3]/div/div[2]/div[1]/div/div[3]/div[1]/section/p/b')
    feedbackText = feedbackElem.text.strip()
    print(feedbackText)

    if (feedbackText == "Thank You for Entering!"):
        print("Successfully entered on " + site + " site")
    else:
        print("Error: Submission to " + site + " site failed")

    time.sleep(1)

def enterSweeps(email):
    navAndEnter("HGTV", email)
    navAndEnter("FoodNetwork", email)

# Check for emails to submit
emailFile = open('emails.txt')
emails = emailFile.readlines()
emailFile.close()

for e in emails:
    e = e.strip()
    if (e != ""):
        print('Entering sweeps with: ' + e)
        enterSweeps(e)

browser.quit()
