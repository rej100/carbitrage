class BetInfo:
    def __init__(self, bookieName="", optionAName="", optionBName="", aWinOdds=0.0, drawOdds=0.0, bWinOdds=0.0):
        self.bookieName=bookieName
        self.optionAName=optionAName
        self.optionBName=optionBName
        self.aWinOdds=aWinOdds
        self.drawOdds=drawOdds
        self.bWinOdds=bWinOdds
    def __str__(self):
        return "{} {} vs {} {} {} {}".format(self.bookieName, self.optionAName, self.optionBName, self.aWinOdds, self.drawOdds, self.bWinOdds)

class ArbSet:
    def __init__(self, betInfoList=[], arbCoefficient=0):
        self.betInfoList=betInfoList
        self.arbCoefficient = arbCoefficient
    def __str__(self):
        finalStr = ""
        for betInfo in self.betInfoList:
            finalStr += betInfo.__str__()
            finalStr += " | "
        finalStr += str(self.arbCoefficient)
        return finalStr