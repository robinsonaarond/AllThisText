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

import cmd

class Globals():
    def __init__(self): 
        moves            = 0
        points           = 0
        secrets_found    = 0
        total_secrets    = 0
        puzzles_solved   = 0
        total_puzzles    = 0
        self.item        = spawn_items()

class Room():
    def __init__(self):
        name             = ""
        description      = ""
        time_in_room     = 0
        hints            = { "0": "" }
        exits            = []
        initial_items    = []

class Player():
    def __init__(self):
        name             = ""
        room             = "start"
        inventory        = []

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
                "name"        : "picture", 
                "description" : "It's just a picture of the moon.", 
            }
        ]
    for item in item_list:
        obj = Item()
        for k, v in item.items():
            setattr(obj, k, item[k])
        object_list[item['name']] = obj
    return object_list

def reset_game(g, player):
    player.room = "start"
    player.name = ""
    player.inventory = [ g.item['picture'] ]

def process_action(g, player, action):
    pass

def run_game(g, player):
    reset_game(g, player)
    while True:
        action = raw_input("> ")
        process_action(g, player, action)

if __name__ == "__main__":
    g = Globals()
    player = Player()
    run_game(g, player)
