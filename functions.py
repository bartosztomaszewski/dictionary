import sqlite3
import os
from random import randint
import json
from repository import *

cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class table:
    def __init__(self, tableName, counterColumnName):
        self.tableName = tableName.replace("'","")
        self.counterColumnName = counterColumnName.replace("'","")


def addWord(dbCon,dbCur):
    createWordsTable(dbCon,dbCur)
    addingMode = True
    while addingMode:
        try:
            eng = input("English word: ")
            if eng in ("q", ""):
                raise ValueError
            pl  = input("Polish translation: ")
            if pl == "q" or eng == "":
                raise ValueError
            wordType = input("Type (noun/verb/adjective/other): ")
            if wordType == "q" or eng == "":
                raise ValueError
            cls()
            addWord(dbCon,dbCur,eng,pl,wordType)
        except ValueError:
            cls()
            addingMode = False
            print('The operation has been canceled')


def addExpression(dbCon, dbCur):
    while True:
        expression = input("Write an English expression: ")
        if expression in ['q', '']:
            print("The operation has been cancelled\n")
            return
        comment = input("Any comment?: ")
        if comment == 'q':
            print("The operation has been cancelled\n")
            return
        result = addExpressionToDb(dbCon, dbCur, expression, comment)
        if result is True:
            cls()
            print(f'The expression "{bcolors.OKGREEN}{expression}{bcolors.ENDC}" has been added successfully!\n')
        else:
            print(f'The error has occured: {result}\n')

def addWord(dbCon,dbCur,wEng,wPl,wType):
    result = addWordToDb(dbCon,dbCur,wEng,wPl,wType)
    if result is True:
        print(f'{bcolors.OKGREEN}The word "{wEng}/{wPl}/{wType}" has been added successfully!{bcolors.ENDC}')
    else:
        print(f'The error has occured: {result}')

def administratingMode(dbCur):           
    cls()
    words = getAllWordsInDb(dbCur)
    print("eng / pl / type / how many times it was trained\n")
    for word in words:
        print(f'{word}')
    
    answer = input('''
1 - Select an English word you wanna edit
2 - Reset all counters
3 - Export all words to JSON file
4 - Import all words from JSON file (it won't change English words)
5 - Show number of words per level
q - return to the main menu\n: ''')
    return answer, words

def am_editWord(dbCon,dbCur):
    editingWord = input('Write an English word: ')
    answer = input ('''
1 - Delete word
2 - Set counter
3 - Make a correction
Your choice: ''')
    return answer, editingWord

def am_setCounter(dbCon, dbCur, editingWord):
    correctFormat = False
    newCounter = None
    while not correctFormat and newCounter != 'q': 
        newCounter = input(f'Write a new value for "{editingWord}" counter: ')
        if newCounter.isNumber():
            counterAfterChange = setCounterInDb(dbCon, dbCur, editingWord, newCounter)
            if str(counterAfterChange[0][0]) == str(newCounter):
                print(f'Counter has been set to {newCounter} for word "{editingWord}" successfully')
                correctFormat = True
            else:
                print(f'We were unable to set counter for word "{editingWord}", please try again.')
        elif newCounter != 'q':
            print(f'"{newCounter}" is not a number! Try again...')
        else:
            print("Operation cancelled")

def am_makeCorrection(dbCon, dbCur, editingWord):
    eng = input('Write a new English word: ')
    pl = input('Write a new Polish word: ')
    wordType = input("Write a new type (noun/verb/adjective/other): ")
    correctWord(dbCon, dbCur, eng, pl, wordType, editingWord)

def exportWordsToJson(file, words):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    cls()
    print(f'All words has been exported to {bcolors.OKGREEN}{file}{bcolors.ENDC} file')

def importWordsFromJson(file, dbCon, dbCur):
    f = open(file, 'r', encoding='utf-8')
    data = json.load(f)
    cls()
    importWordsFromJsonIntoDb(dbCon, dbCur, data)  
    print(f'Words have been updated successfully according to "{file}" file\n')


