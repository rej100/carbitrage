import time
import re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from globals import BetInfo

def getStakeFootball(driver, link):
    driver.get(link)

    renderSwitch = True
    while renderSwitch:
        time.sleep(0.5)

        pageSource = driver.page_source

        soup = BeautifulSoup(pageSource, "lxml")
        betsRef = soup.find_all("div", attrs={"data-test": "fixture-preview"})
        if len(betsRef) > 0:
            renderSwitch = False

            time.sleep(1)

            moreSwitch = True
            while moreSwitch:
                try:
                    moreButton = driver.find_element(By.XPATH, "//button[contains(span, 'Load')]")
                    moreButton.click()
                except:
                    moreSwitch = False

                time.sleep(1)

            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, "lxml")

            betsRef = soup.find_all("div", attrs={"data-test": "fixture-preview"})

    stakeBets = []

    for bet in betsRef:
        testBetInfo = BetInfo()
        testBetInfo.bookieName = "stake"

        try:
            outcomesContainer = bet.find("div", attrs={"class" : "outcomes"})
            testBetInfo.optionAName = outcomesContainer.find_all("button")[0].find_all("span")[0].text
            testBetInfo.aWinOdds = float(outcomesContainer.find_all("button")[0].find_all("span")[-1].text.replace(",", "."))
            testBetInfo.drawOdds = float(outcomesContainer.find_all("button")[1].find_all("span")[-1].text.replace(",", "."))
            testBetInfo.optionBName = outcomesContainer.find_all("button")[2].find_all("span")[0].text
            testBetInfo.bWinOdds = float(outcomesContainer.find_all("button")[2].find_all("span")[-1].text.replace(",", "."))
        except:
            break
        stakeBets.append(testBetInfo)

    return stakeBets