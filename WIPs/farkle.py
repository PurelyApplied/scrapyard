#!/usr/bin/python3
import random
printFullScoreSheet = False
# Checking for 1s/5s is checking for exactly 1 of either, not any of either

# 5s are 50 each
# 1s are 100 each
# Triples are [val] * 100 // Triple 1s are defacto 300
# Quad is 1k
# Quint is 2k
# Six of a kind is 3k
# Straight 1-6 is 1.5k
# Three Pairs is 1.5k
# Four + pair is 1.5k
# Double trips is 2.5k

# Score description, bool function, value
def playFarkle():
    previousRolls = []
    # locked dice: set, score
    lockedDice = []
    keepRolling = True
    while keepRolling:
        diceToRoll = 6 - len(lockedDice)
        thisRoll = rollNdK(diceToRoll, 6)
        thisRoll.sort()
        previousTotal = sum( [prev[1] for prev in previousRolls ])
        printInfo(previousRolls, lockedDice, thisRoll) 
        if not hasAnyScoring(thisRoll):
            print("You bust out!")
            keepRolling = False
        else:
            keepRolling = getUserInput(previousRolls, lockedDice, thisRoll)

def getUserInput(previousRolls, lockedDice, thisRoll):
    scorables = getListOfScorables(thisRoll)
    assert 0 < len(scorables), "User Input hit with bustout roll"
    if 1 == len(scorables):
        print("You must score [%d]: %s (%d)" % (scorables[0], scoresheet[scorables[0]][0], scoresheet[scorables[0]][2]))
    else:
        numScored = 0
        scoreAgain = True
        while scoreAgain:
            inp = input("Enter index of item you wish to score. >>")
            if not inp.isdigit() or not int(inp) in scorables:
                print("Cannot score input %s" % inp)
            else:
                #### Move from thisRoll to lockedDice
                #### If thisRoll is now empty, move lockedDice to previousRolls
                
                pass
    # Promp
    # If only one scoring event is thrown, you must claim it
    ## No input
    # Otherwise, prompt
    
    if input("Bank %d points and quit? (y/n) >> " % getScore(previousRolls + lockedDice)).lower() == "y":
        return False
    else:
        return True

def getListOfScorables(aList):
    scorables = []
    for i in range(len(scoresheet)):
        item = scoresheet[i]
        hit = item[1](aList)
        if hit or printFullScoreSheet:
            scorables.append(i)
    return scorables

def printInfo(previousRolls, lockedDice, thisRoll):
    if len(lockedDice) != 0:
        print("Locked dice:")
    for stuff in lockedDice:
        print("{} ({})".format(stuff[0], stuff[1]))
    print("This roll: {}".format(thisRoll))
    for i in range(len(scoresheet)):
        item = scoresheet[i]
        hit = item[1](thisRoll)
        line = "[%2d] %s %*s (%4d) %s" %(i,
                                         (">>>>>" if hit else "     "),
                                         scoreDescLen, item[0],
                                         item[2],
                                         ("<<<<<" if hit else "     ") )
        if hit or printFullScoreSheet:
            print(line)
    print("Current score: %d" % getScore(previousRolls + lockedDice))

def getScore(scoredList):
    return sum([ val[1] for val in scoredList]) 

def rollNdK(n,k):
    return [random.randint(1,k) for i in range(n)]

# Score bool functions

def isTwoTriples(aList):
    triples=0
    for i in range(1,7):
        if hasNKs(aList, 3, i):
            triples += 1
    return triples == 2

def isAFullHouse(aList):
    return hasASetOfSize(aList, 2) and hasASetOfSize(aList, 4)

def hasNKs(aList, n, k):
    return aList.count(k) == n

def isThreePairs(aList):
    pairs=0
    for i in range(1,7):
        if hasNKs(aList, 2, i):
            pairs += 1
    return pairs == 3
    
def isAStraight(aList):
    for i in range(1,7):
        if not hasNKs(aList, 1, i):
            return False
    return True

def hasASetOfSize(aList, n):
    for i in range(1,7):
        if hasNKs(aList, n, i):
            return True
    return False
    
# Locking functions

scoresheet=[
    ["Two sets of three of a kind", isTwoTriples, 2500],
    ["Three Pairs", isThreePairs, 1500],
    ["Four of a Kind + a Pair", isAFullHouse , 1500],
    ["A Straight of 1-6", isAStraight, 1500],
    ["Six of a Kind", lambda L: hasASetOfSize(L, 6), 3000],
    ["Five of a Kind", lambda L: hasASetOfSize(L, 5), 2000],
    ["Four of a Kind", lambda L: hasASetOfSize(L, 4), 1000],
    ["Triple 6s", lambda L: hasNKs(L, 3, 6), 600],
    ["Triple 5s", lambda L: hasNKs(L, 3, 5), 500],
    ["Triple 4s", lambda L: hasNKs(L, 3, 4), 400],
    ["Triple 3s", lambda L: hasNKs(L, 3, 3), 300],
    ["Triple 2s", lambda L: hasNKs(L, 3, 2), 200],
    ["Triple 1s", lambda L: hasNKs(L, 3, 1), 300],
    ["Double 1", lambda L: hasNKs(L, 2, 1), 200],
    ["Double 5", lambda L: hasNKs(L, 2, 5), 100],
    ["One 1", lambda L: hasNKs(L, 1, 1), 100],
    ["One 5", lambda L: hasNKs(L, 1, 5), 50]
]

def hasAnyScoring(aList):
    return sum([ item[1](aList) for item in scoresheet ] )

scoreDescLen = 0
for item in scoresheet:
    scoreDescLen = max(scoreDescLen, len(item[0]))

# Commandline
if __name__=="__main__":
    playFarkle()
