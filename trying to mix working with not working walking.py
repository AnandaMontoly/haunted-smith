import webbrowser
import time
import random

class Room:
###This is an environment with a series of commands
###that the player can be within and can use commands inside of

    def __init__(self,name,printed_name,description,commands):
        self.name = name
        self.printed_name = printed_name
        self.description = description
        self.commands = commands
    def printDesc(self):
        print(self.description)
        return self.description
    def printCommands(self):
        i = 0
        for value in self.commands:
            if value[1] == True:
                i +=1
                try:
                    print(str(i)+".",value[0].name+".", value[0].description)
                except AttributeError:
                    print(str(i)+".",str(value[0].name)+".",str(value[0]["description"]))
        print(str(i+1)+". Get help. Bring up short guide")
        i += 1
        print(str(i+1)+". Print your inventory.")
            
    def giveCommands(self):
        commands_per_room = self.commands
        return commands_per_room

class roomCommand:
###This is a command within a room.  Technically, items should be a subclass of it but I yeeted it.
    def __init__(self,name,description):
        self.name = name
        self.description = description
    def giveName(self):
        return self.name
    def giveDescription(self):
        return self.description
        
class Exit(roomCommand):
###This is a room command which provides the info for the player to move from one room to the other
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
        print("The door to the", to_room.name,"has been opened.")
        for command in from_room.commands:
            if command[0] == self:
                if command[0] == self: #open these gates
                    command[1] = True
        
class NPC(roomCommand):
    ###This is a room command class which has dialogue and talks to the user.
    def __init__(self,name,description,dialogue,dialogue_number):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.dialogue_number = dialogue_number
        self.dialogue_count = 0
    def speak(self):
        print("\n")
        print(self.name.upper())
        print("""#################################################
              """)
        print(self.dialogue[self.dialogue_count % self.dialogue_number])
        self.dialogue_count += 1
        print("""#################################################
              """)        
    
class fetchNPC(NPC):
    ###this npc is special because they will ask the player for an item in their initial dialogue
    ###and then will change their dialogue after an item is used to.
    #dialogue 1 = "I need this item" or some shit like that lol
    #dialogue 2 - "thank you for doing that whatever the fuck.
    #they will also pass in a string which will be the command
    #that is processed by a
    def __init__(self,name,description,dialogue,dialogue2,thanks_dialogue,dialogue_number,action,Exit,stage,item,item2):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.dialogue2 = dialogue2
        self.thanks_dialogue = thanks_dialogue        
        self.dialogue_number = dialogue_number
        self.dialogue_count = 0
        self.action = action #what the npc does upon being gifted the item
        self.Exit = Exit
        self.stage = stage
        self.item = item #the item that the npc wants
        self.item2 = item2

    def processAction(self,inventory):
        #if the task that the npc does upon having their quest being solved is opening up a location
        if self.action == "openDoor":
            self.Exit.openDoor()
            self.item.takeFromInventory(inventory)
        if self.action == "giveItem":
            print(self.name,"has a gift for you as thanks.")
            self.item2.putIntoInventoryFromNPC(inventory)
            print("""
""")
    def interact(self,inventory):
        
        if self.stage == "notFulfilled" and self.item not in inventory.contents:
            self.speak()
        elif self.stage == "notFulfilled" and self.item in inventory.contents:
            print(self.name.upper())
            print("""#################################################
              """)
            print(self.thanks_dialogue)
            print("""#################################################
              """)
            self.processAction(inventory)
            self.stage = "Fulfilled"
            self.dialogue = self.dialogue2
        elif self.stage == "Fulfilled":
            self.speak()
        
            
    
    
class Look(roomCommand):
###This will later return an image of the room in a browser.  Not yet tho.

    def showImage(self):
        print("Look")
        print("not coded yet :(")

class Inventory:
    ###This is the dictionary that holds the items and the special methods for it yo.
    def __init__(self,contents):
        self.contents = []
    def printItems(self):
        print("\nThese are all of the items in your inventory\n")
        i = 0
        for value in self.contents:
            if value.shown == True:
                i +=1
                print(str(i)+".",value.name+".",value.description)
                
        if i == 0:
            print("There are no items in your inventory")
        print("\n")


class Fart(roomCommand):
    def fart(self):
        print("fart")
