from functions import *

def showMenu(dbCon, dbCur):
    tables = createClassesWithTables(dbCur)
    choice = ''
    print('Welcome to the self-made program, which helps you learn English words :)\nChoose one of the following options:')
    while choice != 'q':
        print(f'1 - Add a new word\n2 - Learning mode (pol -> eng)\n3 - Learning mode (eng -> pol)\n4 - Manage of all known words\n5 - Reading mode\nq - Exit the program')
        choice = input("Your choice: ")
        match choice:
            case '1':
                addWord(dbCon,dbCur)
            case '2':
                learningModePlToEng(dbCon,dbCur)
            case '3':
                learningModeEngToPl(dbCon,dbCur)
            case '4':
                administratingMode(dbCon,dbCur)
            case '5':
                readingMode(dbCon,dbCur,tables)
            case 'q':
                print("Bye!")
            case _:
                os.system('cls')
                print('Wrong option\n')
    return

if __name__ == '__main__':
    os.system('cls')
    databaseConnection = initializeDatabase("db_vocabularies")
    databaseCursor     = createDatabaseCursor(databaseConnection)
    showMenu(databaseConnection, databaseCursor)
    databaseConnection.close()