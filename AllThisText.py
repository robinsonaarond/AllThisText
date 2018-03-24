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
import sys
from random import choice

class Globals():
    def __init__(self): 
        self.moves            = 0
        self.points           = 0
        self.points_total     = 50
        self.secrets_found    = 0
        self.total_secrets    = 0
        self.puzzles_solved   = 0
        self.total_puzzles    = 0
        self.sleep_interval   = 0.2
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
        self.room             = "factory"
        self.credits          = 0
        self.inventory        = []

class Item():
    def __init__(self):
        self.name        = ""
        self.description = ""
        self.location    = "player"
        self.accessible  = True
        self.visible     = True
        self.takeable    = True

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    CYAN      = '\033[36m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def static_images(g,img):
    if img == "post":
        print(chr(27) + "[2J")
        i = """

************************************************************
************************************************************

  __   _  _    _____  _    _        _____  _
 (  ) ( )( )  (_   _)( )  (_)      (_   _)(_)
 /o \ ( )( )    | |  | |_  _  __     | |   _  __  __  ___
( __ )( )( )    ( )  ( _ )( )(_      ( )  ( )( _\/_ )( o_)
/_\/_\/_\/_\    /_\  /_\||/_\/__)    /_\  /_\/_\  /_\ \(


************************************************************
************************************************************



All This Time
A Text Adventure Game
Copyright (c) 2017 Jonathan Coulton Inc., All rights reserved.
Revision 79 / Serial number 58784



"""
        print i
        time.sleep(1)
        print(chr(27) + "[2J")
    elif img == "moon":
        i = """
            .          .                                                    .
    +           .           +                     *                           . 
.                   *                   .                  .                 
              .                                 .                    
*                                .                                .          *
         *                                    .                          . 
                       .                                .
    .                               *                           *  
+              *                         .                              .
                                                     .                         
           .                  .                              .               
    *                        *                        *                  .
            .                                     .                         
                       .                                          .
                 *                                                     *
      .                                .                                     .
 *                                 *                        *           
                        *                             .                  
               .                                                    .
                                        *                                  *
        *                          .                             .
    *                                                 +                    
                      +                           .                      + 
                .                                           .          
""" + """
            .          .                        .....                       .
    +           .           +               _d^^^^^^^^^b_                     . 
.                   *                    .d''           ''b.                 
              .                        .p'   .   .-.       'q.       
*                                .    .d'       (   )       'b.   .          *
         *                           .d'      o  '-'   0     'b.         . 
                       .             ::   ()              .   ::
    .                                ::            .          ::   
+              *                     ::  .   .--.       0     ::        .
                                     'p.    |    |           .q'               
           .                  .       'p.   '.__.'  ()      .q'              
    *                        *         'b.                .d'            .
            .                            'q..   o      ..p'                 
                       .                    ^q........p^          .
                 *                              ''''                   *
      .                                .                                     .
 *                                 *                        *           
                        *                             .                  
               .                                                    .
                                        *                                  *
        *                          .                             .
    *                                                 +                    
                      +                           .                      + 
                .                                           .          
"""
        for line in i.splitlines():
            time.sleep(0.1)
            print line

def animate_stars():
    stars = [ "*", "+", "." ]
    for i in range(1,10):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, choice(stars)))
        sys.stdout.flush()
        time.sleep(0.4)

