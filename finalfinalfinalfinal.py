from graphics import *
import time
import random
import sys
import pygame
from pygame.locals import *
import getpass
import decoding_game
import random
import hangman

locations = {}
stories = []
potPart = [0]#potential partners - how many spoken to
dead = ["no"]#must be a list.
badEndConditions = {"hasRock": "",
          "notMean":False,
                    "hasCandle":""
   }
class Story:
   "This an object which organizes all of the narratives that we can go through with this project.  We have two test stories currently, classic and castle."
   def __init__(self,name,printed_name,landing_point,description):
      self.name = name
      self.landing_point = landing_point
      self.description = description
      stories.append(self)

class Picture:
   """Image that isn't in a look"""
   def __init__(file):
      self.file = file
   def showPicture(self):
      print("Click x to continue") #instructions
      pygame.init()
      pygame.display.init() #initializes the window
      #screen = pygame.display.set_mode((500,500))
      test_room_pic = pygame.image.load(self.file) #loads the image, won't be able to find dimensions otherwise
      #finds width and height for the window
      WIDTH = test_room_pic.get_width() 
      HEIGHT = test_room_pic.get_height()
      screen = pygame.display.set_mode((WIDTH, HEIGHT)) #sets up the window
      screen.blit(test_room_pic, (WIDTH,HEIGHT)) # creates the window
      room_pic = pygame.image.load(self.file) # loads image to actual window
      screen.blit(pygame.transform.scale(room_pic, (WIDTH, HEIGHT)), (0,0)) #changes the window to fit the image
      pygame.display.flip() #updates the window
      while True:
          pygame.event.pump() #begins accepting new events
          event = pygame.event.wait() #waits for event
          if event.type == QUIT: #when pressing x
              pygame.display.iconify() #minimizes window-- otherwise doesn't fully close
              pygame.display.quit() #closes window
              break
##      pygame.init()
##      pygame.display.init()
##      screen = pygame.display.set_mode((500,500),HWSURFACE|DOUBLEBUF|RESIZABLE)
##      room_pic = pygame.image.load(self.file).convert_alpha()
##      screen.blit(pygame.transform.scale(room_pic, (500,500)), (0,0))
##      room_pic = pygame.image.load(self.file)
##      pygame.display.flip()
##      while True:
##          try:
##              #pygame.event.pump()
##              event = pygame.event.wait()
##              if event.type == QUIT:
##                  pygame.display.iconify()
##                  pygame.display.quit()
####          elif event.type==VIDEORESIZE:
####              screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
####              screen.blit(pygame.transform.scale(room_pic,event.dict['size']),(0,0))
####              pygame.display.flip()
##          except pygame.error:
##              pygame.display.iconify()
##              pygame.display.quit()
##              pass
        
              
      #WIDTH = pygame.surface.get_width()
      #win = GraphWin(self.name, 350, 350)
      #room_pic = Image(Point(175, 175), self.file)=
      #room_pic.draw(win)
##      try:
##         win.getMouse()
##         win.close()
##      except GraphicsError:
         #pass
      
class Ending:
   """this is an ending to the game."""
   #how to structure conditions of ending
   # if you're checking if an item is in the inventory, have an entry which is the item
   # if you're checking if a condition has been met, do [variable that is being checked]
   #this object needs to be initiated right when the ending check is happening
   #BUT - the conditions need to be a dictionary that's initiated at the beginning.
   #this dictionary is then checked at initiation.
   def __init__(self,conditions,text):
      self.conditions = conditions
      self.text = text
   def checkEnding(self,inventory):
      for key,check in self.conditions.items():
         if type(check) == bool:
            if check == True:
               pass
            else:
               return
         if type(check) == str and key[:3] == "has":
            inInventory = False
            for item in inventory.contents:
               if item.name == key[3:]:
                  inInventory = True
            if inInventory == True:
               pass
            else:
               return
      self.playEnding()
         
      
   def playEnding(self):
      for line in self.text:
         if type(line) == str:
            print(line)
            time.sleep(0.75)
         elif type(line) == Picture:
            line.showPicture()      
      dead[0] = "yes"
      pygame.mixer.music.stop()
      
#story mode.  this variable determines which story is being told
classic = Story("classic","A classic adventure","house","The original adventure in the game's code") #what mode of the story and where the player starts.
final = Story("final","starting the final","lectureHall","final starting")
current_story = final

def intro():
   """what plays at the beginning of the game"""
   pass
class Room:
   """Environment the player is located in.  Hosts commands."""
   def __init__(self,name,printed_name,description,commands):
      self.name = name
      self.printed_name = printed_name
      self.description = description
      self.commands = commands
      locations[str(name)] = self
   def printDesc(self):
      print(self.description)
      return self.description
   def printCommands(self):
      i = 0
      for value in self.commands:
        if value[1] == True:
           i +=1
           print(str(i)+".",value[0].name+".", value[0].description)
      print(str(i+1)+". Get help. Bring up short guide")
      print(str(i+2)+". Print your inventory.")
            
   def giveCommands(self):
        commands_per_room = self.commands
        return commands_per_room
class eventRoom(Room):
   """this is a room which prints a short series of text to the screen upon being entered for the first time"""
   def __init__(self,name,printed_name,description,commands,event,music):
        super().__init__(name,printed_name,description,commands)

        self.event = event#this is the event that happens.  it will be a list of different strings.
        self.visits = 0 #how many the players has visited the room.  this makes it so the event only plays the first time
        locations[str(name)] = self
        self.music = music
   def playEvent(self):
      if self.music == "":
         pass
      else:
         pygame.mixer.music.fadeout(10)
         pygame.mixer.music.load(self.music)
         pygame.mixer.music.play(-1)
      for text in self.event:
         print(text)
         time.sleep(0.75)
      print("\n")
      self.visits += 1
        
class roomCommand:
    """This is a command within a room. Kept despite not being used for the hierarchy of it"""
    def __init__(self,name,description):
        self.name = name
        self.description = description
    def giveName(self):
        return self.name
    def giveDescription(self):
        return self.description
        
class Exit(roomCommand):
    """This is a room command which provides the info for the player to move from one room to the other"""
    def __init__(self,name,description,from_room,to_room):
        self.name = name
        self.description = description
        self.from_room = from_room
        self.to_room = to_room
    def giveToRoom(self):
        return self.to_room
    def giveFromRoom(self):
        return self.from_room
    def openDoor(self):
        to_room = locations[self.to_room]
        from_room = locations[self.from_room]
        print("The way to the", to_room.printed_name,"has been opened.")
        for command in from_room.commands:
            if command[0] == self:
                if command[0] == self: #open these gates
                    command[1] = True
        
