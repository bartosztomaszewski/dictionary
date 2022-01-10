from functions import *

def showMenu(dbCon, dbCur):
    tables = createClassesWithTables(dbCur)
    choice = ''
    print('Welcome to the self-made program, which helps you learn English words :)\nChoose one of the following options:')
    while choice != 'q':
        print('''1 - Add a new word
2 - Learning mode (pol -> eng)
3 - Learning mode (eng -> pol)
4 - Manage of all known words
5 - Reading mode
q - Exit the program''')
        choice = input("Your choice: ")
        match choice:
            case '1':
                addWord(dbCon,dbCur)
            case '2':
                learningModePlToEng(dbCon,dbCur)
            case '3':
                learningModeEngToPl(dbCon,dbCur)
            case '4':
                jsonFile = 'database\\words.json'
                nextChoice, words = administratingMode(dbCur)
                match nextChoice:
                    case '1':
                        nextChoice, editingWord = am_editWord(dbCon,dbCur)
                        match nextChoice:
                            case '1':
                                am_deleteWord(dbCon, dbCur, editingWord)
                            case '2':
                                am_setCounter(dbCon, dbCur, editingWord)
                            case '3':
                                am_makeCorrection(dbCon, dbCur, editingWord)
                            case _:
                                print("You didn't choose any of the available options.")
                    case '2':
                        resetAllWordsCounters(dbCon, dbCur)
                    case '3':
                        exportWordsToJson(jsonFile, words)
                    case '4':
                        importWordsFromJson(jsonFile, dbCon, dbCur)
                    case '5':
                        nextChoice = showNumberOfWordsPerLevel(dbCur)
                        match nextChoice:
                            case 'q':
                                cls()
                            case _:
                                showWordsOnChosenLevel(dbCur=dbCur, level=nextChoice)
            case '5':
                nextChoice = readingMode(dbCon,dbCur)
                match nextChoice:
                    case '1':
                        addExpression(dbCon, dbCur)
                    case '2':
                        readRandomExpression(dbCon, dbCur, tables)
                    case '3':
                        resetReadingCounters(dbCon, dbCur)
                    case _:
                        cls()
            case 'q':
                print("Bye!")
            case _:
                cls()
                print('Wrong option\n')
    return

if __name__ == '__main__':
    cls()
    databaseConnection = initializeDatabase("db_vocabularies")
    databaseCursor     = createDatabaseCursor(databaseConnection)
    showMenu(databaseConnection, databaseCursor)
    databaseConnection.close()