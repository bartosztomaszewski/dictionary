import sqlite3
import os
from random import randint
import json

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
            os.system('cls')
            addRow(dbCon,dbCur,eng,pl,wordType)
        except ValueError:
            os.system('cls')
            addingMode = False
            print('The operation has been canceled')


def addExpression(dbCon, dbCur, expression, comment):
    try:
        dbCur.execute('''INSERT INTO expressions
                         VALUES (?, ?, '0')''',(expression,comment))
        dbCon.commit()
        os.system('cls')
        print(f'The expression "{bcolors.OKGREEN}{expression}{bcolors.ENDC}" has been added successfully!')
    except sqlite3.Error as e:
        print(f'The error has occured: {e}')
    return

def addRow(dbCon,dbCur,wEng,wPl,wType):
    try:
        dbCur.execute('''INSERT INTO dictionary
                         VALUES (?, ?, ?, '0')''',(wEng,wPl,wType))
        dbCon.commit()
        print(f'{bcolors.OKGREEN}The word "{wEng}/{wPl}/{wType}" has been added successfully!{bcolors.ENDC}')
    except sqlite3.IntegrityError as e:
        print(f'The word "{wEng}" already exists in the database')
    except (sqlite3.Error, sqlite3.Error)  as e:
        print(f'The error has occured: {e}')
    return