class NPC(roomCommand):
    """This is a room command class which has dialogue and talks to the user."""
    def __init__(self,name,description,dialogue):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.dialogue_count = 0
    def speak(self):
        print("\n")
        print(self.name.upper())
        print("""#################################################
              """)
        print(self.dialogue[self.dialogue_count % len(self.dialogue)])
        self.dialogue_count += 1
        print("""#################################################
              """)

class Celia(NPC):
   """This is the ghost!  She has special events and stages so she's a seperate class"""
   def __init__(self,name,description,dialogue):
      super().__init__(name,description,dialogue)
      self.dialogue_count = 0
      self.leaveLecture = Exit("Side door","The way out of the lecture hall","lectureHall","campus")
      self.bitOfStory = "MeetingFirst"
   def meetFirst(self,player,room):
      words = ["And so, you agreed to become partners with Celia.",
               "She seemed really nice once you got to know her.",
               "Not that you knew her that well after 5 minutes of talking after class.",
               "She'd been studying CS for years.",
               "And she lived in Sessions.",
               "There was something about her. . .",
               "Something that you just couldn't pin down."]
      for line in words:
         print(line)
         time.sleep(0.75)
      print("\n")
      room.commands.append([self.leaveLecture,True])
      
   def speak(self,player,room):
      super().speak()
      if self.bitOfStory == "MeetingFirst":
         self.meetFirst(player,room)
         self.bitOfStory == "MeetingSecond"
      
class Partner(NPC):
   """This is the potential partners class.  It inherits from NPC.  It exists so that you have to talk to all of the partners before being able to meet Celia"""
   def __init__(self,name,description,dialogue):
      super().__init__(name,description,dialogue)
      self.dialogue_count = 0
   def speak(self,room,celia):
      super().speak()
      if self.dialogue_count == 1:
        potPart[0] += 1
      if potPart[0] == 4 and [cel,True] not in room.commands:
         print("\nWait. . .")
         time.sleep(0.1)
         print("Someone else just showed up\n")
         room.commands.append([cel,True])
         
         
         
class doNPC(NPC):
   """a fetch npc that won't take your stuff.  They will do an action upon being talked to."""
   def __init__(self,name,description,dialogue,thanks_dialogue,action,item2give):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.thanks_dialogue = thanks_dialogue        
        self.dialogue_count = 0
        self.action = action #what the npc does upon being gifted the item
        self.stage = "notFulfilled" # determines if the object has been given or not
        self.item2give = item2give#the item the NPC gives
   def interact(self,inventory):
      if self.stage == "notFulfilled":
          print(self.name.upper())
          print("""#################################################
           """)
          print(self.dialogue)
          print("""#################################################
           """)
          self.processAction(inventory)
          self.stage = "Fulfilled"
          self.dialogue = self.thanks_dialogue
      elif self.stage == "Fulfilled":
          self.speak()
   def processAction(self,inventory):
            #if the task that the npc does upon having their quest being solved is opening up a location
       if self.action == "openDoor":
          self.Exit.openDoor()
       if self.action == "giveItem":
          print(self.name,"has a gift for you as thanks.")
          self.item2give.putIntoInventoryFromNPC(inventory)
          print("""
         """)

class fetchNPC(doNPC):
   """this npc is special because they will ask the player for an item in their initial dialogue
   ###and then will change their dialogue after an item is used to.
   #dialogue 1 = "I need this item"
   #thanks_dialogue = "thanks for giving me that item!"
   #dialogue 2 - "you're real cool."
   #they will also pass in a string which will be the command
   #that is processed by a function called Interact."""
   def __init__(self,name,description,dialogue,dialogue2,thanks_dialogue,action,item,stage,actionObject):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.dialogue2 = dialogue2
        self.thanks_dialogue = thanks_dialogue        
        self.dialogue_count = 0
        self.action = action #what the npc does upon being gifted the item
        self.Exit = Exit
        self.stage = stage # determines if the object has been given or not
        self.item = item #the item that the npc wants
        self.actionObject = actionObject
   def interact(self,inventory):
      if self.stage == "notFulfilled" and self.item not in inventory.contents:
         self.speak()
      if self.stage == "notFulfilled" and self.item in inventory.contents:
          self.speak()
          print("Give",self.name,"the",self.item.name+"?  Yes or No?")
          answer = getInput().strip().upper()
          if answer == "YES":
             print(self.name.upper())
             print("""#################################################
              """)
             print(self.thanks_dialogue)
             print("""#################################################
              """)
             self.processAction(inventory)
             self.stage = "Fulfilled"
             self.dialogue = self.dialogue2
          elif answer == "NO":
             print("Darn")
          else:
             print("Invalid input")
      elif self.stage == "Fulfilled":
          self.speak()
   def processAction(self,inventory):
        #if the task that the npc does upon having their quest being solved is opening up a location
        if self.action == "openDoor":
            self.actionObject.openDoor()
            self.item.takeFromInventory(inventory)
        if self.action == "giveItem":
            print(self.name,"has a gift for you as thanks.")
            self.actionObject.putIntoInventoryFromNPC(inventory)
            self.item.takeFromInventory(inventory)

            print("""
""")
        

class realRoomCommand(roomCommand):
   """miscellaneous thing that can be done, such as throwing a tomato"""
   def __init__(self,name,description,action):
      super().__init__(name,description)
      self.action = action
   def doTheThing(self,inventory,location):
      toDo = self.action[0] #this is the command to be done upon the thing.
      thing = self.action[1] #this is what the action is done upon.
      if toDo == "giveItem":
         print("You got a",thing+"!")
         thing.putIntoInventoryFromNPC(inventory)
      elif toDo == "openDoor":
         thing.openDoor()
      elif toDo == "endingCheck":
         thing.checkEnding()
      elif toDo == "changeConditionToTrue":
         dictionary = thing[0]
         key = thing[1]
         dictionary[key] = True
      elif toDo == "changeConditionToFalse":
         dictionary = thing[0]
         key = thing[1]
         dictionary[key] = False
      for command in location.commands:
         if command[0] == self:
            del command[0]

      
