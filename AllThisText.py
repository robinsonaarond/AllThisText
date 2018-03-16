#! /usr/bin/env python

# Title screen
# Items.  Can be in inventory (on your person), in a room, accessible at certain times (visible/takeable flag?).  Personal inventory cap?
# Locations.  Have description (varied based on description), and ingress/egress points.  Each of these needs another location to reference.  Also may have custom text for other exit points that don't work.  Hints if player takes long enough in the room
# NPCs. Basically like items that can't be taken, and that have state-based dialog.
# Actions. Look/Inspect/Go/Take/Eat
# Turn counter
# Save/Load function
# Endgame screen
# Game completion percentage
# Score (usually a product of secrets found/puzzles solved/% game completed)

#import re
import time
import sys

class Globals():
    def __init__(self): 
        self.moves            = 0
        self.points           = 0
        self.points_total     = 50
        self.secrets_found    = 0
        self.total_secrets    = 0
        self.puzzles_solved   = 0
        self.total_puzzles    = 0
        self.sleep_interval   = 0.1
        self.item             = spawn_items()
        self.rooms            = spawn_rooms()

class Room():
    def __init__(self):
        self.name             = ""
        self.description      = ""
        self.time_in_room     = 0
        self.hints            = { "0": "" }
        self.exits            = []
        self.initial_items    = []

class Player():
    def __init__(self):
        self.name             = ""
        self.room             = "start"
        self.inventory        = []

class Item():
    def __init__(self):
        self.name        = ""
        self.description = ""
        self.location    = "player"
        self.accessible  = True
        self.visible     = True
        self.takeable    = True

# Statically generated list of all Items in the game in their initial state
def spawn_items():
    object_list = {}
    item_list = [
            {   
                "id"          : "picture", 
                "name"        : "PICTURE OF THE MOON", 
                "description" : "It is a picture of the moon.",
                "examined"    : "You see nothing special about |g.item['picture'].name|.  |g.item['picture'].description",
                "takeable"    : True,
                "taketext"    : ", and put it in your pocket",
            },
            {
                "id"          : "belt",
                "name"        : "CONVEYOR BELT",
                "description" : "NULL",
                "takeable"    : False,
                "taketext"    : "Only a moron would try to take a CONVEYOR BELT."
            }
        ]
    for item in item_list:
        obj = Item()
        for k, v in item.items():
            setattr(obj, k, item[k])
        object_list[item['id']] = obj
    return object_list

def spawn_rooms():
    object_list = {}
    room_list = [
            {
                "id"          : "start",
                "name"        : "Factory Floor",
                "description" : "You are in a factory.\n\nIt's an enormous room.  If there are walls, they're too far away for you to make out.  You assume there is a ceiling somewhere above you, but when you look up, you see only an impenetrable darkness.\n\nIn front of you is a short |g.item['belt'].name| that stretches between two columns.  There are other people standing at similar conveyor belts all around you, in all directions, as far as the eye can see.<p><p>\n\nIn your hand is a |g.item['picture'].name|.",
                "shortdesc"   : "You are on the factory floor.  It's an enormous room.  You see a |g.item['belt'].name| in front of you.",
                "exits"       : { "n": None, "s": None, "e": "boiler", "w": None },
                "hint"        : "(There is a conveyor belt though.  It is stopped.)",
                "items"       : [],
                "itemstext"   : "  On the floor you see |','.join(g.rooms[g.player.room].items)|."
            }
        ]
    for room in room_list:
        obj = Room()
        for k, v in room.items():
            setattr(obj, k, room[k])
        object_list[room['id']] = obj
    return object_list

def process_desc(room_desc):
    room_sanitized = []
    # Parse out the template code
    while "|" in room_desc:
        room_desc = room_desc.split('|')
        for line in room_desc:
            if 'g' and '.' and '[' in line:
                room_sanitized.append(eval(line))
            else:
                room_sanitized.append(line)
    return "".join(room_sanitized)

def enter_room(g):
    room = g.rooms[g.player.room]
    room_desc = room.description
    if len(room.items) > 0:
        room_desc = room_desc + room.itemstext
    room_sanitized = process_desc(room_desc)

    # Parse <p> markup for pauses
    for line in room_sanitized.split("<p>"):
        if line:
            print line
            time.sleep(g.sleep_interval)