def administratingMode(dbCon,dbCur):           
    os.system('cls')
    words = getAllWords(dbCur)
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
    match answer:
        case '1':
            editingWord = input('Write an English word: ')
            answer = input ('''
1 - Delete word
2 - Set counter
3 - Make a correction
Your choice: ''')         
            match answer:
                case '1':
                    deleteWord(dbCon, dbCur, editingWord)
                case '2':
                    correctFormat = False
                    newCounter = None
                    while not correctFormat and newCounter != 'q': 
                        newCounter = input(f'Write a new value for "{editingWord}" counter: ')
                        try:
                            int(newCounter)
                            setCounter(dbCon, dbCur, editingWord, newCounter)
                            correctFormat = True
                        except:
                            if newCounter != 'q':
                                print(f'"{newCounter}" is not a number! Try again...')
                            else:
                                print("Operation cancelled")
                case '3':
                    eng = input('Write a new English word: ')
                    pl = input('Write a new Polish word: ')
                    wordType = input("Write a new type (noun/verb/adjective/other): ")
                    correctWord(dbCon, dbCur, eng, pl, wordType, editingWord)
                case _:
                    print("You didn't choose any of the available options.")
        case '2':
            resetAllCounters(dbCon, dbCur)
        case '3':
            with open('database\\words.json', 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            os.system('cls')
            print(f'All words has been exported to {bcolors.OKGREEN}words.json{bcolors.ENDC} file in "database" folder')
        case '4':
            f = open('database\\words.json', 'r', encoding='utf-8')
            data = json.load(f)
            os.system('cls')
            for word in data:
                try:
                    dbCur.execute('''UPDATE dictionary
                        SET eng = ?, pl = ?, type = ?, howManyTrained = ?
                        WHERE eng = ?''',(word[0], word[1], word[2], word[3], word[0]))
                except sqlite3.Error as e:
                    print(f'There was an error during updating the word "{word}": {e}')
            dbCon.commit()
            print('Words have been updated successfully according to "words.json" file\n')
        case '5':
            dbCur.execute('''SELECT DISTINCT howManyTrained
                             FROM dictionary
                             ORDER BY howManyTrained ASC''')
            allLevels = dbCur.fetchall()
            #print(allLevels)
            clearLevels = []
            for level in allLevels:
                clearLevels.append(str(level[0]))
            loop = True
            while loop:
                for level in clearLevels:
                    dbCur.execute('''SELECT COUNT(eng)
                                    FROM dictionary
                                    WHERE howManyTrained = ?''',(level,))
                    numberOfWords = dbCur.fetchall()
                    print(f'Level {level} -> words {numberOfWords[0][0]}')
                answer = input('''
Write a level to show all words on this level
q - back to main menu
Your answer: ''')
                os.system('cls')
                print(f'Your answer: {answer}')
                if answer in clearLevels:
                    dbCur.execute('''SELECT eng, pl, type
                                    FROM dictionary
                                    WHERE howManyTrained = ?
                                    ORDER BY eng ASC''',(answer,))
                    print('')
                    for word in dbCur.fetchall():
                        print(f'{word[0]} / {word[1]} / {word[2]}')
                    print('')
                elif answer is 'q':
                    loop = False
                    os.system('cls')
                else:
                    os.system('cls')
                    print('Wrong answer!\n')
        case 'q':
            os.system('cls')

def correctWord(dbCon, dbCur, eng, pl, wordType, editingWord):
    try:
        dbCur.execute('''UPDATE dictionary
                         SET eng = ?, pl = ?, type = ?
                         WHERE eng = ?''',(eng, pl, wordType, editingWord))
        dbCon.commit()
        os.system('cls')
        print(f'The word "{editingWord}" has been changed. The new one is "{eng}/{pl}/{wordType}"')
    except sqlite3.Error as e:
        os.system('cls')
        print(f'There was an error during updating the word "{editingWord}": {e}')

def createDatabaseCursor(dbCon):
    return dbCon.cursor()

def createReadingTable(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS expressions
                     (eng TEXT, comments TEXT, howManyRead INT)''')
    dbCon.commit()
    return

def createClassesWithTables(dbCur):
    dbCur.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    allTables = dbCur.fetchall()
    listOfTables = []
    for myTable in allTables:
        #learningColumn = len(myTable[1].split())
        learningColumn = [i for i, item in enumerate(myTable[1].split()) if item.startswith('howMany')]
        #tempTable = table(myTable[0],myTable[1].split()[length-2])
        tempTable = table(myTable[0],myTable[1].split()[learningColumn[0]])
        listOfTables.append(tempTable)
    return listOfTables

def createWordsTable(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS dictionary
                     (eng TEXT PRIMARY KEY, pl TEXT, type TEXT, howManyTrained INT)''')
    dbCon.commit()
    return

def deleteWord(dbCon, dbCur, word):
    dbCur.execute('''SELECT COUNT(eng)
                     FROM dictionary''')
    before = dbCur.fetchall()
    dbCur.execute('''DELETE FROM dictionary
                     WHERE eng = ?''',(word,))
    print (dbCur.fetchall())
    dbCon.commit()
    dbCur.execute('''SELECT COUNT(eng)
                     FROM dictionary''')
    after = dbCur.fetchall()
    if before[0][0] == after[0][0] + 1:
        os.system('cls')
        print(f'The word "{word}" has been deleted successfully')
    else:
        print(f'There was an error during deleting "{word}" word. The number of words in the dictionary is the same like before.')

def getAllWords(dbCur):
    dbCur.execute('''SELECT eng, pl, type, howManyTrained FROM dictionary
                     ORDER BY eng ASC''')
    return dbCur.fetchall()

def getRandom(dbCon, dbCur, tables, tableName):
    myTable = getTable(tables, tableName)
    dbCur.execute(f'''SELECT {myTable.counterColumnName} 
                      FROM {myTable.tableName} 
                      ORDER BY {myTable.counterColumnName} 
                      ASC LIMIT 1''')
    theSmallestValue = dbCur.fetchall()
    dbCur.execute(f'''SELECT COUNT({myTable.counterColumnName})
                    FROM {myTable.tableName}
                    WHERE {myTable.counterColumnName} = {theSmallestValue[0][0]}''')
    howManyRowsOnThisLevel = dbCur.fetchall()
    randomNumber = randint(0, howManyRowsOnThisLevel[0][0] - 1)
    #print(f'Random number: {randomNumber}, howManyRowsOnThisLevel: {howManyRowsOnThisLevel[0][0]}')
    match myTable.tableName:
        case 'dictionary':
            dbCur.execute('''SELECT eng, pl, type FROM dictionary
                    WHERE howManyTrained = ?''',(theSmallestValue[0][0],))
            randomWord = dbCur.fetchall()
            return randomWord[randomNumber]
        case 'expressions':
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

def increaseWordCounter(dbCon,dbCur,word):
    dbCur.execute('''SELECT howManyTrained FROM dictionary
                     WHERE eng = ?
                     OR pl = ?''',(word, word))
    counter = dbCur.fetchall()
    updatedCounter = counter[0][0] + 1
    dbCur.execute('''UPDATE dictionary
                     SET howManyTrained = ? 
                     WHERE eng = ?
                     OR pl = ?''',(updatedCounter, word, word))
    dbCon.commit()

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
    os.system('cls')
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
            increaseWordCounter(dbCon,dbCur,word[0])
        else:
            print(f"{bcolors.FAIL}Wrong answer{bcolors.ENDC}, the correct is: {word[1]}\n")
    os.system('cls')   

def learningModePlToEng(dbCon,dbCur):
    answer = None
    os.system('cls')
    while answer != 'q':
        word = getRandomWord(dbCur)
        print(f'Type: {word[2]}\nPolish: {word[1]}')
        answer = input("English: ")
        if answer == word[0]:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}\n")
            increaseWordCounter(dbCon,dbCur,answer)
        else:
            print(f"Wrong answer, the correct is: {bcolors.FAIL}{word[0]}{bcolors.ENDC}\n")
    #os.system('cls')