class smoothTalker(NPC):
   """An NPC with branching dialogue.  Can do things"""
   #structure for dialogue - tag, description/npc dialogue, and then options list w/ each option being ["text","which tag to jump to after this"]
   def __init__(self,name,description,dialogue):
      super().__init__(name,description,dialogue)
      self.stage = 0#this is which dialogue the pc is on.
      self.tags = []#these are the dialogue tags
      self.player_input = ""
   def speak(self,inventory):
      if self.stage != "End":
         self.tags = []
         self.results = {}
         print(self.name.upper())
         print("""#################################################
                 """)    
         print(self.dialogue[str(self.stage)][0])
         print("""#################################################
                 """)
         self.options = self.dialogue[str(self.stage)][1]
         i = 0
         for choice in self.options:
            print(str(i+1)+".",choice[0])
            i += 1
            self.tags.append(choice[1])
            try:
               self.results[i] = choice[2]
            except IndexError:
               pass
         print(str(i+1)+". Stop talking to",self.name)
         try:
            player_input = int(getInput())
            self.player_input = player_input
         except ValueError:
            print(self.name,"wasn't able to understand you.")
            return
         if player_input-1 > len(self.tags):
            print(self.name,"wasn't able to understand you.")
            return
         elif player_input-1 == len(self.tags):
            print("You can always talk again later!")
            return
         else:
            self.stage = self.tags[player_input-1]
            if self.stage == "End":
               print("Looks like",self.name,"doesn't have that much more to say.")
            else:
               try:
                  action = self.results[player_input]
                  self.doAction(action,inventory)
                  
               except KeyError:
                  pass
               self.speak(inventory)
      else:
         print(self.name,"has told you just about everything.")
      
   def wipe(self):
      self.stage = "0"
   def doAction(self,action,inventory):
      toDo = action[0] #this is the command to be done upon the thing.
      thing = action[1] #this is what the action is done upon.
      if toDo == "giveItem":
         print(self.name,"gave you the",thing)
         thing.putIntoInventoryFromNPC(inventory)
      elif toDo == "openDoor":
         thing.openDoor()
      elif toDo == "endingCheck":
         thing.checkEnding()
      elif toDo == "changeConditionToTrue":
         dictionary = thing[0]
         key = thing[1]
         dictionary[key] = True
      elif toDo == "changeConditionToFalse":
         dictionary = thing[0]
         key = thing[1]
         dictionary[key] = False



class Book(roomCommand):
   """A readable file.  Good for lore."""
   def __init__(self,name,description,file):
      super().__init__(name,description)
      self.file = file
   def read(self):
      file = open(self.file,"r")
      text = file.read()
      text = text.split("\n")
      for line in text:
         print(text)



class Look(Picture):
    """This command opens up a window with an image."""
    def __init__(self, name, description, file):
        self.name = name
        self.description = description
        self.file = file
    def showImage(self):
        super().showPicture()
class Inventory:
    """This is the list that holds the items and the special methods for it yo.  Could have been a function
but I preferred keeping everything as classes."""
    def __init__(self,contents, combos):
        self.contents = []
    def printItems(self):
        print("\nThese are all of the items in your inventory\n")
        if len(self.contents) > 0:
           print("#"*80)
           i = 0
           for value in self.contents:
               if value.shown == True:
                   i +=1
                   print(str(i)+".",value.name+".",value.description)
           print("#"*80)
                   
        if len(self.contents) == 0:
            print("There are no items in your inventory")
        print("\n")


    def alchemy(self):
        checkingdevicethingy = self.contents[1] #to prevent alchemy from running if there aren't two objects
        alchemy_info = print("Enter the numbers of two items you wish to combine separated by spaces.")
        combo_input = input("What would you like to combine?: ")
        combo_input = combo_input.split()
        choice1 = int(combo_input[0]) - 1 # gives the equivalent place within the list
        choice2 = int(combo_input[1]) - 1
        if (choice1 >= choice2): # switches the order so the order of deleting doesn't get affected
            choice1, choice2 = choice2, choice1
        inventory_list = self.contents
        element1 = str(inventory_list[choice1]) # turns it into a string for easy matching
        element2 = str(inventory_list[choice2])
        print("You selected: " + element1 + ", " + element2)
        # these are the predecided combinations, the player can only combine the pairs in here to get something new
        pair_counter = 0
        for pair in comboDict.keys():
            pair_counter += 1
            if (element1+element2) in pair:
                #print(comboDict.values())
                del inventory_list[choice1]
                inventory_list.insert(choice1, "placeholder")
                del inventory_list[choice2]
                del inventory_list[choice1]
                inventory_list.append(comboDict.get(pair))
                print("you created a new item!")
                break
            else:
                print("you can't combine these items!")
                break
                
class Combos(Inventory):
   """combine items"""
   def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2
   def comboCreator(self):
        return (self.part1+self.part2, self.part2+self.part1)

class Item:
   """an object which can be put into an inventory"""
   def __init__(self,name,description,shown):
        self.name = name
        self.description = description
        self.shown = shown
    # makes the item show up as its name when printed
   def __str__(self):
            return '{self.name}'.format(self=self)
   def printItem():
        print("Item name:",self.name+". Item description",self.description)
   def putIntoInventory(self,room,inventory):
        if type(self) == Key:
            self.newCommand()
        inventory.contents.append(self)
        inventory_counter = 0
        for item in room.commands:
            inventory_counter +=1
            if item[0].name == self.name:
                del room.commands[inventory_counter-1]
                if type(item) == Key:
                    item.newCommand
                break
        print("You put the",self.name,"into your inventory.")
   def putIntoInventoryFromNPC(self,inventory):
        if type(self) == Key:
            try:
               self.newCommand()
            except KeyError:
               inventory.contents.remove(self)
               pass
        if self in inventory.contents:
           pass
        else:
           inventory.contents.append(self)
        print("You put the",self.name,"into your inventory.")
        
   def takeFromInventory(self,inventory):
        taking_counter = 0
        for thing in inventory.contents:
            taking_counter +=1
            if thing.name == self.name:
                del inventory.contents[taking_counter-1]
                break

class MiniGame:
   def __init__(self, name, description, gamefile, prize):
      self.name = name
      self.description = description
      self.gamefile = gamefile
      self.prize = prize
   def playGame(self):
      self.gamefile.main()
   def getPrize(self, inventory):
       self.prize.putIntoInventoryFromNPC(inventory)
       print("yee haw")

    