def reset_game(g):
    g.player.room = "start"
    g.player.name = ""
    g.player.inventory = [ 'picture' ]
    enter_room(g)

def __action_take(g,textinput,action):
    for match in action.matches:
        textinput = textinput.replace(match, "").strip()
    if len(textinput.split()) == 1:
        try:
            item = g.item[textinput]
        except:
            print "How can you take '%s'?  I don't know what it is." % textinput
            return
        # Assume it's an Item
        if textinput not in g.player.inventory:
            if item.takeable:
                print "You take the %s%s." % (item.name,item.taketext)
                g.player.inventory.append(textinput)
            else:
                print item.taketext
        else:
            print "You can't take the %s because you already have it." % item.name

def __action_drop(g,textinput,action):
    text = textinput.split()
    if len(text) > 1:
        itemname = " ".join(text[1:])
        try:
            item = g.item[itemname]
        except:
            print "I'm not sure what '%s' even is, let alone know how to drop it." % itemname
            return
        if itemname in g.player.inventory:
            print "You drop the %s." % g.item[itemname].name
            g.player.inventory.remove(itemname)
            g.rooms[g.player.room].items.append(itemname)
        else:
            print "You don't actually have the %s" % g.item[itemname].name
    else:
        print "What do you want me to drop?"

def __action_look(g,textinput,action):
    # If there is an argument, it must be an object
    if len(textinput.split()) >= 2:
        action = textinput.split()[0]
        item_name = textinput.split()[-1]
        if action == "examine" and hasattr(g.item[item_name], 'examined'):
            print process_desc(g.item[item_name].examined)
        else:
            print "You look at the %s.  %s" % (g.item[item_name].name, process_desc(g.item[item_name].description))
    # If no argument, it must be the room.  Use the short description
    else:
        room = g.rooms[g.player.room]
        if len(room.items) > 0:
            room_desc = room.shortdesc + room.itemstext
        else:
            room_desc = room.shortdesc
        print process_desc(room_desc)

def __action_inventory(g,textinput,action):
    print "You take stock of your possessions.  You are carrying the following:\n"
    if len(g.player.inventory) == 0:
        print "Nothing"
    else:
        for item in g.player.inventory:
            print "  ", item

def __action_exit(g,textinput,action):
    print "Thanks for playing.  You played for a total of %s moves, and your score was %s out of a possible %s." % (g.moves, g.points, g.points_total)
    sys.exit(0)

def process_action(g,textinput):
    # Actions. Look/Inspect/Go/Take/Eat
    # Action list
    class Action():
        def __init__(self):
            pass
    #action_dict = [ "eat", "play", "love", "go", "exit", "quit" ]
    actions = {}
    action_dict = [ 
        {
            "id"            : "take",
            "matches"       : [ "take", "grab", "pick up", "get", "steal" ],
            "description"   : "For putting items in your inventory.",
            "run"           : __action_take
        },
        {
            "id"            : "drop",
            "matches"       : [ "drop" ],
            "description"   : "For putting items in the room you're in.",
            "run"           : __action_drop
        },
        {
            "id"            : "look",
            "matches"       : [ "look", "l", "examine" ],
            "description"   : "Take a look around you.",
            "run"           : __action_look
        },
        {
            "id"            : "inventory",
            "matches"       : [ "inventory", "i" ],
            "description"   : "You take stock of your possessions.",
            "run"           : __action_inventory
        },
        {
            "id"            : "exit",
            "matches"       : [ "exit" ],
            "description"   : "Leave the game forever.  Actually you can play again at any time.",
            "run"           : __action_exit
        }
    ]
    for action in action_dict:
        obj = Action()
        for k, v in action.items():
            setattr(obj, k, action[k])
        actions[action['id']] = obj
    
    if textinput is not "":
        action_exists = False
        for action in actions.keys():
            if any(textinput.startswith(x) for x in actions[action].matches):
                actions[action].run(g,textinput,actions[action])
                action_exists = True
                break
        if not action_exists:
            print """I don't understand "%s".""" % textinput

def run_game(g):
    reset_game(g)
    while True:
        textinput = raw_input("\n> ")
        process_action(g, textinput.lower())
        g.moves += 1

if __name__ == "__main__":
    g = Globals()
    g.player = Player()
    run_game(g)
