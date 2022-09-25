# This is a sample Python script.

import bookies
import time
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


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

# initial setup

DRIVER_PATH = "C:/chromedrv/chromedriver.exe"

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
options.add_argument("lang=en-GB");

driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)

# scraping odds data

cloudbetBets = bookies.getCloudBetSoccer(driver=driver, link="https://www.cloudbet.com/en/sports/soccer/spain-laliga")
stakeBets = bookies.getStakeSoccer(driver=driver, link="https://stake.com/sports/soccer/spain/la-liga")

# calculating profitability

arbSets = []
leftovers = []
for cloudBet in cloudbetBets:
    for stakeBet in stakeBets:
        if getSimiliarity(cloudBet.optionAName, stakeBet.optionAName) > 0.7 and getSimiliarity(cloudBet.optionBName, stakeBet.optionBName) > 0.7:
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

            tempArbSet.arbCoefficient = (1.0/awh + 1.0/dwh + 1.0/bwh)

            arbSets.append(tempArbSet)


def sorter(e):
    return e.arbCoefficient

arbSets.sort(key=sorter)

print("PRINTING SETS FROM {} CLOUDBETS AND {} STAKEBETS".format(len(cloudbetBets), len(stakeBets)))
counter = 0
for arbSet in arbSets:
    print(arbSet.betInfoList[0], "|", arbSet.betInfoList[1], "|", arbSet.arbCoefficient)
    counter += 1
print("PRINTED", counter, "ARBSETS")

for bet in cloudBet:
    add = True
    for arbSet in arbSets:
        if cloudBet.optionAName == arbSet.betInfoList[0].optionAName:
            add = False
    if add:
        leftovers.append(cloudBet)

counter = 0
for bet in leftovers:
    print("LEFTOVER CB:", bet.__str__())
print("PRINTED", counter, "LEFT")