class Key(Item):
   """An object which can open up a location"""
   def __init__(self,name,description,shown,room,command):
        self.name = name
        self.description = description
        self.shown = shown
        self.room = room
        self.command = command
   def useKey(self,inventory,Exit_here,room):
        #change command of if a location is shown from False to True
        #remove item from inventory
        #change descriptor of room.
        #self.command[1] = True #the command here is the command to open the next room.
        item_index = inventory.contents.index(self)
        del inventory.contents[item_index]
        from_room = locations[Exit_here.from_room]
        print("You have used the",self.name)
        self.command.openDoor()
        for action in from_room.commands:
            if action[0] == self: #
                from_room.commands.remove(action)                

   def newCommand(self): #room is the room where it can be used.  the command is for it to open the door.
        self.room = locations[self.room]
        for value in self.room.commands:
            if value[0] == self:
                value[1] = True
                break
   def returnRoom(self):
        self.room = locations[self.room]
        return self.room
#supporting the user making choices
class Option:
   """Options for a choice menu"""
   def __init__(self,name,description,result,choice):
       self.name = name
       self.description = description
       self.result = result
       #choice.optionsList.append([self,False])  #the boolean is for determining if the user has picked this option yet  
class Choice:
   """A choice menu - allows the player to choose something.  Must be optimized or deleted.  Undecided atm"""
   def __init__(self,name,description):
        self.name = name
        self.description = description
        self.optionsList = []
   def makeChoice(self):
        print(self.description)
        i = 0
        for option in self.optionsList:
            boolean = option[1]
            option = option[0]
            print(str(i+1)+".",option.name+".",option.description)
            i += 1
        print(str(i+1)+".","Return to this choice later.")
        try:
            player_input = getInput()
            player_input = int(player_input)
            print(type(player_input))
            print(player_input)
            print("that")
            try:
                print(player_input)
                if player_input <= (len(self.optionsList)+1):
                    print(player_input-1)
                    option = self.optionsList[player_input-1]
                    result = self.optionsList[player_input-1].result
                    i = 0
                    for result in self.optionsList:
                       print(i)
                       print(result.name)
                       print(player_input)
                       print("#"*60)
                    whatToDo(result)
                elif player_input == (len(self.optionsList)+2):
                    print(player_input-1)
                    processInput()
            except IndexError:
                print("Please only enter numerals within the choices presented")
                self.makeChoice()
        except ValueError:
            print("Please only enter numerals")
            self.makeChoice()
        option = [option,boolean]
        return option
    

class Person:
   """This is a class with the ability to go from one place to the other.  The player is one of these.  Literally
   #all it can do is move from one room to the other, lol."""
   def __init__(self,name,location):
        self.name = getpass.getuser()
        self.location = location
   def moveSelf(self,from_room,to_room):
         self.location = locations[to_room]
         print("You moved to "+ self.location.printed_name)

         if type(self.location) == eventRoom and self.location.visits == 0:
            self.location.playEvent()
         return self.location

if current_story.name == "classic": #which story is being initialized.
#THIS IS LOOKING AROUND
    look_laboratory = Look("Look in the laboratory","There are strange beeping noises and nuclear fallout symbols everywhere.", "lab.gif")
    look_house = Look("Look in the house","McLoving this architecture", "house.gif")
    look_basement = Look("Look around the basement","It's damp and dingy.", "basement.gif")
    look_secret_room = Look("Look around","Actually, you should probably pass on that.  It seems scary", "secretroom.gif")
    look_outside = Look("Look outside","I mean there's stuff here but who cares?", "outside.gif")
    look_garage = Look("Look in the garage","All I can see is old tools dad promised himself that he'd use.", "garage.gif")

    #THIS IS THE PLAYER'S INVENTORY
    player_inventory = Inventory([], {})

    #THESE ARE EXITS
    stairs = Exit("Stairs","These are stairs that go downwards","house","basement")
    upstairs = Exit("Upstairs","Go up the stairs","basement","house")
    side_tunnel = Exit("A side tunnel?","Go through the side tunnel","basement","secret_room")
    side_tunnel_back = Exit("Go back","Time to leave the sights behind","secret_room","basement")
    go_outside = Exit("Is that a door outside?","leave through the door outside","house","outside")
    go_inside = Exit("Well, that was lame","go back inside","outside","house")
    enter_garage = Exit("The garage","Looks like the door to the garage","outside","garage")
    exit_garage = Exit("Leave the garage","Leave the garage since it was boring","garage","outside")
    enter_lab = Exit("Enter the lab","Looks like there's another room off the side","secret_room","laboratory")
    leave_lab = Exit("Leave the lab","You've seen about all there is to see","laboratory","secret_room")
    tunnel = Exit("Go through the tunnel","You're curious what's up this tunnel","laboratory","garage")
    back_tunnel = Exit("Back through tunnel","Well, you figured that out","garage","laboratory")

    #THIS IS A FEW ITEMS
    greenCube = Item("Green Cube","A 7 inch by 7 inch, lime green cube.",True)
    russianTrinket = Item("Russian Trinket","Some creepy doll with cyrillic writing on it",True)
    rock = Item("Rock","Isn't that a great rock",True)
    endingTest = Item("Ending Test", "end tester", True)

    #COMBO ITEMS
    greenTrinket = Item("Green Trinket", "The combo of russian trinket and green cube", True)
    russianRock = Item("Russian Rock", "russian trinket + rock", True)

    #COMBO CREATIONS
    GTCombo = Combos("Green Cube", "Russian Trinket")
    greenTrinketCombo = GTCombo.comboCreator()
    RRCombo = Combos("Russian Trinket", "Rock")
    russianRockCombo = RRCombo.comboCreator()
    comboDict = {greenTrinketCombo: greenTrinket, russianRockCombo: russianRock}

    #THESE ARE KEYS

    garage_key = Key("Garage Key","This is the key that will let you into dad's garage",True,"outside",enter_garage)

    #THESE ARE NPCS
    uncle_joe = NPC("Uncle Joe","Is that Uncle Joe?",["I'm busy in here.","Didn't you hear me?"])
    mom = NPC("Mom","She's holding a platter of cookies",["Do you want some cookies?","I made them just for you"])
    dad = NPC("Dad","He's looking forelornly at the lawn mower",["Your mother told me to fix this","I don't have any idea how"])
    rat = NPC("A Rat","Looks like the mouse trap didn't work.",["Squeak!","Squeeeeak!"])
    vlad = fetchNPC("Definitely not Vlad","A man sitting in front of a computer - seems valid",["I need a green cube","I think that's absolutely valid"],["Wow, you're so nice for helping out","This is a very good cube.  Not nuclear"],"Thank you for the cube","giveItem","notFulfilled",greenCube,rock)



    
    #THESE ARE ROOMS
    garage = Room("garage","The garage","Filled with all of dad's used to be projects",[[look_garage,True],
                                                                                        [exit_garage,True],
                                                                                        [rat,True]])
                                                                                        
                                                                                        
    secret_room = Room("secret_room","A secret room","Huh, this is just an old, secret room",[[look_secret_room,True],
                                                                                              [side_tunnel_back,True],
                                                                                              [uncle_joe,True],
                                                                                              [russianTrinket,True],
                                                                                              [garage_key,True],
                                                                                              [enter_lab,True]])
    house = Room("house","An Upper Middle Class Travesty","This is a house",[[look_house,True],
                                                                             [stairs,True],
                                                                             [go_outside,True],
                                                                             [mom,True],
                                                                             [greenCube,True]])

    basement = Room("basement","Smells like forgotten baby toys","This is a basement",[[look_basement,True],
                                                                               [upstairs,True],
                                                                               [side_tunnel,True]])

    outside = eventRoom("outside","Ew, what is this place","Is this outside???",[[look_outside,True],
                                                                            [go_inside,True],
                                                                            [dad,True],
                                                                            [endingTest, True],
                                                                            [garage_key,False],
                                                                            [enter_garage,False]],["You look around","This is outside","What else would it be?"])
    laboratory = Room("laboratory","A Secret Laboratory","This place seems a little sketchy.  There's writing everywhere",[[look_laboratory,True],
                                                                                                                           [leave_lab,True],
                                                                                                                           [vlad,True]])
                                                                                                                               
