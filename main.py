# This program will submit email addresses into the
# drawing for the 2022 HGTV Dream Home Sweepstakes
# (https://www.hgtv.com/sweepstakes/hgtv-dream-home)
# Pre reqs:
#   - You must have already done the initial entry for the email address to submit as this requires some manual information (Name, Cable Provider, Etc)
#   - Any emails must be in a file named "emails.txt" in the same directory. One email address per line

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
logFile = open('log.txt', 'a')

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

    # Navigate to the URL and give the site time to load
    browser.get(url)

    # The email element is bundled in an iframe, so we have to switch to that frame
    while True:
        try:
            browser.switch_to.frame(browser.find_element(By.ID, frameID))
        except:
            print('Waiting for frame to become ready')
            time.sleep(1)
            continue
        else:
            break

    # Submit the email address
    emailField = browser.find_element(By.NAME, 'xReturningUserEmail')
    emailField.send_keys(em)

    # The site appears to do some validation in the background so if you submit too
    # quickly, you will receive an error message instead of proceeding on the form
    time.sleep(1)
    emailField.submit()
    time.sleep(1)
    
    # Check for errors on this screen
    while True:
        try:
            feedbackElem = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/section/div/div/div/div/div/div[2]/div/div/div/div/div/p/b')
        except:
            print('Locating the feedback text')
            time.sleep(1)
        else:
            break
    
    feedbackText = feedbackElem.text.strip()

    if (feedbackText == "Sorry! You've already entered today. Please come back tomorrow to try again."):
        print("Error: Already entered " + em + " on " + site + " site")
        logFile.write("Error: Already entered " + em + " on " + site + " site" + '\n')
        logFile.flush()
        os.fsync(logFile.fileno())
        return
    else:
        # Wait for the next screen / ads to load after submission
        time.sleep(1)

        # We need to go to the bottom of the outter page to be able to see the enter button
        html = browser.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(1)

        # Click the Enter Button
        while True:
            try:
                enterButton = browser.find_element(By.XPATH, '/html/body/div[1]/div/main/section/div/div/div/div/div/div[1]/div/div[2]/form[2]/div[2]/div/button/span')
            except:
                print('Locating the enter button')
                time.sleep(1)
            else:
                break
        
        enterButton.click()

        # Check for success
        while True:
            try:
                feedbackElem = browser.find_element(By.XPATH, '/html/body/section/div[3]/div[3]/div/div[2]/div[1]/div/div[3]/div[1]/section/p/b')
            except:
                print('Locating the feedback text')
                time.sleep(1)
            else:
                break
        
        feedbackText = feedbackElem.text.strip()

        if (feedbackText == "Thank You for Entering!"):
            print("Successfully entered " + em + " on " + site + " site")
            logFile.write("Successfully entered " + em + " on " + site + " site" + '\n')
            logFile.flush()
            os.fsync(logFile.fileno())
        else:
            print("Error: Submitting " + em + " to " + site + " site failed")
            logFile.write("Error: Submitting " + em + " to " + site + " site failed" + '\n')
            logFile.flush()
            os.fsync(logFile.fileno())

        time.sleep(1)

def enterSweeps(email):
    navAndEnter("HGTV", email)
    navAndEnter("FoodNetwork", email)

now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
logFile.write('--> Begin: ' + dt_string + '\n')
logFile.flush()
os.fsync(logFile.fileno())

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

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
logFile.write('<-- End: ' + dt_string + '\n')
logFile.flush()
os.fsync(logFile.fileno())

logFile.close()
