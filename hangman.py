#hangman.py needs "hang.txt" file to work properly
import random
import os
import time

UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
OKBLUE = '\033[94m'
FAIL = '\033[91m'
ENDC = '\033[0m'
capitols = ["Tirana","Andorra la Vella","Yerevan","Vienna","Baku","Minsk","Brussels","Sarajevo","Sofia","Zagreb","Nicosia","Prague","Copenhagen",
"Tallinn","Helsinki","Paris","Tbilisi","Berlin","Athens","Budapest","Reykjavik","Dublin","Rome","Astana","Pristina","Riga","Vaduz","Vilnius",
"Luxembourg","Skopje","Valletta","Chisinau","Monaco","Podgorica","Amsterdam","Oslo","Warsaw","Lisbon","Bucharest","Moscow","San Marino","Belgrade",
"Bratislava","Ljubljana","Madrid","Stockholm","Bern","Ankara","Kyiv","London","Vatican City"]
CAPITOLS_QUANTITY = len(capitols)


def import_pics():
    """import ascii graphics with hangman from text file and returns them as reversed list"""
    separator = "#"
    pics_list = []
    row = ""
    with open("hang.txt","r") as txt_file:
        for line in txt_file:
            row += line
            if line[0] == separator:
                row = row[:-2] #cut '#' from end of string
                pics_list.append(row)
                row = ""
    pics_list = pics_list[::-1]  #list reversing
    return pics_list


def pick_capitol():
    """Returns random capitol name and lenght of it"""
    capitol_nr = random.randint(0, CAPITOLS_QUANTITY-1)
    return (capitols[capitol_nr].upper(), len(capitols[capitol_nr]))


def init_dashes(dashes, capitol_len):
    """Fills initial list with dashes"""
    for i in range(0, capitol_len):
        dashes.append("-")
    return dashes


def show_game(dashes, bad_char_list,health, pics_list):
    """show hangman progression,hidden dashes list, health of player, 'not in word' list"""
    print("""
    ============
    Hangman Game
    ============
     """)
    print(FAIL+pics_list[health]+ENDC+"\n")
    for item in dashes:
        print(item, end=" ")
    print ("\n\nYour health: {:2d} \nList of wrong chars: {:12s}".format(health, repr(bad_char_list)))


def capitol_to_list_convert(picked_capitol, capitol_len):
    """Converts capitol name from string to list"""
    converted_to_list = []
    for i in range(0,capitol_len):
        converted_to_list.append(picked_capitol[i])
    return converted_to_list


def is_letter(letter):
    """Checks if given input is a letter"""
    if letter == None or len(letter)>1 or letter.upper() not in UPPER_LETTERS:
        return False
    else:
        return True


def timer(time_of_start):
    """Returns duration of game"""
    return time.time() - time_of_start


def cls():
    """Clears terminal"""
    os.system('cls' if os.name=='nt' else 'clear')


def main():
    dashes, health, bad_char_list = [], 5, []   #dashes - list with hidden chars ("-") (after good answer filled with visible chars)
    time_of_start = time.time()
    pics_list = import_pics()
    (picked_capitol, capitol_len) = pick_capitol()  #picking random capital
    picked_capitol_in_list = capitol_to_list_convert(picked_capitol, capitol_len)  #and convert it to list
    dashes = init_dashes(dashes, capitol_len)
    while not (dashes == picked_capitol_in_list or health<1):
        cls()
        show_game(dashes,bad_char_list,health, pics_list)
        print(picked_capitol)  #just for testing purpose (shows answer)
        question=input("\nWhat would you like to guess: \n1) a letter \n2) whole word(s)\n(type \"x\" to exit)\n\nYour answer: ")
        if question == "x":
            print("See you soon!")
            exit()
        elif question == "2":
            ask = input("Guess whole word(s): ").upper()
            if ask == picked_capitol:
                dashes=picked_capitol_in_list[:]
                continue
            else:
                health -= 1
                input("Your answer is incorrect\nEnter to continue")
        elif question == "1":
            ask = None
            while not is_letter(ask):
                ask = input("Guess a letter: ").upper()
            else:
                if ask not in picked_capitol:
                    health -= 1
                    if ask not in bad_char_list:
                        bad_char_list.append(ask)
                    else:
                        print("How many times you want to input char {} ?".format(ask))
                        input("Enter to continue...")
                    continue
                else:
                    for index, char in enumerate(picked_capitol_in_list):
                        if char == ask:
                            dashes[index]=char
    else:
        cls()
        show_game(picked_capitol_in_list,bad_char_list,health, pics_list)
        if health < 1:
            print(FAIL+"You loose!"+ENDC, end="")
            print(" ... such a waste {0:4.2f} sec. of your time...".format(timer(time_of_start)))
        else:
            print(OKBLUE+"Your answer is correct: {0}. You made it in {1:4.2f} sec.!".format(picked_capitol, timer(time_of_start)))
            print(ENDC)


if __name__ == "__main__":
    main()
