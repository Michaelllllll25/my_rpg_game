# NOTES:
# This would normally be in a classes directory
# This would normally be called "game.py" if this were in a proper IDE
 
import random
 
from magic import Spell
 
import pprint
 
class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
   
class Person:
  def __init__(self, name, hp, mp, atk, df, magic, items):
    # Max HP value
    self.maxhp = hp
    # Current HP 
    self.hp = hp
    self.maxmp = mp
    self.mp = mp 
    # We set the low and high attack power +-10
    self.atkl = atk - 10
    self.atkh = atk + 10
    self.df = df
    # This will be a dictionary of magic spells and their MP cost 
    self.magic = magic
    self.items = items
    self.actions = ["Attack", "Magic", "Items"]
    self.name = name
   
  def generate_damage(self):
    return random.randrange(self.atkl, self.atkh)
       
  def take_damage(self, dmg):
    self.hp -= dmg
    if self.hp < 0:
      self.hp = 0 
    return self.hp 
   
   # These are utility classes to get HP and MP information to calculate remaining MP and HP points  
    
  def heal(self, dmg):
    self.hp += dmg
    # This makes sure you don't heal above your max hp 
    if self.hp > self.maxhp:
      self.hp = self.maxhp 
    
  def get_hp(self):
    return self.hp
     
  def get_max_hp(self):
    return self.maxhp 
   
  def get_mp(self):
    return self.mp 
     
  def get_max_mp(self):
    return self.maxmp 
   
  def reduce_mp(self, cost):
    self.mp -= cost
     
  def choose_action(self):
    i = 1 
    print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
    print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
    for item in self.actions:
      print("        " + str(i) + ".", item)
      i += 1 
   
  def choose_magic(self):
    i = 1 
     
    print("\n" + bcolors.OKBLUE + bcolors.BOLD + "     MAGIC:" + bcolors.ENDC)
    for spell in self.magic:
      print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
      i += 1
       
  def choose_items(self):
    i = 1 
     
    print("\n" + bcolors.OKGREEN + bcolors.BOLD + "     ITEMS:" + bcolors.ENDC)
     
    # This prints out the items available in the items dictionary:
    for item in self.items:
      print("        " + str(i) + ".", item["item"].name, ":", item["item"].description, " (x" + str(item["quantity"]) + ")")
      i += 1
       
  def choose_target(self, enemies):
    i = 1
     
    print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
     
    # This prints the enemies on screen, and then lets the player decide which enemy to attack
    for enemy in enemies:
      if enemy.get_hp() != 0:
        print("        " + str(i) + ".", enemy.name)
        i += 1 
    choice = int(input("    Choose target:")) - 1 
    return choice
       
  def get_enemy_stats(self):
    hp_bar = ""
    # Enemy HP bar will be 50 characters long
    bar_ticks = (self.hp / self.maxhp) * 100 / 2 
     
    while bar_ticks > 0:
      hp_bar += "█"
      bar_ticks -= 1
       
    while len(hp_bar) < 50:
      hp_bar += " "
       
    hp_string = str(self.hp) + "/" + str(self.maxhp)
    current_hp = ""
     
    # This makes sure that the enemy's hp bar is only 11 characters long
    if len(hp_string) < 11:
      decreased = 11 - len(hp_string)
       
      while decreased > 0:
        current_hp += " "
        decreased -= 1
       
      current_hp += hp_string
       
    else:
      current_hp = hp_string
       
    print("                    __________________________________________________")
    print(bcolors.BOLD + self.name  +  "|" +
          current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|")
       
  def get_stats(self):
     
    # Health Bar String
    hp_bar = ""
    hp_ticks = (self.hp / self.maxhp) * 100 / 4
     
    mp_bar = ""
    mp_ticks = (self.mp / self.maxmp) * 100 / 10
     
     
    while hp_ticks > 0:
      hp_bar += "█"
      hp_ticks -= 1
       
    while len(hp_bar) < 25:
      hp_bar += " "
     
    while mp_ticks > 0:
      mp_bar += "█"
      mp_ticks -= 1
       
    while len(mp_bar) < 10:
      mp_bar += " "
       
    hp_string = str(self.hp) + "/" + str(self.maxhp)
    current_hp = ""
     
    if len(hp_string) < 9:
      decreased = 9 - len(hp_string)
       
      while decreased > 0:
        current_hp += " "
        decreased -= 1
       
      current_hp += hp_string
       
    else:
      current_hp = hp_string
       
    mp_string = str(self.mp) + "/" + str(self.maxmp)
    current_mp = ""
     
    if len(mp_string) < 7:
      decreased = 7 - len(mp_string)
       
      while decreased > 0:
        current_mp += " "
        decreased -= 1 
       
      current_mp += mp_string 
     
    else:
      current_mp = mp_string
     
    print("                       _________________________          __________")
    print(bcolors.BOLD + self.name  +  "|" +
          current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|" +
          current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")
   
  def choose_enemy_spell (self):
    # This generates a random number based on the amount of spells available in the magic spell list
    magic_choice = random.randrange(0, len(self.magic)) 
    spell = self.magic[magic_choice]
    magic_dmg = spell.generate_damage()
       
    # This checks to see if the enemy still has MP remaining and then recalls the function recursively  
   
    pct = self.hp / self.maxhp * 100
     
    # If the enemy does not have any MP or if the enemy has over 50 HP, then they're not going to use white magic to cure themselves
    if self.mp < spell.cost or spell.type == "white" and pct > 50:
      spell, magic_dmg = self.choose_enemy_spell()
      return spell, magic_dmg
    else:
        return spell, magic_dmg
     