import sqlite3

def addExpressionToDb(dbCon, dbCur, expression, comment):
    try:
        dbCur.execute('''INSERT INTO expressions
                         VALUES (?, ?, '0')''',(expression,comment))
        dbCon.commit()
        return True
    except sqlite3.Error as e:
        return e

def addWordToDb(dbCon,dbCur,wEng,wPl,wType):
    try:
        dbCur.execute('''INSERT INTO dictionary
                         VALUES (?, ?, ?, '0')''',(wEng,wPl,wType))
        dbCon.commit()
        return True
    except sqlite3.Error as e:
        return e

def changeWordInDb(dbCon, dbCur, eng, pl, wordType, editingWord):
    try:
        dbCur.execute('''UPDATE dictionary
                         SET eng = ?, pl = ?, type = ?
                         WHERE eng = ?''',(eng, pl, wordType, editingWord))
        dbCon.commit()
        return True
    except sqlite3.Error as e:
        return e

def createReadingTableInDb(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS expressions
                     (eng TEXT, comments TEXT, howManyRead INT)''')
    dbCon.commit()

def createDictionaryTableInDb(dbCon,dbCur):
    dbCur.execute('''CREATE TABLE IF NOT EXISTS dictionary
                     (eng TEXT PRIMARY KEY, pl TEXT, type TEXT, howManyTrained INT)''')
    dbCon.commit()

def deleteWordFromDb(dbCon, dbCur, word):
    dbCur.execute('''DELETE FROM dictionary
                     WHERE eng = ?''',(word,))
    dbCon.commit()

def getAllKindsOfLevelsFromDb(dbCur):
    dbCur.execute('''SELECT DISTINCT howManyTrained
                        FROM dictionary
                        ORDER BY howManyTrained ASC''')
    return dbCur.fetchall()

def getAllTablesInDb(dbCur):
    dbCur.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    return dbCur.fetchall()

def getAllWordsInDb(dbCur):
    dbCur.execute('''SELECT eng, pl, type, howManyTrained FROM dictionary
                     ORDER BY eng ASC''')
    return dbCur.fetchall()

def getAllWordsOnThatLevelInDb(dbCur, level):
    dbCur.execute('''SELECT eng, pl, type FROM dictionary
                     WHERE howManyTrained = ?
                     ORDER BY eng ASC''',(level,))
    return dbCur.fetchall()

def getAllExpressionsOnThatLevelInDb(dbCur, level):
    dbCur.execute('''SELECT eng, comments, howManyRead FROM expressions
                     WHERE howManyRead = ?''',(level,))
    return dbCur.fetchall()

def getNumberOfWordsInDb(dbCur):
    dbCur.execute('''SELECT COUNT(eng)
                     FROM dictionary''')
    return dbCur.fetchall()

def getNumberOfWordsOnThatLevelInDb(dbCur, level):
    dbCur.execute('''SELECT COUNT(eng)
                     FROM dictionary
                     WHERE howManyTrained = ?''',(level,))
    return dbCur.fetchall()

def getNumberOfRowsOnThatLevelInDb(dbCur, myTable, level):
    dbCur.execute(f'''SELECT COUNT({myTable.counterColumnName})
                    FROM {myTable.tableName}
                    WHERE {myTable.counterColumnName} = {level}''')
    return dbCur.fetchall()

def getTheSmallestCounterValueInDb(dbCur, myTable):
    dbCur.execute(f'''SELECT {myTable.counterColumnName} 
                      FROM {myTable.tableName} 
                      ORDER BY {myTable.counterColumnName} 
                      ASC LIMIT 1''')
    return dbCur.fetchall()

def importWordsFromJsonIntoDb(dbCon, dbCur, data):
    for word in data:
        dbCur.execute('''UPDATE dictionary
                SET pl = ?, type = ?, howManyTrained = ?
                WHERE eng = ?''',(word[1], word[2], word[3], word[0]))
    dbCon.commit()

def increaseExpressionCounterByOneInDb(dbCon, dbCur, expression):
    dbCur.execute('''UPDATE expressions
                     SET howManyRead = ? 
                     WHERE eng = ?''',(expression[2]+1, expression[0]))
    dbCon.commit()

def increaseWordCounterByOneInDb(dbCon,dbCur,word):
    dbCur.execute('''SELECT howManyTrained FROM dictionary
                     WHERE eng = ?
                     OR pl = ?''',(word, word))
    counter = dbCur.fetchall()
    dbCur.execute('''UPDATE dictionary
                     SET howManyTrained = ? 
                     WHERE eng = ?
                     OR pl = ?''',(counter[0][0] + 1, word, word))
    dbCon.commit()

def resetAllExpressionsCounterInDb(dbCon, dbCur):
    dbCur.execute('''UPDATE expressions
                        SET howManyRead = 0''')
    dbCon.commit()

def resetAllWordsCountersInDb(dbCon, dbCur):
    try:
        dbCur.execute('''UPDATE dictionary
                        SET howManyTrained = 0''')
        dbCon.commit()
        return True
        #print('All counters have been set to 0')
    except sqlite3.Error as e:
        return e
        #print(f"There was an error during reseting words' counters: {e}")

def setCounterInDb(dbCon, dbCur, word, counter):
    dbCur.execute('''UPDATE dictionary
                     SET howManyTrained = ? 
                     WHERE eng = ?
                     OR pl = ?''',(counter, word, word))
    dbCon.commit()
    dbCur.execute('''SELECT howManyTrained
                     FROM dictionary
                     WHERE eng = ?
                     OR pl = ?''',(word, word))
    return dbCur.fetchall()