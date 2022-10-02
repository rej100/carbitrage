import time
import re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from globals import BetInfo

def getCloudBetFootball(driver, link):
    driver.get(link)

    renderSwitch = True
    while renderSwitch:
        time.sleep(0.5)

        pageSource = driver.page_source

        soup = BeautifulSoup(pageSource, "lxml")
        betsRef = soup.find_all("p", text=re.compile(":"))
        if len(betsRef) > 0:
            renderSwitch = False;

            time.sleep(1)

            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, "lxml")
            betsRef = soup.find_all("p", text=re.compile(":"))

    betContainers = []

    for bet in betsRef:
        betContainers.append(bet.parent.parent)

    cloudbetBets = []

    for betContainer in betContainers:
        testBetInfo = BetInfo()
        testBetInfo.bookieName = "cloudBet"
        try:
            testBetInfo.optionAName = betContainer.find_all("a")[1].find("div").find("div").find("div").find("div").find("p").text
            testBetInfo.optionBName = betContainer.find_all("a")[1].find("div").find("div").findChildren("div", recursive=False)[1].find("div").find("p").text
            testBetInfo.aWinOdds = float(betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[0].find("p").text)
            testBetInfo.drawOdds = float(betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[1].find("p").text)
            testBetInfo.bWinOdds = float(betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[2].find("p").text)
        except:
            break

        cloudbetBets.append(testBetInfo)

    return cloudbetBets