def readingMode(dbCon,dbCur,allTables):
    createReadingTable(dbCon,dbCur)
    os.system('cls')                
    answer = input('''1 - Add an expression
2 - Read a random expression
3 - Reset reading counters
q - return to the main menu
Your choice: ''')
    match answer:
        case '1':
            addingMode = True
            while addingMode:
                try:
                    expression = input("Write an English expression: ")
                    if expression == "q" or expression == "":
                        raise ValueError
                    comment = input("Any comment?: ")
                    if comment == "q":
                        raise ValueError
                    addExpression(dbCon, dbCur, expression, comment)
                except ValueError:
                    os.system('cls')
                    print("The operation has been cancelled\n")
                    addingMode = False
        case '2':
            readingMode = True
            while readingMode:
                #expression = getRandomExpression(dbCon, dbCur)
                expression = getRandom(dbCon, dbCur, allTables, 'expressions')
                print(f'Expression: {expression[0]}\nComments: {expression[1]}')
                comment = input()
                if comment == 'q':
                    readingMode = False
                    os.system('cls')
        case '3':
            #zintegrować to z 'resetAllCounters'
            try:
                dbCur.execute('''UPDATE expressions
                                    SET howManyRead = 0''')
                dbCon.commit()
                print("All expressions' counters have been set to 0")
            except sqlite3.Error as e:
                print(f"There was an error during reseting words' counters: {e}")
        case 'q':
                        os.system('cls')

def resetAllCounters(dbCon, dbCur):
    try:
        dbCur.execute('''UPDATE dictionary
                        SET howManyTrained = 0''')
        dbCon.commit()
        print('All counters have been set to 0')
    except sqlite3.Error as e:
        print(f"There was an error during reseting words' counters: {e}")

def setCounter(dbCon, dbCur, word, counter):
    dbCur.execute('''UPDATE dictionary
                     SET howManyTrained = ? 
                     WHERE eng = ?
                     OR pl = ?''',(counter, word, word))
    dbCon.commit()
    dbCur.execute('''SELECT howManyTrained
                     FROM dictionary
                     WHERE eng = ?
                     OR pl = ?''',(word, word))
    after = dbCur.fetchall()
    if str(after[0][0]) == counter:
        print(f'Counter has been set to {counter} for word "{word}" successfully')
    else:
        print(f'We were unable to set counter for word "{word}", please try again.')