elif current_story.name == "final": #final story.  The one that will actually be played.
   def intro():
       print("""
   _____                   _             _____           _ _   _     
  / ____|                 | |           / ____|         (_) | | |    
 | (___  _ __   ___   ___ | | ___   _  | (___  _ __ ___  _| |_| |__  
  \___ \| '_ \ / _ \ / _ \| |/ / | | |  \___ \| '_ ` _ \| | __| '_ " 
  ____) | |_) | (_) | (_) |   <| |_| |  ____) | | | | | | | |_| | | |
 |_____/| .__; \___; \___;|_|\_|\__  | |_____;|_| |_| |_|_|___|_| |_|
        | |                      __; |                               
        |_|                     |___;                                
""")
       time.sleep(1)
       text = ["You're in your computer science class's lecture hall.",
               "The professor has just assigned a group project for the end of the semester",
               "Unfortunately for you, you don't know anyone in the class. that well",
               "It's time for you to look around for a partner.",
               "Make sure you find someone good!",
               "After all. . .",
               "You'd rather die than fail"]
       for line in text:
          print(line)
          time.sleep(1)
       print("\n"*2+"#"*60,"\n"*2)
       time.sleep(1)
   #LOOKING AROUND
   lookParlor = Look("Take a look around the parlor","You feel like this isn't what Sessions really looks like","parlor.gif")
   lookCampusCenter = Look("Check out the campus center","It's bustling with people, orgs, and activity.","campuscenter.gif")
   lookGillett = Look("Look around Gillett","Look around the best house on campus","gillett.gif")
   lookLectureHall = Look("Look around your lecture hall","It's on the second floor of Ford","fordhall.gif")

   #PLAYER'S INVENTORY
   player_inventory = Inventory([], {})
   #EXITS
   toCampusCenter = Exit("The campus center","The way into the campus center","campus","campusCenter")
   fromCampusCenterToCampus = Exit("The glass doors","A way back onto campus","campusCenter","campus")
   toResourceRoom = Exit("The resource room","Go into the resource room","campusCenter","resourceRoom")
   fromResourceRoom = Exit("Back to the campus center","The way back to the campus center","resourceRoom","campusCenter")
   toBookStore = Exit("Into the bookstore","Go into the bookstore to buy things","campusCenter","bookStore")
   fromBookStore = Exit("Out of the bookstore","Leave into the campus center","bookStore","campusCenter")
   toElmStreet = Exit("Onto Elm Street","The way onto Elm Street","campusCenter","elmStreet")
   toGillett = Exit("The way into Gillett House","The best house on campus","elmStreet","gillett")
   toSessionsHall = Exit("The door into Sessions","The paint is peeling","outsideSessions","sessionsHall")
   toOutsideSessions = Exit("Walk to the outside of Sessions","You can head to the outside of sessions","elmStreet","outsideSessions")
   toGillDine = Exit("The way into Gillett Dining","Are you sure you want to enter a dining hall that crowded?","gillett","gillDine")
   toSessionsParlor = Exit("The Parlor","You can see a parlor full of chintzy decorations","sessionsHall","sessionsParlor")
   toSessionsAnnex = Exit("Sessions Annex", "A strange smell is coming from here", "sessionsHall", "sessionsAnnex")
   faint = Exit("Faint", "The strange smell has knocked you out", "sessionsAnnex", "sessionsBasement")
   toCarrollRoom = Exit("The Carroll Room", "They have events here", "campusCenter", "carrollRoom")
   
   #ITEMS
   orb = Item("Orb", "It looks cloudy inside", True)
   cutePoem = Item("Cute poem","A poem about art, love, and flowers Allison wrote on the card that you made",True)
   
   #COMBINABLE ITEMS
   markers = Item("Markers","A handful of felt tip markers",True)
   paper = Item("Construction paper","Some blue and white construction paper",True)
   rock = Item("Rock","A rock",True)
   tomato = Item("Tomato", "Marinara sauce, salsa, ketchup, the pomodoribilities are endless!", True)

   #COMBO ITEMS
   card = Item("Handmade card","Allison asked you to make this",True)
   etchedPoem = Item("Pure pumice poetry","Show Allison your enduring love and friendship by etching her poem onto this rock",True)
   #COMBO CREATIONS
   markersPaper = Combos("Markers", "Construction paper")
   cardCombo = markersPaper.comboCreator()
   poemRock = Combos("Cute poem", "Rock")
   prockCombo = poemRock.comboCreator()
   comboDict = {cardCombo: card, prockCombo: etchedPoem}
    
   #KEYS
   #garage_key = Key("Garage Key","This is the key that will let you into dad's garage",True,"outside",enter_garage)
   oneCard = Key("One Card","This wonderful key isn't yours, but you lost yours ages ago",True,"gillett",toGillDine)
   paperSlip = Key("A Slip of Paper", "It says 'I do what I want'", True, "campusCenter", toCarrollRoom)
   candle = Key("An electric candle", "It has batteries, so you can use it", True,"campus", toSessionsHall)
   #Celia
   cel = Celia("Celia","You've never met her before",["You want to be my partner, "+getpass.getuser()+"?","I'd really love that.",
                                                      "We must have met before because that's how I remember your name",
                                                      "If you're ok with it","No one's ever asked me before"])
 
   #NPCS
   professor = NPC("Professor Harmen","Your computer science professor.",["Are you looking for a partner?",
                                                                          "I'm sure that you'll find one easily."])

   #PARTNERS
   mariya = Partner("Mariya","You think that you take sociology with her",["I already have a partner, sorry"])
   sam = Partner("Sam","He's definitely in your math class. He seems to get everything easily, ugh",["I'm Ellen's partner","She's a great programmer"])
   janet = Partner("Janet","You don't really know her but she looks cool",["I'm thinking about dropping this class so we shouldn't partner up"])
   kaitlin = Partner("Kaitlin","You're friends on facebook you think",["Oh. . . hey(She doesn't seem too enthused)","(time to gracefully duck out)"])
   
   #DO NPCS
   
   allan = smoothTalker("Allan","A cheerful housekeeper",{"0":["Say hi to Allan",[["Hi!  I love rocks!","Cool",["giveItem",rock]],["Hello!","Bros",["changeConditionToTrue",[badEndConditions,"notMean"]]]]],
                                                   "Cool":["He thinks you're cool because he also loves rocks",[["Awesome!","End"],["Sweet!","End"]]],
                                                "Bros":["You guys are bros now",[["Wow!","End"],["Yay!","End"]]]})


   carl = doNPC("Carl", "He's j chillin", "Howdy Partner", "Don't spend it all in one place now...", "giveItem", tomato)
