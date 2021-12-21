import sqlite3
import os
from random import randint

def initializeDatabase(dbName):
    databaseConnection = None
    try:
        databaseConnection = sqlite3.connect(f'database\\{dbName}.db')
    except sqlite3.Error as e:
        print(e + ' in ' + "database" + '\\' + dbName)
    finally:
        if createDatabaseCursor != None:
            print ('Database has been connected')
        else:
            print ('There was an error during connecting to database')
        return databaseConnection

def createDatabaseCursor(dbCon):
    return dbCon.cursor()

def createWordsTable(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS dictionary
                     (eng TEXT PRIMARY KEY, pl TEXT, type TEXT, howManyTrained INT)''')
    dbCon.commit()
    return

def createReadingTable(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS expressions
                     (eng TEXT, comments TEXT, howManyRead INT)''')
    dbCon.commit()
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

def getRandomWord(dbCur):
    dbCur.execute('''SELECT howManyTrained FROM dictionary
                     ORDER BY howManyTrained ASC
                     LIMIT 1''')

    theLeastValue = dbCur.fetchall()

    dbCur.execute('''SELECT COUNT(howManyTrained)
                     FROM dictionary
                     WHERE howManyTrained = ?''',(theLeastValue[0][0],))

    howManyWordsOnThisLevel = dbCur.fetchall()
    randomNumber = randint(0, howManyWordsOnThisLevel[0][0] - 1)

    dbCur.execute('''SELECT eng, pl, type FROM dictionary
                     WHERE howManyTrained = ?''',(theLeastValue[0][0],))

    randomWord = dbCur.fetchall()
    
    return randomWord[randomNumber]

def getRandomExpression(dbCon, dbCur):
    dbCur.execute('''SELECT howManyRead FROM expressions
                     ORDER BY howManyRead ASC
                     LIMIT 1''')

    theLeastValue = dbCur.fetchall()

    dbCur.execute('''SELECT COUNT(howManyRead)
                     FROM expressions
                     WHERE howManyRead = ?''',(theLeastValue[0][0],))

    howManyExpressionsOnThisLevel = dbCur.fetchall()
    randomNumber = randint(0, howManyExpressionsOnThisLevel[0][0] - 1)

    dbCur.execute('''SELECT eng, comments FROM expressions
                     WHERE howManyRead = ?''',(theLeastValue[0][0],))
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

def getAllWords(dbCur):
    dbCur.execute('''SELECT eng, pl, type, howManyTrained FROM dictionary
                     ORDER BY eng ASC''')
    return dbCur.fetchall()

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

def resetAllCounters(dbCon, dbCur):
    try:
        dbCur.execute('''UPDATE dictionary
                        SET howManyTrained = 0''')
        dbCon.commit()
        print('All counters have been set to 0')
    except sqlite3.Error as e:
        print(f"There was an error during reseting words' counters: {e}")

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

def addExpression(dbCon, dbCur, expression, comment):
    try:
        dbCur.execute('''INSERT INTO expressions
                         VALUES (?, ?, '0')''',(expression,comment))
        dbCon.commit()
        print(f'The expression "{bcolors.OKGREEN}{expression}{bcolors.ENDC}" has been added successfully!')
    except sqlite3.Error as e:
        print(f'The error has occured: {e}')
    return