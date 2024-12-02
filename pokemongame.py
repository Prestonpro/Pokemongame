import random
import time
import csv

#stores pokemon.csv data to pokelist
with open('pokemon.csv','r') as pk:
        pokelist = pk.readlines()
        ct=0
        for lines in pokelist:
            pokelist[ct] = lines.split(',')
            ct+=1

def print_instruction():
    '''This function prints the instructions for the Pokemon game. There are no inputs for this function.
    The output of the function is printed to screen.'''
    print("Introduction: This is a 2 player pokemon-style game.")
    print("Playing the Game:")
    print("Each player chooses 1 pokemon to start the game.")
    print()
    print("For the first 5 turns(per player), both players will search for pokemon.")
    print("The player must guess an integer between 0-9 to determine whether the player's turn runs.")
    print("If the player's guess is in the list of 4 random numbers generated by the computer, the turn will run.")
    print()
    print("If the turn is run, the player will have a random amount of time to click on their keyboard.")
    print("If the player presses in time, a random pokemon will be added to the player's inventory.")
    print()
    print("Once Player 1's turn is finished, Player 2 will follow the same process.")
    print()
    print("After 10 total turns, players get to choose at the beginning of every turn between seeking battle and hunting pokemon.")
    print("If a player decides to seek battle, the same random integer guess process will determine whether he finds it.")   
    print("If the player guesses incorrectly, their turn will be over, and the next player's turn will begin")
    print("If the player guesses correctly, both players will be thrown into battle.")
    print("During battle, players can select 4 moves:")
    print("evade: dodges attack at 50 percent chance")
    print("block: reduces incoming damage by 60 percent")
    print("attack: deal 25 percent atk as damage")
    print("heavy attack: deal 50 percent atk as damage at a 50 percent chance")
    print("When a pokemon is killed, battle ends and turns continue normally with options for hunting pokemon or battling")
    print()
    print("You win by killing all the other player's pokemon")
    print()
    print("You can restart the game at any time by accessing pokemon_save_file.")
    


def run_turn(guess):
    '''This function will decide if the player's turn will run or not based on whether the user can guess a random number.'''
    '''The parameter is the user's numerical guess (integer). The return is a boolean.'''
    user_g = int(guess)
    ran_nums =  []
    rand_int = 0
    while len(ran_nums) < 3:
        rand_int = random.randint(0,9)
        if rand_int in ran_nums:
            pass
        else:
            ran_nums.append(rand_int)
    if user_g in ran_nums:
        run = True
    else:
        run = False
    return(run)

def hunt():
   '''The purpose of this function is to allow the players to hunt for pokemon. A random pokemon is generated and the player is asked to type the letter displayed in the terminal.
   The result is displayed to the terminal. If the player is successful a tuple with the pokemon's name, Attack, and HP is returned, so that it may be added to the players inventory.'''
   kb = 'abcdefghijklmnopqrstuvwxyz'
   randPoke = random.randint(1,801)
   print(f'A wild {pokelist[randPoke][1]} has appeared!')
   print('Type in the character prompted when it appears to catch the pokemon!')
   randkb = random.randint(1,25)
   time.sleep(random.randint(1,10))
   chara = input(f'Input {kb[randkb]} ')
   time.sleep(1)
   print('Time\'s up!')
   if chara == kb[randkb]:
       print(f'Congratulations! {pokelist[randPoke][1]} has now joined your party!')
       return pokelist[randPoke][1], pokelist[randPoke][5], pokelist[randPoke][6]
   elif chara in kb:
       print('Get good')
       return
   else:
       print('Are you even trying?')
       return

def addpokemon(hunt_return):
    '''Adds the pokemon returned from the hunt to a players dictonary of pokemon. Takes in a 3 argument tuple that is returned from hunt. 
    This tuple includes the  Pokemon's Name, Attack and HP. There is no return on this function but the pokemon is added to the players 1's inventory.'''
    try:
        player1_pokemon_list_dictionary[hunt_return[0]] = [float(hunt_return[1]),float(hunt_return[2])]
    except:
        return
    
