import os
import sqlite3
import os

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

if __name__ == '__main__':
    os.system('cls')
    databaseConnection = initializeDatabase("db_vocabularies")
    databaseCursor     = createDatabaseCursor(databaseConnection)

    databaseCursor.execute("SELECT * FROM expressions;")
    tablesInfo = databaseCursor.fetchall()
    print(tablesInfo)

    databaseConnection.close()