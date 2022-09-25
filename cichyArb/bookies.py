import time
import re
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class BetInfo:
    def __init__(self, bookieName="", optionAName="", optionBName="", aWinOdds=0, drawOdds=0, bWinOdds=0):
        self.bookieName=bookieName
        self.optionAName=optionAName
        self.optionBName=optionBName
        self.aWinOdds=aWinOdds
        self.drawOdds=drawOdds
        self.bWinOdds=bWinOdds
    def __str__(self):
        return "{} {} {} {} {} {}".format(self.bookieName, self.optionAName, self.optionBName, self.aWinOdds, self.drawOdds, self.bWinOdds)

class ArbSet:
    def __init__(self, betInfoList=[], arbCoefficient=0):
        self.betInfoList=betInfoList
        self.arbCoefficient = arbCoefficient

def getCloudBetSoccer(driver, link):
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
            testBetInfo.optionAName = betContainer.find_all("a")[1].find("div").find("div").find("div").find(
                "div").find("p").text
            testBetInfo.optionBName = \
            betContainer.find_all("a")[1].find("div").find("div").findChildren("div", recursive=False)[1].find(
                "div").find("p").text
            testBetInfo.aWinOdds = float(
                betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[0].find(
                    "p").text)
            testBetInfo.drawOdds = float(
                betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[1].find(
                    "p").text)
            testBetInfo.bWinOdds = float(
                betContainer.findChildren(("div"), recursive=False)[0].findChildren("button", recursive=False)[2].find(
                    "p").text)
        except:
            break
        cloudbetBets.append(testBetInfo)
    return cloudbetBets

def getStakeSoccer(driver, link):
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
            testBetInfo.optionAName = bet.find_all("button")[1].find_all("span")[0].text
            testBetInfo.aWinOdds = float(bet.find_all("button")[1].find_all("span")[-1].text.replace(",", "."))
            testBetInfo.drawOdds = float(bet.find_all("button")[2].find_all("span")[-1].text.replace(",", "."))
            testBetInfo.optionBName = bet.find_all("button")[3].find_all("span")[0].text
            testBetInfo.bWinOdds = float(bet.find_all("button")[3].find_all("span")[-1].text.replace(",", "."))
        except:
            break
        stakeBets.append(testBetInfo)
    return stakeBets
