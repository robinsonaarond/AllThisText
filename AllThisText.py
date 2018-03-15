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

import time

class Globals():
    def __init__(self): 
        self.moves            = 0
        self.points           = 0
        self.secrets_found    = 0
        self.total_secrets    = 0
        self.puzzles_solved   = 0
        self.total_puzzles    = 0
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

# Statically generated list of all Items in the game in their initial state
def spawn_items():
    object_list = {}
    item_list = [
            {   
                "id"          : "picture", 
                "name"        : "PICTURE OF THE MOON", 
                "description" : "It is a picture of the moon."
            },
            {
                "id"          : "conveyor",
                "name"        : "CONVEYOR BELT",
                "description" : "NULL"
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
                "description" : "You are in a factory.\n\nIt's an enormous room.  If there are walls, they're too far away for you to make out.  You assume there is a ceiling somewhere above you, but when you look up, you see only an impenetrable darkness.\n\nIn front of you is a short <conveyor> that stretches between two columns.  There are other people standing at similar conveyor belts all around you, in all directions, as far as the eye can see.<p><p>\n\nIn your hand is a <picture>",
                "exits"       : { "n": None, "s": None, "e": "boiler", "w": None },
                "hint"        : "(There is a conveyor belt though.  It is stopped.)"
            }
        ]
    for room in room_list:
        obj = Room()
        for k, v in room.items():
            setattr(obj, k, room[k])
        object_list[room['id']] = obj
    return object_list

def enter_room(g):
    room_desc = g.rooms[g.player.room].description.split("<p>")
    for line in room_desc:
        if line:
            print line
            time.sleep(1)

def reset_game(g):
    g.player.room = "start"
    g.player.name = ""
    g.player.inventory = [ g.item['picture'] ]
    enter_room(g)

def process_action(g, action):
    # Actions. Look/Inspect/Go/Take/Eat
    # Action list
    class Action():
        def __init__(self):
            pass
    actions = [ "eat", "play", "love", "go", "exit", "quit" ]
    if action in actions:
        print action
    elif action is "":
        return
    else:
        print "I don't know how to do that."

def run_game(g):
    reset_game(g)
    while True:
        action = raw_input("> ")
        process_action(g, action)

if __name__ == "__main__":
    g = Globals()
    g.player = Player()
    run_game(g)