def showNumberOfWordsPerLevel(dbCur):
    allLevels = getAllKindsOfLevelsFromDb(dbCur)
    clearLevels = [str(level[0]) for level in allLevels]
    for level in clearLevels:
        numberOfWords = getNumberOfWordsOnThatLevelInDb(dbCur, level)
        print(f'Level {level} -> words {numberOfWords[0][0]}')  
    answer = input('''
Write a level to show all words on this level
q - back to main menu
Your answer: ''')
    while True:
        if answer in clearLevels or answer == 'q':
            return answer
        print('\nYou chose a wrong option')
        answer = input('Your answer: ')
        
def showWordsOnChosenLevel(dbCur, level):
    cls()
    print(f'Your answer: {level}')
    words = getAllWordsOnThatLevelInDb(dbCur, level)
    print('')
    for word in words:
        print(f'{word[0]} / {word[1]} / {word[2]}')
    print('')

def correctWord(dbCon, dbCur, eng, pl, wordType, editingWord):
    result = changeWordInDb(dbCon, dbCur, eng, pl, wordType, editingWord)
    if result is True:
        cls()
        print(f'The word "{editingWord}" has been changed. The new one is "{eng}/{pl}/{wordType}"')
    else:
        cls()
        print(f'There was an error during updating the word "{editingWord}": {result}')

def createDatabaseCursor(dbCon):
    return dbCon.cursor()

def createClassesWithTables(dbCur):
    allTables = getAllTablesInDb(dbCur)
    listOfTables = []
    for myTable in allTables:
        #learningColumn = len(myTable[1].split())
        learningColumn = [i for i, item in enumerate(myTable[1].split()) if item.startswith('howMany')]
        #tempTable = table(myTable[0],myTable[1].split()[length-2])
        tempTable = table(myTable[0],myTable[1].split()[learningColumn[0]])
        listOfTables.append(tempTable)
    return listOfTables

def createWordsTable(dbCon,dbCur):
    createDictionaryTableInDb(dbCon,dbCur)

def am_deleteWord(dbCon, dbCur, word):
    before = getNumberOfWordsInDb(dbCur)
    deleteWordFromDb(dbCon, dbCur, word)
    after = getNumberOfWordsInDb(dbCur)
    if before[0][0] == after[0][0] + 1:
        cls()
        print(f'The word "{word}" has been deleted successfully')
    else:
        print(f'There was an error during deleting "{word}" word. The number of words in the dictionary is the same like before.')

def getRandom(dbCon, dbCur, tables, tableName):
    myTable = getTable(tables, tableName)
    theSmallestLevel = getTheSmallestCounterValueInDb(dbCur, myTable)
    numberOfRowsOnTheSmallestLevel = getNumberOfRowsOnThatLevelInDb(dbCur, myTable, theSmallestLevel[0][0])
    randomNumber = randint(0, numberOfRowsOnTheSmallestLevel[0][0] - 1)
    #print(f'Random number: {randomNumber}, howManyRowsOnThisLevel: {howManyRowsOnThisLevel[0][0]}')
    match myTable.tableName:
        case 'dictionary':
            wordsOnTheSmallestLevel = getAllWordsOnThatLevelInDb(dbCur, theSmallestLevel[0][0])
            return wordsOnTheSmallestLevel[randomNumber]
        case 'expressions':
            expressionsOnTheSameLevel =  getAllExpressionsOnThatLevelInDb(dbCur,  theSmallestLevel[0][0])
            updatedCounter = expressionsOnTheSameLevel[randomNumber][2] + 1
            increaseExpressionCounterByOneInDb(dbCon, dbCur, expressionsOnTheSameLevel[randomNumber])
            return expressionsOnTheSameLevel[randomNumber]

"""
def getRandomExpression(dbCon, dbCur):
    dbCur.execute('''SELECT howManyRead FROM expressions
                     ORDER BY howManyRead ASC
                     LIMIT 1''')
    theSmallestValue = dbCur.fetchall()
    dbCur.execute('''SELECT COUNT(howManyRead)
                     FROM expressions
                     WHERE howManyRead = ?''',(theSmallestValue[0][0],))
    howManyExpressionsOnThisLevel = dbCur.fetchall()
    randomNumber = randint(0, howManyExpressionsOnThisLevel[0][0] - 1)
    dbCur.execute('''SELECT eng, comments FROM expressions
                     WHERE howManyRead = ?''',(theSmallestValue[0][0],))
    randomWord = dbCur.fetchall()
    dbCur.execute('''SELECT howManyRead FROM expressions
                     WHERE eng = ?''',(randomWord[randomNumber][0],))
    counter = dbCur.fetchall()
    updatedCounter = counter[0][0] + 1
    dbCur.execute('''UPDATE expressions
                     SET howManyRead = ? 
                     WHERE eng = ?''',(updatedCounter, randomWord[randomNumber][0]))
    dbCon.commit()
    return randomWord[randomNumber]
"""