#
   #FETCH NPCS
   #persephoneGive = fetchNPC("Give Persephone the tomato","She looks like she needs it.", "I'm so hungry...", "I haven't seen anything so delicious in a long time", "Thank you so much, it tastes delicious", "openDoor", tomato, "notFulfilled",toCampusCenter)

   allison = fetchNPC("Allison","Your best friend since orientation",["I haven't seen you in awhile","By the way, could you get me a card from the resource room?"],["By the way, your partner's name is Celia?","I've never heard of her. . ."],"Oh my god this is so cute!","giveItem",card,"notFulfilled",cutePoem)

   #SMOOTH TALKERS
   #persephoneTalk = smoothTalker("Persephone", "She looks a lot like Celia but a lot more...solid? If that even is the right word.",{"0":["I haven't seen another person in quite some time...",[["Who are you?","Who"],["What do you mean 'quite some time'?","What"]]],
                                                                                                                                 #"Who":["I'm Persephone, and I was turned into a ghost...",["Oh my god..., are you Celia??", "Ghost"]],
                                                                                                                                 #"What":["I have no sense of time anymore... I was turned into a ghost...",["It makes sense now! You're Celia!","Ghost"]],
                                                                                                                                 #"Ghost":["Yes unfortunately...And I'm so hungry...",["This is so crazy","End"]]})

   sophia = smoothTalker("Sophia","A girl with dark bags around her eyes",{"0":["Are you trying to get into Sessions?",[["Yeah my partner for a project is in there","partner",["openDoor",toSessionsHall]],["Um, if that's ok","timid",["openDoor",toSessionsHall]]]],
                                                                           "partner":["What's her name",[["Celia","truth"],["Mary","lie"]]],
                                                                           "timid":["Why wouldn't it be?",[["Oh, no reason at all","enter"],["I'm not from this house","enter"]]],
                                                                           "truth":["That's. . . I hate to say this, but are you sure someone isn't messing with you?",[["I'm sure","sure"],["Huh, maybe they are","unsure"]]],
                                                                           "lie":["Huh, I must not know her",[["She's a first year","enter"]]],
                                                                           "enter":["Alright then...",[["Yup...","Goodbye"]]],
                                                                           "sure":["Well. . . um, if you're sure then",[["I guess that I'll head in now","Goodbye"]]],
                                                                           "unsure":["You know, maybe I heard her wrong",[["I guess that I'll head in now","Goodbye"]]],
                                                                           "Goodbye":["Well, wonderful talking to you!",[["Nice talking to you!","End"]]]})


   esther = smoothTalker("Esther","A girl with perfectly coiffed hair and an A cut dress covered in roses",{"0":["Whose guest are you?",[["I'm visiting Celia?","Celia"]]],
                                                                                                            "Celia":["She ought to know not to bring your kind here",[["I'm not sure what you mean by 'my kind'","exp"],["That's incredibly rude of you to say","confront"]]],
                                                                                                            "exp":["Your kind. . .(She wrinkles her nose).  You stink of blood",[["...(You can't think of a response)","noResponse"],["We all have blood","blood"]]],
                                                                                                            "confront":["Oh don't get in a tizzy about it.  I'm sure you can't help your condition",[["And what condition is that exactly?","mortal"],["I'm perfectly fine with how I am","proud"]]],
                                                                                                            "noResponse":["Classless, aren't you.  It's a shame how they're letting this college fall apart",[["No response","End"]]],
                                                                                                            "blood":["Not true sophisticated Smith women",[["You really don't know what to say to that","End"]]],
                                                                                                            "mortal":["You... you're mortal.  How gauche",[["I'm mortal?","moreExp"],["And you aren't?","moreExp"]]],
                                                                                                            "proud":["And that's why this college is falling apart",[["This college is perfectly lovely","argue"],["And not the rising problems with financial aid?","finaid"]]],
                                                                                                            "finaid":["True Smith women aren't poor enough to depend on that kind of thing",[["Unbelievable","End"]]],
                                                                                                            "argue":["It would be without your kind here",[["Unbelievable","End"]]],
                                                                                                            "moreExp":["What God is mortal?",[["(Gracefully back out from this conversation","End"]]]})
   #ENDINGS
   basementEnding = Ending(badEndConditions, ["You ate the tomato because you're hungry", "You cannot escape the basement...","You're trapped in here forever"])
   #CHOICES
   #OPTIONS
   #GAMES
   decode = MiniGame("Decode", "Figure out what the message says", decoding_game, paperSlip)
   hangman = MiniGame("Hangman", "Guess the hidden word", hangman, candle)
   
   #ROOMS
   lectureHall = Room("lectureHall","A lecture hall","The lecture hall for your Computer Science class",[[professor,True],
                                                                                                         [lookLectureHall,True],
                                                                                                         [mariya,True],
                                                                                                         [sam,True],
                                                                                                         [janet,True],
                                                                                                         [kaitlin,True]])
                                                                                                    


   campus = Room("campus","The school campus","This is where you can do all those campus things",[[toCampusCenter,True],[hangman,True]])
   campusCenter = Room("campusCenter","The campus center","You can visit different rooms in here",[[toResourceRoom,True],
                                                                                                   [toBookStore,True],
                                                                                                   [fromCampusCenterToCampus,True],
                                                                                                   [toElmStreet,True],
                                                                                                   [oneCard,True],
                                                                                                   [lookCampusCenter,True],
                                                                                                   [decode, True],
                                                                                                   [paperSlip,False],[toCarrollRoom,False]])
   resourceRoom = Room("resourceRoom","The resource room","You can pick up some art supplies in here",[[fromResourceRoom,True],
                                                                                                       [markers,True],
                                                                                                       [paper,True]])
   carrollRoom = Room("carrollRoom","The Carroll Room","Some orgs host events here",[[toCampusCenter, True]])
   bookStore = Room("bookStore","The Book Store","You don't think you need any more Smith College tee shirts yet",[[allison,True],
                                                                                                                   [fromBookStore,True]])
   gillDine = Room("gillDine", "The Gillett Dining Hall", "Vegetarian anchovies in the tin...", [[toGillett, True]])
   #EVENT ROOMS
   sessionsAnnex = eventRoom("sessionsAnnex", "Sessions Annex", "A strange, sweet, smell...", [[faint, True]], ["Everything feels a bit woozy here..."], "psychedelic.mp3")
   sessionsBasement = eventRoom("sessionsBasement", "Sessions Basement", "You're trapped in here...", [[toSessionsHall,False],[candle,False]],["You wake up slowly", "The room is dim", "You see a shadowy figure sitting by the wall"], "")

   elmStreet = eventRoom("elmStreet","Elm Street","You know that Sessions is here",[[toCampusCenter,True],
                                                                                    [toGillett,True],
                                                                                    [toOutsideSessions,True]],["As you step onto Elm Street, you feel a sense of foreboding.",
                                                                           "Of course, it could just be your umpteenth serving of bulgogi settling badly",
                                                                           "Or even your Green Street rivalry.",
                                                                           "but somehow, you think that isn't right.",
                                                                           "Something very wrong is lingering in the air here."],"")
   
   outsideSessions = eventRoom("outsideSessions","Outside of Sessions","You can see the sickly green of the paint",[[toSessionsHall,False],
                                                                                                                    [toElmStreet,True],
                                                                                                                    [sophia,True]],["The feeling of unease gets worse",
                                                                                                                                         "You can feel the rush of your heart",
                                                                                                                                         "You're terrified",
                                                                                                                                         "How can one group project inspire so much worry?"],"")
                                                                                                                    
   gillett = eventRoom("gillett","Gillett House","Somehow, the best house on campus",[[toElmStreet,True],
                                                                                      [allan,True],
                                                                                      [toGillDine,False],
                                                                                      [oneCard,False],
                                                                                      [lookGillett,True]],["This place is pretty great",
                                                                                                          "You'd recommend it to anyone"],"")

   sessionsHall = eventRoom("sessionsHall","The hall to Sessions house","You can see coats everywhere",[[toSessionsParlor,True],
                                                                                                        [toSessionsAnnex, True],
                                                                                                         [toOutsideSessions,False],[carl,True]],["You're in the Sessions Hallway",
                                                                                                                                  "You hear a startling 'THUNK'",
                                                                                                                                  "The door behind you seems sealed shut",
                                                                                                                                  "You try to open it, rapidly jiggling the handle",
                                                                                                                                  "It doesn't matter",
                                                                                                                                  "You're trapped in Sessions House.",
                                                                                                                                  "You need to find Celia"],"circushomonculus.mp3")
   sessionsParlor = eventRoom("sessionsParlor","Sessions Parlor","Old china rests inside of a cabinet and floral decorations abound",[[esther,True],
                                                                                                                                      [toSessionsHall,True],
                                                                                                                                      [lookParlor,True]],["This is the only place that you can get to from the Hall",
                                                                                                                                         "It seems like it was suspended in time",
                                                                                                                                         "You've stepped into another era"],"")
   
