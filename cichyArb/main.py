# This is a sample Python script.

import time
import re
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
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
    def __init__(self, betInfoList=[], arbCoefficent=0):
        self.betInfoList=betInfoList
        self.arbCoefficent = arbCoefficent

def getSimiliarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# initiral setup

DRIVER_PATH = "C:/chromedrv/chromedriver.exe"

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
options.add_argument("lang=en-GB");

driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)

# cloudbet scraping

#driver.get("https://www.cloudbet.com/en/sports/soccer/international-clubs-uefa-champions-league")
driver.get("https://www.cloudbet.com/en/sports/soccer/international-world-cup")

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



# stake scraping

#driver.get("https://stake.com/sports/soccer/international-clubs/uefa-champions-league")
driver.get("https://stake.com/sports/soccer/international/world-cup")

renderSwitch = True
while renderSwitch:
    time.sleep(0.5)

    pageSource = driver.page_source

    soup = BeautifulSoup(pageSource, "lxml")
    betsRef = soup.find_all("div", attrs={"data-test" : "fixture-preview"})
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

# print("PRINTING CLOUDBETS")
# counter = 0
# for bet in cloudbetBets:
#     print(bet.__str__())
#     counter += 1
# print("PRINTED", counter, "CLOUDBETS")
#
# print("PRINTING STAKEBETS")
# counter = 0
# for bet in stakeBets:
#     print(bet.__str__())
#     counter+=1
# print("PRINTED", counter, "STAKEBETS")

arbSets = []

for cloudBet in cloudbetBets:
    for stakeBet in stakeBets:
        if getSimiliarity(cloudBet.optionAName, stakeBet.optionAName) > 0.8 and getSimiliarity(cloudBet.optionBName, stakeBet.optionBName) > 0.8:
            tempArbSet = ArbSet(betInfoList=[cloudBet, stakeBet])

            if cloudBet.aWinOdds > stakeBet.aWinOdds:
                awh = cloudBet.aWinOdds
            else:
                awh = stakeBet.aWinOdds

            if cloudBet.drawOdds > stakeBet.drawOdds:
                bwh = cloudBet.drawOdds
            else:
                bwh = stakeBet.drawOdds

            if cloudBet.bWinOdds > stakeBet.bWinOdds:
                dwh = cloudBet.bWinOdds
            else:
                dwh = stakeBet.bWinOdds

            if awh ==0.0 or bwh ==0.0 or dwh == 0.0:
                print("WTFWTFWTF", cloudBet.optionAName)

            tempArbSet.arbCoefficent = (1.0/awh + 1.0/dwh + 1.0/bwh)

            arbSets.append(tempArbSet)

def sorter(e):
    return e.arbCoefficent

arbSets.sort(key=sorter)

print("PRINTING SETS FROM {} CLOUDBETS AND {} STAKEBETS".format(len(cloudbetBets), len(stakeBets)))
counter = 0
for arbSet in arbSets:
    print(arbSet.betInfoList[0], "|", arbSet.betInfoList[1], "|", arbSet.arbCoefficent)
    counter += 1
print("PRINTED", counter, "ARBSETS")

