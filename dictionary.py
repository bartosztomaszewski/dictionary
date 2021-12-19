from functions import *

def showMenu(dbCon, dbCur):
    choice = ''
    print('Welcome to the self-made program, which helps you learn English words :)\nChoose one of the following options:')
    while choice != 'q':
        print(f'1 - Add a new word\n2 - Learning mode (pol -> eng)\n3 - Learning mode (eng -> pol)\n4 - Manage of all known words\nq - Exit the program')
        choice = input("Your choice: ")
        match choice:
            case '1':
                createTable(dbCon,dbCur)
                try:
                    eng = input("English word: ")
                    if eng == "q" or eng == "":
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
                    print('The operation has been canceled')

            case '2':
                answer = None
                os.system('cls')
                while answer != 'q':
                    word = getRandomWord(dbCur)
                    print(f'Polish: {word[1]}')
                    answer = input("English: ")
                    if answer == word[0]:
                        print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
                        increaseWordCounter(dbCon,dbCur,answer)
                    else:
                        print(f"Wrong answer, the correct is: {word[0]}")
                os.system('cls')
            
            case '3':
                answer = None
                os.system('cls')
                while answer != 'q':
                    word = getRandomWord(dbCur)
                    print(f'English: {word[0]}')
                    answer = input("English: ")
                    if answer == word[1]:
                        print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
                        increaseWordCounter(dbCon,dbCur,answer)
                    else:
                        print(f"Wrong answer, the correct is: {word[1]}")
                os.system('cls')
            
            case '4':
                os.system('cls')
                words = getAllWords(dbCur)
                print("eng / pl / type / how many times it was trained\n")
                for word in words:
                    print(f'{word}')
                
                answer = input('\n1 - Select an English word you wanna edit\n2 - Reset all counters\nq - return to the main menu\n:')
                match answer:
                    case '1':
                        editingWord = input('Write an English word: ')
                        answer = input ("1 - Delete word\n2 - Set counter\n3 - Make a correction\nYour choice: ")         
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
                    case 'q':
                        os.system('cls')
    return

if __name__ == '__main__':
    os.system('cls')
    databaseConnection = initializeDatabase("db_vocabularies")
    databaseCursor     = createDatabaseCursor(databaseConnection)
    showMenu(databaseConnection, databaseCursor)
    databaseConnection.close()