import time

from globals import ArbSet
from globals import BetInfo
from utils import getMultiFootball
from utils import matchBetSets

# scraping odds data

cloudLinksFB = ["https://www.cloudbet.com/en/sports/soccer/england-premier-league",
              "https://www.cloudbet.com/en/sports/soccer/germany-bundesliga",
              "https://www.cloudbet.com/en/sports/soccer/international-world-cup",
              "https://www.cloudbet.com/en/sports/soccer/france-championnat-national-u19",
              "https://www.cloudbet.com/en/sports/soccer/spain-laliga"]

stakeLinksFB = ["https://stake.com/sports/soccer/england/premier-league",
              "https://stake.com/sports/soccer/germany/bundesliga",
              "https://stake.com/sports/soccer/international/world-cup",
              "https://stake.com/sports/soccer/france/championnat-national-u19",
              "https://stake.com/sports/soccer/spain/la-liga"]

cloudbetBetsFB = getMultiFootball("cloudbet", cloudLinksFB)
stakeBetsFB = getMultiFootball("stake", stakeLinksFB)

# calculating profitability

arbSetsFB = matchBetSets([cloudbetBetsFB, stakeBetsFB])

# printing
counter = 0
for arbSet in arbSetsFB:
    print(arbSet)
    counter += 1
print("PRINTED", counter, "ARBSETS", "FROM", len(cloudbetBetsFB), "CLOUDBETBETS AND", len(stakeBetsFB), "STAKEBETS")