def addpokemon2(hunt_return):
    '''Adds the pokemon returned from the hunt to a players dictonary of pokemon. Takes in a 3 argument tuple that is returned from hunt. 
    This tuple includes the  Pokemon's Name, Attack and HP. There is no return on this function but the pokemon is added to the players 2's inventory.'''
    try:
        player2_pokemon_list_dictionary[hunt_return[0]] = [float(hunt_return[1]),float(hunt_return[2])]
    except:
        return
    
def battle(thingy):
    ''' This is the Battle function that pits to players and their pokemon against each other. It takes in a tuple with the names of player 1 and player 2's choosen pokemon. 
    Edits the existing pokemon lists and the pokemon's stats. (The pokemon that wins levels up, +10 hp and atk) Doesn't return anything'''
    player1 = thingy[0]
    player2 = thingy[1]
    continuing = True
    valids = ['evade', 'block', 'attack', 'heavy attack']
    while continuing:
        #print statement with participant info
        print(f'Player 1: {player1}\nHP: {player1_pokemon_list_dictionary[player1][0]}\nATK: {player1_pokemon_list_dictionary[player1][1]}\n')
        print(f'Player 2: {player2}\nHP: {player2_pokemon_list_dictionary[player2][0]}\nATK: {player2_pokemon_list_dictionary[player2][1]}\n')
        move1 = input('What would player 1 like to do? (evade,block,attack,heavy attack)')
        while move1 not in valids:
            move1 = input(f'Invalid. Valids: {valids}')
        move2 = input('What would player 2 like to do? (evade, block, attack, heavy attack)')
        while move2 not in valids:
            move2 = input(f'Invalid. Valids: {valids}')
        print(f'\nPlayer 1 used {move1}')
        print(f'Player 2 used {move2}\n')
        if (move1 == 'block' or move1 == 'evade') and (move2 == 'block' or move2 == 'evade'):
            continue
        result1 = move(move1)
        result2 = move(move2)
        
        damage1 = 0
        damage2 = 0

        #calculating player 1 damage
        if move2 == 'attack':
            damage1 = float(player2_pokemon_list_dictionary[player2][1]) * 0.25
        if move2 == 'heavy attack' and result2:
            print('Player 2\'s heavy attack landed!')
            damage1 = float(player2_pokemon_list_dictionary[player2][1]) * 0.5
        if move2 == 'heavy attack' and result2 == False:
            print('Player 2\'s heavy attack missed!')
            damage1 = 0
        if move1 == 'evade' and result1 and damage1 != 0:
            print('Player 1\'s evade was successful!')
            damage1 = 0
        if move1 == 'evade' and result1 == False and damage1 != 0:
            print('Player 1\'s evade was unsuccessful!')
        if move1 == 'block' and damage1 != 0:
            damage1 = damage1*0.4
        #calculating player 2 damage
        if move1 == 'attack':
            damage2 = float(player1_pokemon_list_dictionary[player1][1]) * 0.25
        if move1 == 'heavy attack' and result1:
            print('Player 1\'s heavy attack landed!')
            damage2 = float(player1_pokemon_list_dictionary[player1][1]) * 0.5
        if move1 == 'heavy attack' and result1 == False:
            print('Player 1\'s heavy attack missed!')
            damage2 = 0
        if move2 == 'evade' and result2 and damage2 != 0:
            print('Player 2\'s evade was successful!')
            damage2 = 0
        if move2 == 'evade' and result2 == False and damage2 != 0:
            print('Player 2\'s evade was unsuccessful!')
        if move2 == 'block' and damage2 != 0:
            damage2 = damage2*0.4
            
        player1_pokemon_list_dictionary[player1][0] -= damage1
        player2_pokemon_list_dictionary[player2][0] -= damage2
        
        print(f'Player 1 took {damage1} damage')
        print(f'Player 2 took {damage2} damage')
        
        if player1_pokemon_list_dictionary[player1][0] <= 0:
            continuing = False
            print(f'{player1} fainted')
            del player1_pokemon_list_dictionary[player1]
            player2_pokemon_list_dictionary[player2][0] += 10
            player2_pokemon_list_dictionary[player2][1] += 10
            print(f'{player2} leveled up!')
            return 
        if player2_pokemon_list_dictionary[player2][0] <= 0:
            continuing = False
            print(f'{player2} fainted')
            del player2_pokemon_list_dictionary[player2]
            player1_pokemon_list_dictionary[player1][0] += 10
            player1_pokemon_list_dictionary[player1][1] += 10
            print(f'{player1} leveled up!')
            return
        
