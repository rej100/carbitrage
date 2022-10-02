from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

from globals import ArbSet
from globals import BetInfo

from cloudbet import getCloudBetFootball
from stake import getStakeFootball

def getSimiliarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def arbSorter(e):
    return e.arbCoefficient

def createDriver():
    DRIVER_PATH = "C:/chromedrv/chromedriver.exe"

    options = Options()
    ua = UserAgent()
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("lang=en-GB")

    return webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)

def getMultiFootball(bookieName, linkList):
    betsInfoSet = []

    if bookieName == "cloudbet":
        driver = createDriver()
        for link in linkList:
            betsInfoSet += getCloudBetFootball(driver, link)
    elif bookieName == "stake":
        for link in linkList:
            driver = createDriver()
            betsInfoSet += getStakeFootball(driver, link)

    return  betsInfoSet

def matchBetSets(betInfoSets):
    arbSets = []

    for betInfo in betInfoSets[0]:
        tempArbSet = ArbSet(betInfoList=[], arbCoefficient=0)
        tempArbSet.betInfoList.append(betInfo)

        i = 1
        while i < len(betInfoSets):
            for betInfoAlt in betInfoSets[i]:
                if getSimiliarity(betInfo.optionAName, betInfoAlt.optionAName) >= 0.7 and getSimiliarity(betInfo.optionBName, betInfoAlt.optionBName) >= 0.7:
                    tempArbSet.betInfoList.append(betInfoAlt)
                elif getSimiliarity(betInfo.optionAName, betInfoAlt.optionBName) >= 0.7 and getSimiliarity(betInfo.optionBName, betInfoAlt.optionAName) >= 0.7:
                    temp = betInfoAlt.optionAName
                    betInfoAlt.optionAName = betInfoAlt.optionBName
                    betInfoAlt.optionBName = temp

                    temp = betInfoAlt.aWinOdds
                    betInfoAlt.aWinOdds = betInfoAlt.bWinOdds
                    betInfoAlt.bWinOdds = temp

                    tempArbSet.betInfoList.append(betInfoAlt)
            i+=1

        if len(tempArbSet.betInfoList) > 1:
            arbSets.append(tempArbSet)

    for arbSet in arbSets:
        awh = arbSet.betInfoList[0].aWinOdds
        dwh = arbSet.betInfoList[0].drawOdds
        bwh = arbSet.betInfoList[0].bWinOdds

        i = 1
        while i < len(arbSet.betInfoList):
            if arbSet.betInfoList[i].aWinOdds > awh:
                awh = arbSet.betInfoList[i].aWinOdds
            if arbSet.betInfoList[i].drawOdds > dwh:
                dwh = arbSet.betInfoList[i].drawOdds
            if arbSet.betInfoList[i].bWinOdds > bwh:
                bwh = arbSet.betInfoList[i].bWinOdds
            i+=1
        if not dwh == 0:
            arbSet.arbCoefficient = (1.0/awh+1.0/dwh+1.0/bwh)
        else:
            arbSet.arbCoefficient = (1.0/awh+1.0/bwh)

    arbSets.sort(key=arbSorter)

    return arbSets
