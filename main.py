from game import Person, bcolors
from magic import Spell
from inventory import Item 
import random
 
# Parameters for Person Class: (self, hp, mp, atk, df, magic)
 
# Create Black Magic 
# Parameters for Spell() class: name, cost, dmg, type
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")
 
# Create White Magic 
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")
 
# Create Some Items
# Parameters for Item() class: name, type, description, prop
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Full restores HP/MP of one party member", 9999)
megaelixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
 
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)
 
enemy_spells = [fire, meteor, curaga]
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, 
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5}, 
                {"item": megaelixer, "quantity": 2}, {"item": grenade, "quantity": 5}]
 
# Title Screen
#MAKE IT
 
# Character Creation
characterEntry = False
while characterEntry ==  False:
    char_name = input("Username (10 Character Maximum): ")
    if len(char_name) > 10:
        characterEntry = False
        char_name = input("More Than 10 Characters Entered, Please make your username (10 Character Maximum): ")
     
    elif char_name == "":
        characterEntry = False  
        char_name = input("Less Than 10 Characters Entered, Please make your username (10 Character Maximum): ")
     
    elif len(char_name) > 0 and len(char_name) < 10:
        characterEntry = True
 
    print("Username: = ", char_name)
 
# We are instantiating the Person() class twice to make a player and an enemy object 
# Parameters for Person Class: (self, name, hp, mp, atk, df, magic, items)
player1 = Person("Tiggerabcd:", 3460, 165, 300, 34, player_spells, player_items)
player2 = Person("Tiggerabcd:", 4460, 185, 311, 34, player_spells, player_items)
player3 = Person("Tiggerabcd:", 3460, 175, 288, 34, player_spells, player_items)
 
enemy1 = Person("Minion", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Ulfric", 11200, 265, 525, 25, enemy_spells, [])
enemy3 = Person("Minion", 1250, 130, 560, 325, enemy_spells, [])
 
enemies = [enemy1, enemy2, enemy3]
 
players = [player1, player2, player3]
 
# This calls the generate_damage() class to generate an attack
# print("Player generates damage with", player.generate_damage(), "atk pts")
# print("Player generates damage with", player.generate_damage(), "atk pts")
# print("Player generates damage with", player.generate_damage(), "atk pts")
 
# This calls the generate_spell_damage to generate a magic spell by giving a parameter index value for a specific spell in the 'magic' dictionary
# print("Player casts Fire spell for", player.generate_spell_damage(0), "atk pts")
# print("Player casts Thunder spell for", player.generate_spell_damage(1), "atk pts")
 
running = True
 
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
 
while running:
    print("===================")
    
    print("\n\n")
    
    print("NAME                HP                                 MP")
    
    for player in players:
        player.get_stats()
        
    print("\n")
    
    for enemy in enemies:
        enemy.get_enemy_stats()
    
    for player in players:
    
        player.choose_action()
        choice = input("    Choose Action:")
        # Index is a variable that takes the value of choice and subtracts it by 1 to give the program the correct index value for each of the lists
        # This is because computers start counting lists from position "0"
        index = int(choice) - 1 
        
        # print("You chose", player.get_spell_name(int(index)))
        
        if index == 0:
            dmg = player.generate_damage()
        # This calls the choose_target() function in the Player class to choose an enemy in the available Enemy array 
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")
        # This checks to see if the enemy is dead, and if so, delete it from the enemies list 
        if enemies[enemy].get_hp() == 0:
            print(enemies[enemy].name.replace(" ", "") + " has died.")
            del enemies[enemy]
            
        elif index == 1:
            player.choose_magic()
        # This combined statement allows you to index into the correct magic spell choice since computers start counting from 0 onward
        
            magic_choice = int(input("Choose magic:"))-1
        
        # This allows you to go back into the previous menu with the use of the number choice, '0'
            if magic_choice == -1:
                continue
            
            # This indexes into the magic list based on the user's number choice
            spell = player.magic[magic_choice]
            # This calls the generate_damage() class from the magic class
            magic_dmg = spell.generate_damage()
            
            current_mp = player.get_mp()
            
            if spell.cost > current_mp:
                # \n: this creates a line break within a print statement in Python
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            
            # This reduces the player's mp based on the mp cost of the spell
            player.reduce_mp(spell.cost)
            
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                # This calls the choose_target() function in the Player class to choose an enemy in the available Enemy array 
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                
                # This checks to see if the enemy is dead, and if so, delete it from the enemies list 
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
        
        elif index == 2:
            player.choose_items()
        
            item_choice = int(input("Choose item: ")) - 1
            
            # This allows you to go back into the previous menu with the use of the number choice, '0'
            if item_choice == -1:
                continue
            
            item = player.items[item_choice]["item"]
            
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "No " + item.name + "s left..." + bcolors.ENDC)
                continue
            
            player.items[item_choice]["quantity"] -= 1
            
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp 
                        i.mp = i.maxmp 
                else:
                    player.hp = player.maxhp 
                    player.mp = player.maxmp 
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
                
            elif item.type == "attack":
                # This calls the choose_target() function in the Player class to choose an enemy in the available Enemy array 
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)
                # This checks to see if the enemy is dead, and if so, delete it from the enemies list 
                if enemies[enemy].get_hp() == 0:
                # The .replace() function strips a whitespace each time an enemy dies
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
            
    # Check if battle is over
        defeated_enemies = 0 
        defeated_players = 0 
    
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1 
    
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1 
    
    # Check if Player Won:
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
        
    # Check if Enemy Won:
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False
        
    print("\n")
    
    # Enemy Attack Phase:
    for enemy in enemies:       
        enemy_choice = random.randrange(0, 2)
        
        if enemy_choice == 0:
        # Enemy chooses player to attack 
            target = random.randrange(0, 3)
        # This allows the first enemey to start the attack 
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
        # The .replace() function replaces all spaces
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + " for", enemy_dmg)
        
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
        
        if spell.type == "white":
            enemy.heal(magic_dmg)
            print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + "for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == "black":
            # This calls the choose_target() function in the Player class to choose an enemy in the available Enemy array 
            target = random.randrange(0, 3)
            players[target].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)
            
            # This checks to see if the enemy is dead, and if so, delete it from the enemies list 
            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has died.")
                del players[player]
        # print("Enemy chose", spell, "damage is", magic_dmg)