#THIS IS THE PLAYER  Location is set with their initialization
player = Person("Ritchie",locations[current_story.landing_point])
playerStuff = {"player": player}   



#THIS IS NON CLASS BASED DEFINITIONS
def getInput():
    player_input = input("--> ")
    return player_input
def help():
    print("""
Dialogue, walking, and picking up items simulator
Simply enter the number of the command that you want to do.
Type the number as a numeral or it will not work.
You can end the game by typing "end."
If you have combinable items, you can put them together in the inventory menu.
          """)

def gameEnder():
    inventory_list = player_inventory.contents
    if current_story == classic:
       ending_choices = {garage.name:"Ending Test", basement.name:"basement key test"}
       # garage ending
       for items in inventory_list:
           if items.name in ending_choices.values():
               if player.location.name in ending_choices.keys():
                   if player.location.name == garage.name:
                       print("The game has ended because you went to the Man Cave")
                       print("A.K.A. the Garage")
                       print("How dare you ruin the sanctity of your dad's special shrine to Manhood")
                       print("Your dad is very, very disappointed.")
                       win = GraphWin("Dad", 350, 350)
                       dad_bg = Image(Point(175, 175), "disappointeddad.gif")
                       dad_bg.draw(win)
                       time.sleep(4)
                       win.close()
                       pygame.mixer.music.stop()
                       going = False
                       return going
           else:
               going = True
               return going
       else:
           going = True
           return going

def whatToDo(answer):
   options ={"Exit":Exit,
            "Look":Look,
            "NPC":NPC,
            "Choice":Choice,
            "Item":Item,
            "Key":Key,
            "fetchNPC":fetchNPC,
            "Fart":Fart,
            "MiniGame":MiniGame
       }
   if type(answer) == Exit: #if the type of the command associated is Exit, complete an exit action
       player.moveSelf(answer.from_room,answer.to_room)
       print("You moved to "+ player.location.printed_name)
   elif type(answer) == Look: #code this :disappointed: - find image files
       answer.showImage()
   elif type(answer) == Celia:
      answer.speak(player,player.location)
   elif type(answer) == NPC:
       answer.speak()
   elif type(answer) == Choice:
       answer.makeChoice()
   elif type(answer) == smoothTalker:
      answer.speak(player_inventory)
   elif type(answer) == Partner:
       answer.speak(player.location, Celia)
   elif type(answer) == Item:
       answer.putIntoInventory(player.location,player_inventory)
   elif type(answer) == Key:
       if answer in player_inventory.contents:
           answer.useKey(player_inventory,answer.command,answer.room)
       else:
           answer.putIntoInventory(player.location,player_inventory)
   elif type(answer) == fetchNPC:
       answer.interact(player_inventory)
   elif type(answer) == MiniGame:
       answer.playGame()
       answer.getPrize(player_inventory)

    