def move(action):
    '''determines whose move it is. Takes in the string of input from the user and then determines the reult of the move. ouputing a bullion. '''
    if action == 'evade':
        if random.randint(0,1) == 1:
            return True
        else:
            return False
    elif action == 'heavy attack':
        if random.randint(0,1) == 1:
            return True
        else:
            return False
    elif action == 'attack':
        return True
    elif action == 'block':
        return True
    else:
        return True

#POKEMON_LIST WILL BE A LIST
def generate_save_file(dictionary1, dictionary2):
    '''generates a save file that saves the user's level, and their pokemon. Takes in the player's dictionary of pokemon to write them onto a text file. No return.'''
    with open('pokemon_save_file', 'w') as file:
        file.write("Player 1 Captured Pokemon:\n")
        for pokemon in dictionary1:
            file.write(f'{pokemon},{dictionary1[pokemon][0]},{dictionary1[pokemon][1]}\n')
        file.write("Player 2 Captured Pokemon:\n")
        for pokemon in dictionary2:
            file.write(f'{pokemon},{dictionary2[pokemon][0]},{dictionary2[pokemon][1]}\n')

def import_save_file(file_name):
    '''imports the save file. Takes in the name of the file as an input argument, no output. Edits player pokemon lists directly'''
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line_index in range(len(lines)):
            if "Player 1 Captured Pokemon" in lines[line_index]:
                start_index_1 = line_index + 1
            if "Player 2 Captured Pokemon" in lines[line_index]:
                start_index_2 = line_index + 1 
        for line in lines[start_index_1:(start_index_2-1)]:
            line = line.strip()
            pokemon_list = line.split(',')
            current_list = []
            current_list.append(float(pokemon_list[1]))
            current_list.append(float(pokemon_list[2]))
            player1_pokemon_list_dictionary[pokemon_list[0]] = current_list
        for line in lines[start_index_2:]:
            line = line.strip()
            pokemon_list = line.split(',')
            current_list = []
            current_list.append(float(pokemon_list[1]))
            current_list.append(float(pokemon_list[2]))
            player2_pokemon_list_dictionary[pokemon_list[0]] = current_list

player1_pokemon_list_dictionary = {}
player2_pokemon_list_dictionary = {}
player1_current_pokemon_list = []
player2_current_pokemon_list = []

def get_initial_pokemon():
    '''gets initial pokemon to add to the player's lists. No i/o arguments. Takes in user input and appends them directly to list'''
    valid_pokemon = ['Charmander', 'Squirtle', 'Bulbasaur', 'Pikachu']
    pick = input('Player 1, pick Charmander, Squirtle, Bulbasaur, or Pikachu: ')
    while pick not in valid_pokemon:
        pick = input('choose again. You can only pick Charmander, Squirtle, Bulbasaur, or Pikachu: ')
    with open('pokemon.csv','r') as pokemon_file:
        sheet_reader = csv.DictReader(pokemon_file)
        for row in sheet_reader:
            if row['Name'] == pick:
                for column in row:
                    try:
                        row[column] = float(row[column])
                    except ValueError or TypeError:
                        continue
                player1_current_pokemon_list.append(row['HP'])
                player1_current_pokemon_list.append(row['Attack'])
                player1_pokemon_list_dictionary[row['Name']] = player1_current_pokemon_list
    pick = input('Player 2, pick Charmander, Squirtle, Bulbasaur, or Pikachu: ')
    while pick not in valid_pokemon:
        pick = input('choose again. You can only pick Charmander, Squirtle, Bulbasaur, or Pikachu: ')
    with open('pokemon.csv','r') as pokemon_file:
        sheet_reader = csv.DictReader(pokemon_file)
        for row in sheet_reader:
            if row['Name'] == pick:
                for column in row:
                    try:
                        row[column] = float(row[column])
                    except ValueError or TypeError:
                        continue
                player2_current_pokemon_list.append(row['HP'])
                player2_current_pokemon_list.append(row['Attack'])
                player2_pokemon_list_dictionary[row['Name']] = player2_current_pokemon_list