class Item:
    def __init__(self,name,description,shown):
        self.name = name
        self.description = description
        self.shown = shown
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
            self.newCommand()
        inventory.contents.append(self)
        print("You put the",self.name,"into your inventory.")
        
    def takeFromInventory(self,inventory):
        taking_counter = 0
        for thing in inventory.contents:
            taking_counter +=1
            if thing.name == self.name:
                del inventory.contents[taking_counter-1]
                break
    
class Key(Item):
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
        print("You have used the",self.name,"to open a way to the",self.room.name)
        Exit_here.openDoor()
        from_room = locations[Exit_here.from_room]
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
    


class Person:
#This is a class with the ability to go from one place to the other.  The player is one of these.  Literally
    #all it can do is move from one room to the other, lol.
    def __init__(self,name,location):
        self.name = "Ritchie"
        self.location = location
    def giveLocation(self):
        return self.location
    def moveSelf(self,from_room,to_room):
        self.location = locations[to_room]
        return self.location
    
#TEST CLASS
fart = Fart("a big fart","wow, it's gross.  no big surprise there, sherlock.")


#THIS IS LOOKING AROUND
look_laboratory = Look("Look in the laboratory","There are strange beeping noises and nuclear fallout symbols everywhere.")

look_house = Look("Look in the house","McLoving this architecture")
look_basement = Look("Look around the basement","It's damp and dingy.")
look_secret_room = Look("Look around","Actually, you should probably pass on that.  It seems scary")
look_outside = Look("Look outside","I mean there's stuff here but who cares?")
look_garage = Look("Look in the garage","All I can see is old tools dad promised himself that he'd use.")

#THIS IS THE PLAYER'S INVENTORY
player_inventory = Inventory([])

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
#THESE ARE KEYS

garage_key = Key("Garage Key","This is the key that will let you into dad's garage",True,"garage",enter_garage)

#THESE ARE NPCS
uncle_joe = NPC("Uncle Joe","Is that Uncle Joe?",["I'm busy in here.","Do zou zink I am a Russian spy"],2)
mom = NPC("Mom","She's holding a platter of cookies",["Do you want some cookies?","I made them just for you"],2)
dad = NPC("Dad","He's looking forelornly at the lawn mower",["Your mother told me to fix this","I don't have any idea how"],2)
rat = NPC("A Rat","Looks like the mouse trap didn't work.",["Squeak!","Squeeeeak!"],2)
vlad = fetchNPC("Definitely not Vlad","A man sitting in front of a computer - seems valid",["I need a green cube","I think that's absolutely valid"],["Wow, you're so nice for helping out","This is a very good cube.  Not nuclear"],"Zank you for ze cube",2,"giveItem",tunnel,"notFulfilled",greenCube,rock)

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

outside = Room("outside","Ew, what is this place","Is this outside???",[[look_outside,True],
                                                                        [go_inside,True],
                                                                        [dad,True],
                                                                        [garage_key,True],
                                                                        [enter_garage,False]])
laboratory = Room("laboratory","A Secret Laboratory","This place seems a little sketchy.  There's Russian writing everywhere",[[look_laboratory,True],
                                                                                                                               [leave_lab,True],
                                                                                                                               [vlad,True],
                                                                                                                               [tunnel,False]])
                                                                                                                               

#THIS IS THE PLAYER  Location is set with their initialization
player = Person("Ritchie",house)


#LOCATIONS DICTIONARY.  I have literally no idea why I need this, lol.  But I know if I don't, it flips the fuck out.
locations = {
"house":house,
"basement":basement,
"secret_room":secret_room,
"outside":outside,
"garage":garage,
"laboratory":laboratory}

#THIS IS NON CLASS BASED DEFINITIONS
def getInput():
    player_input = input("--> ")
    return player_input
def help():
    print("""
Dialogue, walking, and picking up items simulator
Simply enter the number of the command that you want to do.
Type the number as a numeral or it will not work.
You can end the game simply by typing "end."
          """)