def processInput(player_input):

   i = 0
   counter_of_written = len(locations[player.location.name].commands)
   try:
       for value in player.location.commands: #the counter of the written is how many of the commands are written to the screen
           if value[1] == False:
               counter_of_written -= 1
       for value in player.location.commands: #this determines how far off the player's input will be from what they are actually asking for
           if (value[1] == False and (player.location.commands.index(value)<int(player_input))): #it differs from the counter of written because it only goes up to the total of the player input
               player_input = int(player_input)+1 #for each one that's false, the player's input will have to go one further from where it originally would have gone
       #the above will run a check that handles false commands
       try:
           player_choice = player.location.commands[int(player_input)-1]
           if player_choice[1] == True:
               #this section right here is where I can add in different kinds of commands
               if type(player_choice[0]) == Exit: #if the type of the command associated is Exit, complete an exit action
                   player.moveSelf(player_choice[0].from_room,player_choice[0].to_room)
               elif type(player_choice[0]) == Look:
                   player_choice[0].showImage()
               elif type(player_choice[0]) == NPC:
                   player_choice[0].speak()
               elif type(player_choice[0]) == smoothTalker:
                  player_choice[0].speak(player_inventory)
               elif type(player_choice[0]) == Item:
                   player_choice[0].putIntoInventory(player.location,player_inventory)
               elif type(player_choice[0]) == Choice:
                   player_choice[0].makeChoice()
               elif type(player_choice[0]) == Partner:
                  player_choice[0].speak(player.location,cel)
               elif type(player_choice[0]) == Celia:
                  player_choice[0].speak(player,player.location)
               elif type(player_choice[0]) == Key:
                   if player_choice[0] in player_inventory.contents:
                       player_choice[0].useKey(player_inventory,player_choice[0].command,player_choice[0].room)
                   else:
                       player_choice[0].putIntoInventory(player.location,player_inventory)
               elif type(player_choice[0]) == fetchNPC:
                   player_choice[0].interact(player_inventory)
               elif type(player_choice[0]) == doNPC:
                  player_choice[0].interact(player_inventory)
               elif type(player_choice[0]) == MiniGame:
                  player_choice[0].playGame()
                  player_choice[0].getPrize(player_inventory)
               elif type(player_choice[0]) == realRoomCommand:
                  player_choice[0].doTheThing(player_inventory,player.location)

       except IndexError:
           player_choice = player_input
# this accounts for the increase in player_input from above without affecting the rooms that don't have falses
           for value in player.location.commands: #this determines how far off the player's input will be from what they are actually asking for
               if (value[1] == False and (player.location.commands.index(value)<int(player_input))): #it differs from the counter of written because it only goes up to the total of the player input
                   player_input = int(player_input)-1 #for each one that's false, the player's input will have to go one less than what was adjusted above
                   player_choice = player_input

           if int(player_choice) ==(counter_of_written+1): #if the number the player inputs is past the list of commands inherent to each room and so is a normal commands
               help()
           elif int(player_choice) == (int(counter_of_written) + 2):
              
               player_inventory.printItems()
               if len(player_inventory.contents) >= 2:
                  choose_combine = input("Do you want to create a new item? YES/NO: ")
                  if choose_combine.upper().strip() == "YES":
                      try:
                          player_inventory.alchemy()
                          player_inventory.printItems()
                      except IndexError:
                           print("")
                  else:
                      print("")
           elif int(player_choice) >= (counter_of_written+3): #if it isn't one of the commands
               print("\nNon valid command help\n")
           
   except ValueError:
       print("\nPlease type in numerals unless doing an end command\n")


def main():
    going = True
    while going == True:
        state = "worldExp"
        #put ending checker here.  random ending put in just for the sake of checking to see if it will work
        #idea - check dictionary of choices made throughout the game for different endings maybe.
        if state == "worldExp":
           player.location.printDesc()
           player.location.printCommands()
           player_input = getInput()
           if player_input.upper() ==  "END" or player_input == "End" or dead == "yes":
               print("Thank you for playing!")
               pygame.mixer.music.stop()
               break
           else:
               processInput(player_input)
           if current_story.name == "final" and player.location == sessionsBasement:
              basementEnding.playEnding()
              print("thank you for playing!")
              pygame.mixer.music.stop()
              break
        
            
    time.sleep(1)
#####################CODE EXECUTION###################################
if __name__ == "__main__":
   pygame.mixer.init()
   pygame.mixer.music.load("Happy_Ending.mp3")
   pygame.mixer.music.play(-1)
   #intro()
   main()


######################################################################
#http://blog.thedigitalcatonline.com/blog/2015/01/12/accessing-attributes-in-python/
#https://codereview.stackexchange.com/questions/57438/game-inventory-system
# Professor John Foley's code "Spooky Example" - ported these ideas into OOP
# https://www.pythonforbeginners.com/error-handling/python-try-and-except
#https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary
#https://stackoverflow.com/questions/216972/in-pyt5hon-what-does-it-mean-if-an-object-is-subscriptable-or-not
#https://www.tutorialspoint.com/python/list_index.htm
#https://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists/11520540
#https://www.edureka.co/community/18841/how-do-play-audio-playsound-in-background-of-python-script
#https://www.pygame.org/docs/ref/mixer.html
#https://www.quora.com/What-is-the-use-of-__str__-in-python
#https://stackoverflow.com/questions/46058432/python-3-set-name-of-object-in-class/46058669
#https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python
#https://stackoverflow.com/questions/35068209/how-do-i-repeat-music-using-pygame-mixer
#https://stackoverflow.com/questions/3545331/how-can-i-get-dictionary-key-as-variable-directly-in-python-not-by-searching-fr/3545353
#https://www.programiz.com/python-programming/exception-handling
#https://www.pygame.org/docs/ref/event.html?highlight=video%20system%20initialized
#https://www.pygame.org/docs/ref/display.html#pygame.display.flip
#https://stackoverflow.com/questions/10466590/hiding-pygame-display
#https://www.pygame.org/wiki/WindowResizing
#https://stackoverflow.com/questions/21209496/getting-width-and-height-of-an-image-in-pygame



#music
#circus homunculus, the Hunger Artist
#Jockers Dance Orchestra, The Royal Vagabond.