def getRandomWord(dbCur):
    dbCur.execute('''SELECT howManyTrained FROM dictionary
                     ORDER BY howManyTrained ASC
                     LIMIT 1''')
    theSmallestValue = dbCur.fetchall()
    dbCur.execute('''SELECT COUNT(howManyTrained)
                     FROM dictionary
                     WHERE howManyTrained = ?''',(theSmallestValue[0][0],))
    howManyWordsOnThisLevel = dbCur.fetchall()
    dbCur.execute('''SELECT eng, pl, type FROM dictionary
                     WHERE howManyTrained = ?''',(theSmallestValue[0][0],))
    randomWord = dbCur.fetchall()
    randomNumber = randint(0, howManyWordsOnThisLevel[0][0] - 1)
    #print(f'Random number: {randomNumber}, howManyRowsOnThisLevel: {howManyWordsOnThisLevel[0][0]}')
    return randomWord[randomNumber]

def getTable(allTables, tableName):
    for table in allTables:
        if table.tableName == tableName:
            return table

def initializeDatabase(dbName):
    databaseConnection = None
    try:
        databaseConnection = sqlite3.connect(f'database\\{dbName}.db')
    except sqlite3.Error as e:
        print(e + ' in ' + 'database' + '\\' + dbName)
    finally:
        if createDatabaseCursor is None:
            print ('There was an error during connecting to database')
        else:
            print ('Database has been connected')
        return databaseConnection

def learningModeEngToPl(dbCon,dbCur):
    answer = None
    cls()
    while answer != 'q':
        word = getRandomWord(dbCur)
        print(f'Type: {word[2]}\nEnglish: {word[0]}')
        answer = input("English: ")
        if word[2] in ['noun', 'verb', 'adjective']:
            plWords = word[1].split(', ')
        else:
            plWords = word[1]
        if answer in plWords:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC} {word[1]}\n")
            increaseWordCounterByOneInDb(dbCon,dbCur,word[0])
        else:
            print(f"{bcolors.FAIL}Wrong answer{bcolors.ENDC}, the correct is: {word[1]}\n")
    cls()   

def learningModePlToEng(dbCon,dbCur):
    answer = None
    cls()
    while answer != 'q':
        word = getRandomWord(dbCur)
        print(f'Type: {word[2]}\nPolish: {word[1]}')
        answer = input("English: ")
        if answer == word[0]:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}\n")
            increaseWordCounterByOneInDb(dbCon,dbCur,answer)
        else:
            print(f"Wrong answer, the correct is: {bcolors.FAIL}{word[0]}{bcolors.ENDC}\n")
    #cls()

def readingMode(dbCon,dbCur):
    createReadingTableInDb(dbCon,dbCur)
    cls()
    while True:        
        answer = input('''1 - Add an expression
2 - Read a random expression
3 - Reset reading counters
q - return to the main menu
Your choice: ''')
        if answer in ['1', '2', '3', 'q']:
            return answer
        print('Wrong answer, try one more time\n')



def readRandomExpression(dbCon, dbCur, allTables):
    while True:
        #expression = getRandomExpression(dbCon, dbCur)
        expression = getRandom(dbCon, dbCur, allTables, 'expressions')
        print(f'Expression: {expression[0]}\nComments: {expression[1]}')
        ifExit = input()
        if ifExit == 'q':
            cls()
            return

def resetReadingCounters(dbCon, dbCur):
    resetAllExpressionsCounterInDb(dbCon, dbCur)
    cls()
    print("All expressions' counters have been set to 0\n")

def resetAllWordsCounters(dbCon, dbCur):
    result = resetAllWordsCountersInDb(dbCon, dbCur)
    if result is True:
        print('All counters have been set to 0')
    else:
        print(f"There was an error during reseting words' counters: {result}")