# Statically generated list of all Items in the game in their initial state
def spawn_items():
    object_list = {}
    item_list = [
            {   
                "id"          : "picture", 
                "name"        : "PICTURE OF THE MOON", 
                "description" : "It is a picture of the moon.",
                "examined"    : "You see nothing special about |g.item['picture'].name|.  |g.item['picture'].description",
                "matches"     : [ "picture", "picture of the moon", "pic", "photo" ],
                "takeable"    : True,
                "taketext"    : ", and put it in your pocket",
            },
            {   
                "id"          : "credit", 
                "name"        : "CREDITS", 
                "description" : "These will make all the difference back at your pod.",
                "examined"    : "|g.item['credit'].name| are digital.  You can't examine them.",
                "matches"     : [ "credit", "credits" ],
                "takeable"    : False,
                "taketext"    : "|g.item['credit'].name| are digital.  You can't 'take' them.",
            },
            {   
                "id"          : "slots", 
                "name"        : "SLOTS", 
                "description" : "There are slots next to a swith.  They look like they could hold something.",
                "examined"    : "They might hold |g.item['circuit'].name| if you cram them in hard enough.",
                "matches"     : [ "slot", "slots" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "How would you take them?  They're part of the wall.",
            },
            {   
                "id"          : "switch", 
                "name"        : "SWITCH", 
                "description" : "The switch is on the wall next to some |g.item['slots'].name|.",
                "examined"    : "It's an ordinary switch.  Next to it is a label that says 'DESTROY'.",
                "matches"     : [ "switch", "destroy switch" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "It's bolted to the wall.",
            },
            {   
                "id"          : "supervisor", 
                "name"        : "ROBOT SUPERVISOR", 
                "description" : "He's your boss.  Best be nice to him.",
                "examined"    : "|g.item['supervisor'].description|",
                "matches"     : [ "supervisor", "robot", "robot supervisor" ],
                "takeable"    : False,
                "visible"     : False,
                "sadness"     : False,
                "taketext"    : "Your |g.item['supervisor'].name| doesn't look like he wants to be taken anywhere.",
            },
            {   
                "id"          : "redpill", 
                "name"        : "RED PILL", 
                "description" : "The pill is small, red, and clear.  Its contents look something like blood.",
                "examined"    : "|g.item['redpill'].description|",
                "matches"     : [ "red pill", "redpill", "red" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "",
            },
            {   
                "id"          : "bluepill", 
                "name"        : "BLUE PILL", 
                "description" : "The pill is small, blue, and milky.  Its contents look something like happiness.",
                "examined"    : "|g.item['bluepill'].description|",
                "matches"     : [ "blue pill", "bluepill", "blue" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "",
            },
            {   
                "id"          : "circuit", 
                "name"        : "CIRCUIT BOARDS", 
                "description" : "They're circuit boards.  They look like they go in something.",
                "examined"    : "You examine them but you really don't know much about electronics.",
                "matches"     : [ "circuit", "circuits", "circuit boards" ],
                "takeable"    : False,
                "taketext"    : "How would you take them?  They're part of the wall.",
            },
            {   
                "id"          : "feelings", 
                "name"        : "FEELINGS", 
                "description" : "It's a circuit board.  It is labeled FEELINGS.",
                "examined"    : "You examine them but you really don't know much about FEELINGS.",
                "matches"     : [ "feelings", "feelings circuit board", "feels" ],
                "visible"     : False,
                "taketext"    : "  I mean, he's a robot right?  They're probably not even real feelings.",
            },
            {   
                "id"          : "senseofself", 
                "name"        : "SENSE OF SELF", 
                "description" : "It's a circuit board.  It is labeled SENSE OF SELF.",
                "examined"    : "You examine them but you really don't know much about FEELINGS.",
                "matches"     : [ "sense of self" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "The |g.item['senseofself'].name| is blocked by the |g.item['feelings'].name|.  You'll have to take that one first.",
            },
            {   
                "id"          : "willtolive", 
                "name"        : "WILL TO LIVE", 
                "description" : "It's a circuit board.  It is labeled WILL TO LIVE.",
                "examined"    : "You think about your own WILL TO LIVE.  Is is pre-programmed in like this?",
                "matches"     : [ "will to live" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "The |g.item['willtolive'].name| is blocked by the |g.item['senseofself'].name|.  You'll have to take that one first.",
            },
            {   
                "id"          : "widget", 
                "name"        : "WIDGET",
                "description" : "You see nothing special about the |g.item['widget'].name|.  It is a widget.",
                "examined"    : "It is a standard widget, ready for processing.",
                "matches"     : [ "widget" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "You can't take the |g.item['widget'].name|.",
            },
            {
                "id"          : "belt",
                "name"        : "CONVEYOR BELT",
                "matches"     : [ "conveyor", "belt", "conveyor belt" ],
                "description" : "The belt stretches onward to the right.  On the left side is an opening.",
                "takeable"    : False,
                "taketext"    : "Moving the CONVEYOR BELT would require a TEAM LIFT, and currently no one is available to help."
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
                "id"          : "factory",
                "name"        : "Factory Floor",
                "description" : "You are in a factory.\n\nIt's an enormous room.  If there are walls, they're too far away for you to make out.  You assume there is a ceiling somewhere above you, but when you look up, you see only an impenetrable darkness.\n\nIn front of you is a short |g.item['belt'].name| that stretches between two columns.  There are other people standing at similar conveyor belts all around you, in all directions, as far as the eye can see.<p><p>\n\nIn your hand is a |g.item['picture'].name|.",
                "shortdesc"   : "You are on the factory floor.  It's an enormous room.  You see a |g.item['belt'].name| in front of you.",
                "exits"       : { "n": None, "s": None, "e": "boiler", "w": None },
                "hint"        : "\n<p><p>(There is a conveyor belt though.  It is stopped.)",
                "hint_length" : 6,
                "running"     : False,
                "items"       : [],
                "itemstext"   : "  You also see: |', '.join([g.item[x].name for x in g.rooms[g.player.room].items])|."
            }
        ]
    for room in room_list:
        obj = Room()
        for k, v in room.items():
            setattr(obj, k, room[k])
        object_list[room['id']] = obj
    return object_list

def print_desc(room_desc, output=True):
    room_sanitized = []
    # Parse out the template code
    # Currently you can:
    #   put actual code wrapped in ||, e.g. |g.player.name|
    #   put pauses in the dialog using <p>
    if "|" in room_desc:
        while "|" in room_desc:
            room_desc = room_desc.split('|')
            for line in room_desc:
                if 'g' and '.' and '[' in line:
                    room_sanitized.append(eval(line))
                else:
                    room_sanitized.append(line)
        desc = "".join(room_sanitized)
    else:
        desc = room_desc
    if output:
        # Parse <p> markup for pauses
        if "<p>" in desc:
            for line in desc.split("<p>"):
                if line:
                    print line
                    time.sleep(g.sleep_interval)
        else:
            print desc
    else:
        return desc


def enter_room(g):
    room = g.rooms[g.player.room]
    room_desc = room.description
    room.time_in_room = 0
    if len(room.items) > 0:
        room_desc = room_desc + room.itemstext
    print_desc(room_desc)

def reset_game(g):
    g.player.room = "factory"
    g.player.name = ""
    g.player.inventory = [ 'picture' ]
    enter_room(g)

def all_this_time(g):
    print_desc("Your |g.item['supervisor'].name| sees the |g.item['picture'].name| and immediately begins to cry.  He sings a little tune.<p><p><p>\n\nAll we'll have is<p><p>All this time<p><p>All we'll have is<p><p>All this time<p><p>All this time\n")

def get_item(textinput):
    # Generate list of matchable items and their corresponding id
    available_items = []
    item = None
    for k, i in g.item.iteritems():
        for match in i.matches:
            available_items.append(match + '|' + k)

    for s in sorted(available_items, key=len, reverse=True):
        match, item_id = s.split('|')
        if textinput in match:
            item = g.item[item_id]
            break
    if item:
        if item.visible:
            return item
        else:
            print "You don't see any %s here." % textinput
            return None
    else:
        return item

def process_widget(g,_all=False):
    if g.item['widget'].visible:
        if not _all:
            if g.item['supervisor'].visible and not "redpill" in g.player.inventory:
                g.player.credits += 8
                print_desc("Too late!  Your |g.item['supervisor'].name| grips your shoulder.  \"Hey there buddy!,\" he says, \"Seems like you got a little distracted!  Maybe time to take a |g.item['redpill'].name|!\"")
                g.item['redpill'].visible = True
                g.player.inventory.append('redpill')
                g.rooms['factory'].shortdesc = "You idly look at stuff.  There it is.  Bunch of stuff.<p><p>Your |g.item['supervisor'].name| sighs again, but this time it comes out as a little moan."
            else:
                print_desc("You process the |g.item['widget'].name|.  You earn 8 |g.item['credit'].name|! Another |g.item['widget'].name| appears.")
                g.player.credits += 8
        else:
            if g.item['supervisor'].visible:
                print_desc("You mindlessly process |g.item['widget'].name|S.  Your |g.item['supervisor'].name| sighs.  \"Good job buddy.  You're really earning some credits I guess.\"")
                g.item['supervisor'].sadness = True
                g.item['supervisor'].description = "Your |g.item['supervisor'].name| looks miserable.  He stares bleakly into the middle distance."
            g.player.credits += 64

        if g.player.credits >= 48 and not g.item['supervisor'].visible:
            print_desc("You mindlessly process widgets.  Your thoughts begin to wander.\n<p><p><p><p>You think about what entertainment you will watch when you return to your pod's domicile.\n<p><p>You notice a |g.item['switch'].name| on the wall that's labeled \"Destroy.\"  Next to it are three empty |g.item['slots'].name| that look like they hold |g.item['circuit'].name|.\n<p><p><p><p>Oh No! You stopped processing |g.item['widget'].name|S and your |g.item['supervisor'].name| is right behind you!")
            g.item['slots'].visible = True
            g.item['switch'].visible = True
            g.item['supervisor'].visible = True
    else:
        print_desc("You can't see any widgets.")

def end_game(g):
    print_desc("<p>\nYour |g.item['supervisor'].name| winces.  Wait, do they feel pain?")
    the_end_is_near = False
    end_turn_count = 0

    # Note: https://xkcd.com/1378/ about this wall of conditionals
    while True:
        textinput = raw_input("\n>")
        text_sanitized = " ".join([ x for x in textinput.lower().split() if x not in g.word_ignore ])
        if not the_end_is_near:
            if textinput == "" and all(x in g.player.inventory for x in ['feelings','senseofself']):
                print "COME ON.  DO IT."
            elif text_sanitized == "":
                pass
            elif text_sanitized == "take sense of self":
                print_desc("Sure, why not?  You take, and you take, and you take.  Because you're a winner.")
                g.item['willtolive'].takeable = True
                g.player.inventory.append("senseofself")
            elif text_sanitized in ["take will to live","take will  live","take will","take will live"] and "willtolive" not in g.player.inventory and g.item['willtolive'].takeable == True:
                print_desc("Wow.  OK, but this may kill your |g.item['supervisor'].name|.  Are you sure? (y/n)")
                g.player.inventory.append("willtolive")
            elif "willtolive" in g.player.inventory and text_sanitized in [ "y", "n" ]:
                if text_sanitized == "y":
                    print_desc("You take your |g.item['willtolive'].name|'s |g.item['willtolive'].name|.  You hear the hum of his inner workings stutter and slow.")
                elif text_sanitized == "n":
                    print_desc("Too bad.  Some decisions are hard.  You take your |g.item['willtolive'].name|'s |g.item['willtolive'].name|.  You hear the hum of his inner workings stutter and slow.")
                print_desc("<p>\nHe won't last long now.")
                the_end_is_near = True
            else:
                print "I care about \"%s\".  You know what you need to do." % textinput
        else:
            end_turn_count += 1
            if text_sanitized.startswith("put feelings"):
                print "You can't put FEELINGS there."
            elif text_sanitized.startswith("get feelings"):
                print "You already have FEELINGS."
            elif text_sanitized.startswith("circuit boards"):
                print_desc("What do you want to do with the |g.item['circuit'].name|?")
            elif text_sanitized.startswith("put c"):
                print "I don't understand \"%s\"" % textinput
            elif text_sanitized == "what":
                print "What?"

            if end_turn_count == 2:
                print_desc("<p>\nYour |g.item['supervisor'].name| coughs.  His eyes are vacant, glassy.")
            elif end_turn_count == 6:
                print_desc("OK buddy, you sound really frustrated.  Slow it down.")
            elif end_turn_count == 8:
                print_desc("<p>\nYour |g.item['supervisor'].name|'s legs fail.  He crumples to the floor and looks up with sad resignation.  \"That's OK buddy, you tried,\" he says.")
            elif end_turn_count == 9:
                print_desc("<p>You put the |g.item['circuit'].name| into their |g.item['slots'].name| and push the DESTROY SWITCH.\n<p>A low rumble shakes the floor.  You hear the shriek of tearing metal.  Chunks of concrete and glass fall from high above, blanketing people, conveyor belts, widgets.<p><p><p>\nA hiss of depressurization, and you feel the kiss of cold air from outside.<p>\nYour |g.item['supervisor'].name| lies flat on his back, each breath rattling in his broken chest.<p>\nAs the dust clears, you see the ceiling is gone.  The moon is high and full in the night sky.<p>\nThere is still a fading light in your |g.item['supervisor'].name|'s eyes, which are now wide, and full of wonder and gratitude.<p><p><p>")
                static_images(g,"moon")
                animate_stars()
                process_action(g, "exit")
            

def process_action(g,textinput):
    # Actions. Look/Inspect/Go/Take/Eat
    # Action list
    class Action():
        def __init__(self):
            pass

    def __action_take(g,textinput,action):
        for match in action.matches:
            textinput = textinput.replace(match, "", 1).strip()
            break
        try:
            item = get_item(textinput)
            if not item:
                return
        except:
            print "How can you take '%s'?  I don't know what it is." % textinput
            return
        # Assume it's an Item
        if item.id not in g.player.inventory:
            if item.takeable:
                print "You take the %s%s." % (item.name,print_desc(item.taketext, output=False))
                g.player.inventory.append(item.id)
                if item.id == "feelings":
                    g.item['senseofself'].takeable = True
                if item.id == "senseofself":
                    g.item['willtolive'].takeable = True
                    end_game(g)
            else:
                print_desc(item.taketext)
        else:
            print "You can't take the %s because you already have it." % item.name
    
    def __action_drop(g,textinput,action):
        text = textinput.split()
        if len(text) > 1:
            itemname = " ".join(text[1:])
            try:
                item = g.item[itemname]
                if not item:
                    return
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
            item_name = textinput.replace(action, "", 1).strip()
            try:
                item = get_item(item_name)
            except:
                print "You don't see any '%s' here." % textinput
                return
            if action == "examine" and hasattr(item, 'examined'):
                print_desc(item.examined)
            else:
                print "You look at the %s.  %s" % (item.name, print_desc(item.description, output=False))
        # If no argument, it must be the room.  Use the short description
        else:
            room = g.rooms[g.player.room]
            if len(room.items) > 0:
                room_desc = room.shortdesc + room.itemstext
            else:
                room_desc = room.shortdesc
            print_desc(room_desc)
    
    def __action_inventory(g,textinput,action):
        print "You take stock of your possessions.  You are carrying the following:\n"
        if len(g.player.inventory) == 0:
            print "Nothing"
        else:
            for item in g.player.inventory:
                print "  ", g.item[item].name
    
    def __action_start(g,textinput,action):
        if len(textinput.split()) > 1:
            if g.player.room == "factory":
                print_desc("<p>.\n<p><p>..\n<p><p>...\n<p><p>A |g.item['widget'].name| emerges from a hole in the left column.  It moves along the conveyor belt and stops in front of you.\n The low whirr of the |g.item['belt'].name| has a pleasing rhythmic quality to it.  You can feel a song emerging just below your subconscious.")
                g.rooms[g.player.room].items.append('widget')
                g.item['widget'].visible = True
                g.rooms[g.player.room].running = True
            else:
                print "There's nothing here to start."
        else:
            print choice(["What do you want me to start?","You want to start something?"])
    
    def __action_go(g,textinput,action):
        # We actually only want exact matches for this action
        if textinput in action.matches:
            print "There are people at conveyor belts as far as the eye can see."
        else:
            print "I don't understand '%s.'" % textinput
    
    def __action_cant(g,textinput,action):
        print "You can't do that right now."
    
    def __action_quit(g,textinput,action):
        print "You can't quit now!  You haven't processed enough widgets yet!"
    
    def __action_show(g,textinput,action):
        text = " ".join(textinput.split()[1:])
        # Match robot picture action
        if any(x in text for x in g.item['supervisor'].matches) and any(x in text for x in g.item['picture'].matches):
            all_this_time(g)
            g.item['supervisor'].sadness = False
            print_desc("Your |g.item['supervisor'].name| blows his nose.  Looking up at a security camera, he says loudly, \"Now get back to those widgets!\"  He smiles with a faraway look in his eyes and whispers to you, \"I've never seen the moon.\"<p><p>He hands you a |g.item['bluepill'].name| and winks.")
            g.player.inventory.append('bluepill')
            g.item['bluepill'].visible = True
    
    def __action_eat(g,textinput,action):
        item = get_item(' '.join(textinput.split()[1:]))
        if item:
            print "You eat the %s." % item.name
            try:
                # No matter what it is, if you ate it then it shouldn't be in your inventory anymore.
                g.player.inventory.remove(item.id)
            except ValueError:
                pass

            if item.id == "picture":
                print_desc("<p><p>\n<p><p>\n<p><p>Your stomach begins to feel queasy.  Your pulse races.  Slowly, you feel the poisonous ink from |g.item['picture'].name| seeping into your blood.<p><p>\n\n***** YOU HAVE DIED *****\n\n\n")
                __action_exit(g,"death","eat")
            elif item.id == "redpill":
                print_desc("  Now you're energized!  Let's process some |g.item['widget'].name|S!")
            elif item.id == "bluepill":
                print bcolors.CYAN
                print_desc("W H O A\n.<p>..<p>...<p>Wow seriously dude.  You feel GREAT, just, like, super fuzzy but chill?  And you're all, sort of, ITCHY, but in your TEETH?\n<p>Your |g.item['supervisor'].name| makes that \"hang loose\" gesture and leans back.  \"Hey buddy, check this out.\"\n<p>A panel on his chest slides open.  There are three |g.item['circuit'].name|S that look like they might fit in some |g.item['slots'].name| next to a DESTROY SWITCH.\n<p>They are labeled FEELINGS, SENSE OF SELF, and WILL TO LIVE.\n<p>It's a good thing you're high on |g.item['bluepill'].name|, because removing these |g.item['circuit'].name| from your |g.item['supervisor'].name|'s chest will probably kill him.\n<p>The effects of the |g.item['bluepill'].name| are wearing off.\n<p>...")
                print bcolors.ENDC
                print_desc("<p>..<p>.<p>Uh oh.")
                g.item['feelings'].visible = True
                g.item['senseofself'].visible = True
                g.item['willtolive'].visible = True
            else:
                print "Nothing happens."
    
    def __action_count(g,textinput,action):
        item = get_item(' '.join(textinput.split()[1:]))
        if item:
            if item.id == "credit":
                credit_count = g.player.credits
                if credit_count < 32:
                    print 'Only %d credits so far.  You need to process more credits!' % credit_count
                elif 32 <= credit_count < 64:
                    print '%d credits!  Not bad.  Almost enough to entertain your goldfish, maybe.' % credit_count
                elif 64 <= credit_count < 128:
                    print "That's more like it!  With %s credits you can totally watch Bozo's Lament on your screen later." % credit_count
                elif 128 <= credit_count < 200:
                    print "You have %d credits!  You're going to watch the HECK out of an entertainment when you return to your pod's domicile tonight!" % credit_count
                elif 200 <= credit_count < 400:
                    print "Whoa, you have %d credits.  That's a lot of credits." % credit_count
                elif credit_count >= 400:
                    print "Alright, %d credits?  That's a stupid amount of credits." % credit_count
            else:
                print "I don't know how to count a", item.name, "."
        else:
            print "I don't know how to count that."

    def __action_process(g,textinput,action):
        if len(textinput.split()) <= 1:
            print "What do you want to process?"
        else:
            obj = " ".join(textinput.split()[1:])
            if obj == "widget":
                process_widget(g)
            elif obj == "all widgets":
                process_widget(g,_all=True)
            else:
                print "I don't know how to process that."
    
    def __action_boring(g,textinput,action):
        print "I know, right?"
    
    def __action_help(g,textinput,action):
        if len(textinput.split()) == 1:
            print "Type 'help <action>' to learn about your life."
        else:
            try:
                print g.actions[textinput.split()[1]].description
            except:
                print "You can't do that right now."
    
    def __action_exit(g,textinput,action):
        print "Thanks for playing.  You played for a total of %s moves, and your score was %s out of a possible %s." % (g.moves, g.points, g.points_total)
        sys.exit(0)

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
            "id"            : "start",
            "matches"       : [ "start", "turn on" ],
            "description"   : "Start the conveyor belt.",
            "run"           : __action_start
        },
        {
            "id"            : "count",
            "matches"       : [ "count" ],
            "description"   : "Useful in primitive cultures as well as advanced ones.",
            "run"           : __action_count
        },
        {
            "id"            : "process",
            "matches"       : [ "process" ],
            "description"   : "Work is work is work.",
            "run"           : __action_process
        },
        {
            "id"            : "boring",
            "matches"       : [ "boring" ],
            "description"   : "Work is work is work.",
            "run"           : __action_boring
        },
        {
            "id"            : "eat",
            "matches"       : [ "eat", "swallow", "devour", "chew" ],
            "description"   : "For eating pills, because that's awesome.",
            "run"           : __action_eat
        },
        {
            "id"            : "quit",
            "matches"       : [ "quit" ],
            "description"   : "Try to leave the game, the wrong way.",
            "run"           : __action_quit
        },
        {
            "id"            : "show",
            "matches"       : [ "show" ],
            "description"   : "For showing things.",
            "run"           : __action_show
        },
        {
            "id"            : "go",
            "matches"       : [ "go", "go north", "go south", "go east", "go west", "e", "w", "s", "n" ],
            "description"   : "For going into other rooms.  YMMV.",
            "run"           : __action_go
        },
        {
            "id"            : "nonono",
            "matches"       : [ "rip", "kill", "sing", "love" ],
            "description"   : "All the things you can't do in this game.",
            "run"           : __action_cant
        },
        {
            "id"            : "help",
            "matches"       : [ "help", "?" ],
            "description"   : "Prints an action's description.",
            "run"           : __action_help
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

    g.actions = actions
    
    if textinput is not "":
        action_exists = False
        for action in sorted(actions.keys(), key=len, reverse=True):
            if any(textinput.startswith(x) for x in actions[action].matches):
                actions[action].run(g,textinput,actions[action])
                action_exists = True
                break
        if not action_exists:
            print """I don't understand "%s".""" % textinput

def run_game(g):
    reset_game(g)
    while True:
        room = g.rooms[g.player.room]
        try:
            room.time_in_room += 1
            if room.time_in_room == room.hint_length + 1 and not room.running:
                print_desc(room.hint)
        except Exception as e:
            print "ERROR", e
            pass
        # The old games don't support awesome features like readline
        # or autocomplete, so I'm not going to do it here.
        textinput = raw_input("\n>")
        text_sanitized = " ".join([ x for x in textinput.lower().split() if x not in g.word_ignore ])
        process_action(g, text_sanitized)
        g.moves += 1

if __name__ == "__main__":
    animate_stars()
    sys.exit(0)
    g = Globals()
    static_images(g,"post")
    g.player = Player()
    # Only support pidgin English. Aooga.
    g.word_ignore = [ "the", "in", "to", "into", "on", "at", "a" ]
    run_game(g)