def select_pokemon():
    '''selection function for the battle function. No input arguments, takes in user input and returns their selections (String) as a tuple'''
    print('Player 1, here are your current pokemon and their stats: ')
    for key in player1_pokemon_list_dictionary:
        print(f'{key}: {player1_pokemon_list_dictionary[key][0]} HP, {player1_pokemon_list_dictionary[key][1]} Attack')
    p1 = input('Pick a pokemon: ') 
    while p1 not in player1_pokemon_list_dictionary:
        p1 = input("Invalid, pick again: ")
    print('Player 2, here are your current pokemon and their stats: ')
    for key in player2_pokemon_list_dictionary:
        print(f'{key}: {player2_pokemon_list_dictionary[key][0]} HP, {player2_pokemon_list_dictionary[key][1]} Attack')
    p2 = input('Pick a pokemon: ')
    while p2 not in player2_pokemon_list_dictionary:
        p2 = input("Invalid, pick again: ")
    return p1,p2

##### MAIN CODE #####
gameEnd = False
print_instruction()
game_input = input('Would you like to restart a saved game? (Y/N): ')
while game_input.upper() not in 'YN':
    game_input = input('Please input a correct value Y or N:')

if game_input.upper() == 'N':
    new_game = True
elif game_input.upper() == 'Y':
    new_game = False
else:
    new_game = False

if new_game == False:
    import_save_file(input('Please enter the name of your saved game file: '))
else:
    get_initial_pokemon()
num = 0
turns = 0
while num != 'q':
    # Player 1 turn
    num = input('Player1: please input your guess of an integer 0-9 or q to quit: ')
    try: 
        if 0 <= int(num) <= 9:
            pass
    except:
        if num == 'q':
            break
        else: 
            num = input('Please input a correct value: ')
    if turns > 5:
        B_F = input('Would you like to look for pokemon or battle your opponent? (L/B): ')
        while B_F not in 'LB':
            B_F = input('Please enter a valid input L or B: ')
        if run_turn(num) == True:
            if B_F == 'B':
                battle(select_pokemon())
                if bool(player1_pokemon_list_dictionary) == False:
                    print('Player 2 Wins!')
                    gameEnd = True
                    break
                if bool(player2_pokemon_list_dictionary) == False:
                    print('Player 1 Wins!')
                    gameEnd = True
                    break
            else:
                addpokemon(hunt())
        else:
            print("You guessed incorrectly, Player 2's turn")
            
    else:   #if turns <= 5
        if run_turn(num) == True:
            addpokemon(hunt())
        else:
            print("You guessed incorrectly, Player 2's turns")
    
    #Player 2 Turn, identical
    num = input('Player2: please input your guess of an integer 0-9 or q to quit: ')
    try: 
        if 0 <= int(num) <= 9:
            pass
    except:
        if num == 'q':
            break
        else: 
            num = input('Please input a correct value: ')
    if turns > 5:
        B_F = input('Would you like to look for pokemon or battle your opponent? (L/B): ')
        while B_F not in 'LB':
            B_F = input('Please enter a valid input L or B: ')
        if run_turn(num) == True:
            if B_F == 'B':
                battle(select_pokemon())
                if bool(player1_pokemon_list_dictionary) == False:
                    print('Player 2 Wins!')
                    gameEnd = True
                    break
                if bool(player2_pokemon_list_dictionary) == False:
                    print('Player 1 Wins!')
                    gameEnd = True
                    break
            else:
                addpokemon2(hunt())
        else:
            print("You guessed incorrectly, Player 1's turns")
            
    else:   #if turns <= 5
        if run_turn(num) == True:
            addpokemon2(hunt())
        else:
            print("You guessed incorrectly, Player 1's turns")
    
    #Ending Information
    print(f'You have run this many turns: {turns}')
    turns +=1
    
if gameEnd == False:
    save = input('Would you like to save the game file for later? (Y/N) ')
    while save.upper() not in 'YN':
        save = input('Please input a correct value Y or N:')
    if save == 'Y':
        generate_save_file(player1_pokemon_list_dictionary,player2_pokemon_list_dictionary)