def processInput(player_input):
    
    i = 0
    counter_of_written = len(locations[player.location.name].commands)
    try:
        player_input_integer = int(player_input)
        for value in player.location.commands:
            if value[1] == False:
                counter_of_written -= 1
        #the above will run a check that handles false commands
        for value in locations[player.location.name].commands:
            if int(player_input) == (locations[player.location.name].commands.index(value)+1):
                if value[1] == False:
                    player_input = int(player_input) +1
                if value[1] == True:
                    #this section right here is where I can add in different kinds of commands
                    if type(value[0]) == Exit: #if the type of the command associated is Exit, complete an exit action
                        player.moveSelf(value[0].from_room,value[0].to_room)
                        print("You moved to "+ player.location.printed_name)
                        break
                    elif type(value[0]) == Look: #code this :( - find image files
                        value[0].showImage()
                        break
                    elif type(value[0]) == NPC:
                        value[0].speak()
                        break
                    elif type(value[0]) == Item:
                        value[0].putIntoInventory(player.location,player_inventory)
                        break
                    elif type(value[0]) == Key:
                        if value[0] in player_inventory.contents:
                            value[0].useKey(player_inventory,value[0].command,value[0].room)     
                        else:
                            value[0].putIntoInventory(player.location,player_inventory)
                        break
                    elif type(value[0]) == fetchNPC:
                        value[0].interact(player_inventory)
                        break
            if int(player_input) ==(counter_of_written+1): #if the number the player inputs is past the list of commands inherent to each room and so is a normal commands
                help()
                break
            elif int(player_input) == (counter_of_written+2):
                player_inventory.printItems()
                break
            elif int(player_input) >= (counter_of_written+3): #if it isn't one of the commands listed
                print("\nNon valid command\n")
                break
    except ValueError:
        print("\nPlease type in numerals unless doing an end command\n")


def main():
    going = True
    while going == True:
        #put ending checker here.  random ending put in just for the sake of checking to see if it will work
        #idea - check dictionary of choices made throughout the game for different endings maybe.
        if player.location.name == garage.name:
            print("The game has ended because you went to the Man Cave")
            print("A.K.A. the Garage")
            print("How dare you ruin the sanctity of your dad's special shrine to Manhood")
            print("Your dad is very, very disappointed.")
            time.sleep(4)
            webbrowser.open("https://i.imgflip.com/13cf8p.jpg")
            break

        player.location.printDesc()
        player.location.printCommands()
        player_input = getInput()
        if player_input == "End" or player_input == "END" or player_input == "end":
            print("Thank you for playing!")
            break
        else:
            processInput(player_input) 
            
def intro():
    print("A long time ago. . .")
    time.sleep(1)
    print("In a land far away. . .")
    time.sleep(1)
    print("You, a bored kid, decided it was time to go on an adventure. . .")
    time.sleep(1)
    print("Unfortunately, adventure is a high bar to reach in a town like yours")
    time.sleep(1)
    print("Suburbia Hell")
    time.sleep(1)
    print("""   ___     _____ _          _                    __   _______                       _ _ _      
  / _ \   / ____(_)        | |                  / _| |__   __|                     (_) | |     
 | (_) | | |     _ _ __ ___| | ___  ___    ___ | |_     | | _____      ___ ____   ___| | | ___ 
  \__, | | |    | | '__/ __| |/ _ \/ __|  / _ \|  _|    | |/ _ \ \ /\ / / '_ \ \ / / | | |/ _ |
    / /  | |____| | | | (__| |  __/\__ \ | (_) | |      | | (_) \ -  - /| | | \ - /| | | |  __|
   /_/    \_____|_|_|  \___|_|\___||___/  \___/|_|      |_|\___/ \_/\_/ |_| |_|\_/ |_|_|_|\___|
                                                                                               
                                                                                               """)
    time.sleep(1)
#####################CODE EXECUTION###################################
if __name__ == "__main__":
    #pass
    main()
######################################################################
#http://blog.thedigitalcatonline.com/blog/2015/01/12/accessing-attributes-in-python/
#https://codereview.stackexchange.com/questions/57438/game-inventory-system
# Professor John Foley's code "Spooky Example" - ported these ideas into OOP
# https://www.pythonforbeginners.com/error-handling/python-try-and-except
#https://stackoverflow.com/questions/5844672/delete-an-element-from-a-dictionary
#https://stackoverflow.com/questions/216972/in-python-what-does-it-mean-if-an-object-is-subscriptable-or-not
#https://www.tutorialspoint.com/python/list_index.htm
#https://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists/11520540
