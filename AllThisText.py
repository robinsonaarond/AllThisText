#! /usr/bin/env python

import time
import sys
import base64
from random import choice
from random import randint
from textwrap import wrap

class Globals():
    def __init__(self): 
        class Points():
            def count_points(self):
                total = 0
                for key, point in self.__dict__.items():
                    if point.done:
                        total += point.points
                return total
            def count_total_points(self):
                total = 0
                for key, point in self.__dict__.items():
                    total += point.points
                return total
                
            def __init__(self):
                class p():
                    done = False
                    points = 1
                # Point-worthy properties
                self.start_belt = p()
                self.eat_red_pill = p()
                self.credits_peon = p()
                self.credits_banker = p()
                self.credits_maniac = p()
                self.seeing_entertained = p()
                self.hearing_entertained = p()
                self.feeling_entertained = p()
                self.robot_picture = p()
                self.kill_robot = p()
                self.game_end = p()

                # Custom options for properties
                self.credits_banker.points = 4
                self.credits_maniac.points = 5
                self.game_end.points = 10

        self.moves            = 0
        self.points           = Points()
        self.points_total     = self.points.count_total_points()
        self.secrets_found    = 0
        self.total_secrets    = 0
        self.puzzles_solved   = 0
        self.total_puzzles    = 0
        self.sleep_interval   = 2.0
        self.item             = spawn_items()
        self.rooms            = spawn_rooms()
        self.screenon         = False
        self.accidentfreedays = 10700

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
        self.room             = "" # Either 'factory' or 'pod'
        self.credits          = 100
        self.daily_credits    = 0
        self.inventory        = []

class Item():
    def __init__(self):
        self.name        = ""
        self.description = ""
        self.location    = "player" # Can also be room, specified by id
        self.accessible  = True
        self.visible     = True     # Will not show up in LOOK command
        self.takeable    = True     # Can't be removed from room, displays taketext

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
        print((chr(27) + "[2J"))
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
        print(i)
        time.sleep(g.sleep_interval)
        time.sleep(g.sleep_interval)
        time.sleep(g.sleep_interval)
        print((chr(27) + "[2J"))
    elif img == "picture":
        i = """
****************************************************
****************************************************
**                        .            _          **
**  .                                 / |   .     **
**          .                         |_|         **
**                  .           .             .   **     
**                                                **
**            .           .           .           **
**                                                **
**   .           .          .                .    **
**                                                **
**        #### # # ###   # #   #   #   ## #       **
**         #   ### ##    ###  # # # #  # ##       **
**         #   # # ###   #  #  #   #   #  #       **
**                                                **
****************************************************
****************************************************

"""
        print(i)
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
                             .                                            
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
                .                                           .          """
        for line in i.splitlines():
            time.sleep(0.1)
            print(line)

def animate_stars():
    stars = [ "+", "*", "*", ".", ".", ".", "." ]
    for i in range(1,80):
        x = randint(1,80)
        y = randint(1,24)
        if (x < 37 and x > 65) or y > 14: 
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, choice(stars)))
            sys.stdout.flush()
            time.sleep(0.3)

# Statically generated list of all Items in the game in their initial state
def spawn_items():
    object_list = {}
    item_list = [
            {   
                "id"          : "picture", 
                "name"        : "PICTURE OF THE MOON", 
                "description" : "It is a picture of the moon.",
                "examined"    : "You see nothing special about |g.item['picture'].name|. |g.item['picture'].description|",
                "matches"     : [ "picture", "picture of the moon", "picture moon", "pic", "photo" ],
                "takeable"    : True,
                "taketext"    : ", and put it in your pocket",
            },
            {   
                "id"          : "credit", 
                "name"        : "CREDITS", 
                "description" : "These will make all the difference back at your pod.",
                "examined"    : "|g.item['credit'].name| are digital. You can't examine them.",
                "matches"     : [ "credit", "credits" ],
                "takeable"    : False,
                "taketext"    : "|g.item['credit'].name| are digital. You can't 'take' them.",
            },
            {   
                "id"          : "slots", 
                "name"        : "SLOTS", 
                "description" : "There are slots next to a switch. They look like they could hold something.",
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
                "examined"    : "It's an ordinary switch. Next to it is a label that says 'DESTROY'.",
                "matches"     : [ "switch", "destroy switch" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "It's bolted to the wall.",
            },
            {   
                "id"          : "supervisor", 
                "name"        : "ROBOT SUPERVISOR", 
                "description" : "He's your boss. Best be nice to him.",
                "examined"    : "|g.item['supervisor'].description|",
                "matches"     : [ "supervisor", "robot", "robot supervisor" ],
                "takeable"    : False,
                "visible"     : False,
                "sadness"     : False,
                "gaveredpill" : False,
                "taketext"    : "Your |g.item['supervisor'].name| doesn't look like he wants to be taken anywhere.",
            },
            {   
                "id"          : "redpill", 
                "name"        : "RED PILL", 
                "description" : "The pill is small, red, and clear. Its contents look something like blood.",
                "examined"    : "|g.item['redpill'].description|",
                "matches"     : [ "red pill", "redpill", "red" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "",
            },
            {   
                "id"          : "bluepill", 
                "name"        : "BLUE PILL", 
                "description" : "The pill is small, blue, and milky. Its contents look something like happiness.",
                "examined"    : "|g.item['bluepill'].description|",
                "matches"     : [ "blue pill", "bluepill", "blue" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "",
            },
            {   
                "id"          : "circuit", 
                "name"        : "CIRCUIT BOARDS", 
                "description" : "They're circuit boards. They look like they go in something.",
                "examined"    : "You examine them but you really don't know much about electronics. Widgets, on the other hand... actually, you don't know much about those either.",
                "matches"     : [ "circuit", "circuits", "circuit boards" ],
                "takeable"    : False,
                "taketext"    : "How would you take them?  They're part of the wall.",
            },
            {   
                "id"          : "feelings", 
                "name"        : "FEELINGS", 
                "description" : "It's a circuit board. It is labeled FEELINGS.",
                "examined"    : "You examine them but you really don't know much about FEELINGS.",
                "matches"     : [ "feelings", "feelings circuit board", "feels" ],
                "visible"     : False,
                "taketext"    : "  I mean, he's a robot right?  They're probably not even real feelings",
            },
            {   
                "id"          : "senseofself", 
                "name"        : "SENSE OF SELF", 
                "description" : "It's a circuit board. It is labeled SENSE OF SELF.",
                "examined"    : "You examine them but you really don't know much about yourself. Or any self, really.",
                "matches"     : [ "sense of self", "sense self" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "The |g.item['senseofself'].name| is blocked by the |g.item['feelings'].name|. You'll have to take that one first.",
            },
            {   
                "id"          : "willtolive", 
                "name"        : "WILL TO LIVE", 
                "description" : "It's a circuit board. It is labeled WILL TO LIVE.",
                "examined"    : "You think about your own WILL TO LIVE. Is is pre-programmed in like this?",
                "matches"     : [ "will to live", "will live", "live" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "The |g.item['willtolive'].name| is blocked by the |g.item['senseofself'].name|. You'll have to take that one first.",
            },
            {   
                "id"          : "widget", 
                "name"        : "WIDGET",
                "description" : "You see nothing special about the |g.item['widget'].name|. It is a widget.",
                "examined"    : "It is a standard widget, ready for processing.",
                "matches"     : [ "widget" ],
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "You can't take the |g.item['widget'].name|.",
            },
            {
                "id"          : "opening",
                "name"        : "CONVEYOR BELT OPENING",
                "matches"     : [ "opening" ],
                "description" : "It looks like something small could appear out of that opening at any moment.",
                "takeable"    : False,
                "visible"     : False,
                "taketext"    : "You can't take an opening.",
            },
            {
                "id"          : "screen",
                "name"        : "SCREEN",
                "matches"     : [ "screen", "display", "monitor" ],
                "description" : "Your 15-inch flat panel screen. On the bottom left there is a button.",
                "takeable"    : False,
                "powered"     : False,
                "taketext"    : "It is mounted to the wall.",
            },
            {
                "id"          : "fooddispenser",
                "name"        : "FOOD DISPENSER",
                "matches"     : [ "dispenser", "food dispenser" ],
                "description" : "Your 10-inch food dispenser. On the bottom left there is a button.",
                "takeable"    : False,
                "powered"     : False,
                "taketext"    : "It is mounted to the wall.",
            },
            {
                "id"          : "food",
                "name"        : "FOOD CUBE",
                "matches"     : [ "food", "food cube" ],
                "description" : "Your 10-inch food dispenser. On the bottom left there is a button.",
                "powered"     : False,
                "taketext"    : "",
            },
            {
                "id"          : "belt",
                "name"        : "CONVEYOR BELT",
                "matches"     : [ "conveyor", "belt", "conveyor belt" ],
                "description" : "The belt stretches onward to the right. On the left side is an opening.",
                "takeable"    : False,
                "taketext"    : "Moving the CONVEYOR BELT would require a TEAM LIFT, and currently no one is available to help."
            }
        ]
    for item in item_list:
        obj = Item()
        for k, v in list(item.items()):
            setattr(obj, k, item[k])
        object_list[item['id']] = obj
    return object_list

def spawn_rooms():
    object_list = {}
    room_list = [
            {
                "id"          : "factory",
                "name"        : "Factory Floor",
                "description" : "You are in a factory.<n><n>It's an enormous room. If there are walls, they're too far away for you to make out. You assume there is a ceiling somewhere above you, but when you look up, you see only an impenetrable darkness.<n><n>In front of you is a short |g.item['belt'].name| that stretches between two columns. There are other people standing at similar conveyor belts all around you, in all directions, as far as the eye can see.<p><n><n>In your hand is a |g.item['picture'].name|.",
                "shortdesc"   : "You are on the factory floor. It's an enormous room. You see a |g.item['belt'].name| in front of you.",
                "exits"       : { "n": None, "s": None, "e": "boiler", "w": None },
                "hint"        : "<n><p>(There is a conveyor belt though. It is stopped.)",
                "hint_length" : 6,
                "running"     : False,
                "items"       : [],
                "itemstext"   : "  You also see: |', '.join([g.item[x].name for x in g.rooms[g.player.room].items if g.item[x].visible])|."
            },
            {
                "id"          : "pod",
                "name"        : "Your Domicile",
                "description" : "You are in your pod.<n><n>One entire wall is taken up by your 15-inch |g.item['screen'].name|; a real upgrade from the last one. You are sitting in your chair/bed combo as there is no room to stand.<n><n>To your right is a small platform with your |g.item['fooddispenser'].name|. On the wall to your left is a small picture of a goldfish, swimming in a bowl.",
                "shortdesc"   : "The POD is everything you could possibly need. Why would you go anywhere else?  Oh right, credits.",
                "hint_length" : 6,
                "running"     : False,
                "hint"        : "<n>The SCREEN is powered off. Maybe try powering it on?",
                "items"       : [ "screen" ],
                "itemstext"   : "  You also see: |', '.join([g.item[x].name for x in g.rooms[g.player.room].items if g.item[x].visible])|."
            }
        ]
    for room in room_list:
        obj = Room()
        for k, v in list(room.items()):
            setattr(obj, k, room[k])
        object_list[room['id']] = obj
    return object_list

def print_desc(room_desc, output=True):
    room_sanitized = []
    # Parse out the template code
    # Currently you can:
    #   put pauses in the dialog using <p>
    #   put newlines in the dialog using <n>
    #   put actual code wrapped in ||, e.g. |g.player.name|
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
        # Parse <p> markup for pauses, <n> for newlines
        if "<p>" in desc:
            for line in desc.split("<p>"):
                time.sleep(g.sleep_interval)
                if line:
                    for l in line.replace('<n>', '\n').split('\n'):
                        print('\n'.join(wrap(l)))
        else:
            print('\n'.join(wrap(desc.replace('<n>', '\n'))))
    else:
        return desc

def enter_room(g):
    room = g.rooms[g.player.room]
    room_desc = room.description
    room.time_in_room = 0
    if len(room.items) > 0:
        v = []
        for i in room.items:
            if g.item[i].visible:
                v.append(i)
        if len(v) > 0:
            room_desc = room_desc + room.itemstext
    print_desc(room_desc)

def reset_game(g):
    g.player.room = "factory"
    g.player.name = ""
    g.player.inventory = [ 'picture' ]
    g.item['picture'].damaged = False
    enter_room(g)

def all_this_time(g):
    print_desc("Your |g.item['supervisor'].name| sees the |g.item['picture'].name| and immediately begins to cry. He sings a little tune. You feel the song of the |g.item['belt'].name| opening in your mind like the bloom of a... flower?  Whatever _that_ is. His words merge with the song.<p><p><n><n>All we'll have is<p>All this time<p>All we'll have is<p>All this time<p>All this time<n>")

def get_item(textinput):
    # Generate list of matchable items and their corresponding id
    available_items = []
    item = None
    for k, i in g.item.items():
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
            print_desc("You don't see any %s here." % textinput)
            return None
    else:
        print_desc("You don't see any %s here." % textinput)
        return item

def get_action(g, textinput):
    if textinput != "":
        action_exists = False
        for action in sorted(list(g.actions.keys()), key=len, reverse=True):
            for match in g.actions[action].matches:
                # Most single-character actions should be an exact match
                if len(match) == 1 and match not in [ "l" ]:
                    if textinput == match:
                        print("Match is single character", match)
                        action_exists = True
                elif textinput.startswith(match):
                    action_exists = True
                if action_exists:
                    return g.actions[action]
        if not action_exists:
            print("""I don't know how to "%s".""" % textinput)
            return None

def process_widget(g,_all=False):
    if g.item['widget'].visible:
        if not _all:
            if g.item['supervisor'].visible and not "redpill" in g.player.inventory and g.item['supervisor'].gaveredpill == False:
                g.player.credits += 8
                g.player.daily_credits += 8
                print_desc("Too late!  Your |g.item['supervisor'].name| grips your shoulder. \"Hey there buddy!,\" he says, \"Seems like you got a little distracted!  Maybe time to take a |g.item['redpill'].name|!\"")
                g.item['redpill'].visible = True
                g.item['supervisor'].gaveredpill = True
                g.player.inventory.append('redpill')
                g.rooms['factory'].shortdesc = "You idly look at stuff. There it is. Bunch of stuff.<p>Your |g.item['supervisor'].name| sighs again, but this time it comes out as a little moan."
            else:
                print_desc("You process the |g.item['widget'].name|. You earn 8 |g.item['credit'].name|! Another |g.item['widget'].name| appears.")
                g.player.credits += 8
                g.player.daily_credits += 8
        else:
            if g.item['supervisor'].visible:
                print_desc("You mindlessly process |g.item['widget'].name|S. Your |g.item['supervisor'].name| sighs. \"Good job buddy. You're really earning some credits I guess.\"")
                g.item['supervisor'].sadness = True
                g.item['supervisor'].description = "Your |g.item['supervisor'].name| looks miserable. He stares bleakly into the middle distance."
            g.player.credits += 64
            g.player.daily_credits += 64

        if g.player.credits >= 48 and not g.item['supervisor'].visible:
            print_desc("You mindlessly process widgets. Your thoughts begin to wander.<n><p><p>You think about what entertainment you will watch when you return to your pod's domicile.<n><p>You notice a |g.item['switch'].name| on the wall that's labeled \"Destroy.\"  Next to it are three empty |g.item['slots'].name| that look like they hold |g.item['circuit'].name|.<n><p><p>Oh No! You stopped processing |g.item['widget'].name|S and your |g.item['supervisor'].name| is right behind you!")
            g.item['slots'].visible = True
            g.item['switch'].visible = True
            g.item['supervisor'].visible = True

        if g.player.daily_credits >= 200:
            print_desc("You've really processed a lot of |g.item['widget'].name|S.<p>Your |g.item['supervisor'].name| sighs again, and stands up.<p><n>\"Alright, buddy, you've earned enough credits for today.<p>Why don't you head on home?\"<p><n><p>Satisfied with a full day's work, you head to your POD.<p><n>")

            # Me trying my best to revert all state in the factory so you can try again the next day without stuff being messed up
            g.rooms["factory"].running = False
            try:
                g.rooms[g.player.room].items.remove('widget')
            except:
                pass
            g.item['widget'].visible = False
            g.player.room = "pod"
            g.item['slots'].visible = False
            g.item['switch'].visible = False
            g.item['supervisor'].visible = False
            g.item['supervisor'].sadness = False
            g.item['redpill'].visible = False
            g.rooms['factory'].shortdesc = "You are on the factory floor. It's an enormous room. You see a |g.item['belt'].name| in front of you."
            g.item['supervisor'].gaveredpill = False
            enter_room(g)
        
        if g.player.credits > 2000:
            g.points.credits_maniac.done = True
        if g.player.credits > 1000:
            g.points.credits_banker.done = True
        elif g.player.credits >= 100:
            g.points.credits_peon.done = True
    else:
        print_desc("You can't see any widgets.")

def end_game(g):
    print_desc("<p><n>Your |g.item['supervisor'].name| winces. Wait, do they feel pain?")
    the_end_is_near = False
    end_turn_count = 0

    # Note: https://xkcd.com/1378/ about this wall of conditionals
    while True:
        g.moves += 1
        textinput = input("\n>")
        text_sanitized = " ".join([ x for x in textinput.lower().split() if x not in g.word_ignore ])
        if not the_end_is_near:
            if textinput == "" and all(x in g.player.inventory for x in ['feelings','senseofself']):
                print("COME ON. DO IT.")
            elif text_sanitized == "":
                pass
            elif text_sanitized in ["take will to live","take will  live","take will","take will live"] and "willtolive" not in g.player.inventory and g.item['willtolive'].takeable == True:
                print_desc("Wow. OK, but this may kill your |g.item['supervisor'].name|. Are you sure? (y/n)")
                g.player.inventory.append("willtolive")
            elif "willtolive" in g.player.inventory and text_sanitized in [ "y", "n" ]:
                if text_sanitized == "y":
                    print_desc("You take your |g.item['supervisor'].name|'s |g.item['willtolive'].name|. You hear the hum of his inner workings stutter and slow.")
                elif text_sanitized == "n":
                    print_desc("Too bad. Some decisions are hard. You take your |g.item['supervisor'].name|'s |g.item['willtolive'].name|. You hear the hum of his inner workings stutter and slow.")
                print_desc("<p><n>He won't last long now.")
                the_end_is_near = True
            else:
                print("I don't care about \"%s\". You know what you need to do." % textinput)
        else:
            end_turn_count += 1
            if text_sanitized.startswith("put feelings"):
                print("You can't put FEELINGS there.")
            elif text_sanitized.startswith("get feelings"):
                print("You already have FEELINGS.")
            elif text_sanitized.startswith("circuit boards"):
                print_desc("What do you want to do with the |g.item['circuit'].name|?")
            elif text_sanitized.startswith("put c"):
                print("I don't understand \"%s\"" % textinput)
            elif text_sanitized == "what":
                print("What?")

            if end_turn_count == 2:
                print_desc("<p><n>Your |g.item['supervisor'].name| coughs. His eyes are vacant, glassy.")
            elif end_turn_count == 6:
                print_desc("OK buddy, you sound really frustrated. Slow it down.")
            elif end_turn_count == 8:
                print_desc("<p><n>Your |g.item['supervisor'].name|'s legs fail. He crumples to the floor and looks up with sad resignation. \"That's OK buddy, you tried,\" he says.")
            elif end_turn_count == 9:
                print_desc("<p>You put the |g.item['circuit'].name| into their |g.item['slots'].name| and push the DESTROY SWITCH.<n><p>A low rumble shakes the floor. You hear the shriek of tearing metal. Chunks of concrete and glass fall from high above, blanketing people, conveyor belts, widgets.<p><n>The |g.item['belt'].name| in front of you shuts down suddenly, but the song in your mind is louder than ever.<p><p><n>A hiss of depressurization, and you feel the kiss of cold air from outside.<p><n>Your |g.item['supervisor'].name| lies flat on his back, each breath rattling in his broken chest.<p><p>As the dust clears, you see the ceiling is gone. The moon is high and full in the night sky.<p><n>There is still a fading light in your |g.item['supervisor'].name|'s eyes, which are now wide, and full of wonder and gratitude.<p><p>")
                g.accidentfreedays = 0
                static_images(g,"moon")
                animate_stars()
                print_desc("As the song dies away, and you gaze at the moon in the sky, you realize you've reached...<p><p><n><n>THE END<n><p>")
                g.points.game_end.done = True
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
            print("How can you take '%s'?  I don't know what it is." % textinput)
            return
        # Assume it's an Item
        if item.id not in g.player.inventory:
            if item.takeable:
                print("You take the %s%s." % (item.name,print_desc(item.taketext, output=False)))
                g.player.inventory.append(item.id)
                if item.id in g.rooms[g.player.room].items:
                    g.rooms[g.player.room].items.remove(item.id)
                if item.id == "feelings":
                    g.item['senseofself'].takeable = True
                    g.item['senseofself'].taketext = " . Sure, why not?  You take, and you take, and you take. Because you're a winner"
                if item.id == "senseofself":
                    g.item['willtolive'].takeable = True
                    g.item['willtolive'].taketext = ""
                    end_game(g)
            else:
                print_desc(item.taketext)
        else:
            print("You can't take the %s because you already have it." % item.name)
    
    def __action_drop(g,textinput,action):
        text = textinput.split()
        if all([x in ["drop", "picture", "opening"] for x in text]):
            if "picture" in g.player.inventory and g.item['opening'].visible:
                print_desc("You stuff the |g.item['picture'].name| into the |g.item['opening'].name|.")
                g.player.inventory.remove("picture")
                g.rooms['factory'].items.append("picture")
                g.item['picture'].visible = False
                return
        if len(text) > 1:
            itemname = " ".join(text[1:])
            try:
                item = g.item[itemname]
                if not item:
                    return
            except:
                print("I'm not sure what '%s' even is, let alone know how to drop it." % itemname)
                return
            if itemname in g.player.inventory:
                print("You drop the %s." % g.item[itemname].name)
                g.player.inventory.remove(itemname)
                g.rooms[g.player.room].items.append(itemname)
            else:
                print("You don't actually have the %s" % g.item[itemname].name)
        else:
            print("What do you want me to drop?")
    
    def __action_look(g,textinput,action):
        # If there is an argument, it must be an object
        if len(textinput.split()) >= 2:
            action = textinput.split()[0]
            item_name = textinput.replace(action, "", 1).strip()
            item = get_item(item_name)
            if item:
                if item.id == "belt":
                    g.item['opening'].visible = True
                if action == "examine" and hasattr(item, 'examined'):
                    print_desc(item.examined)
                else:
                    print_desc("You look at the %s. %s" % (item.name, print_desc(item.description, output=False)))
        # If no argument, it must be the room. Use the short description
        else:
            room = g.rooms[g.player.room]
            room_desc = room.shortdesc
            if len(room.items) > 0:
                v = []
                for i in room.items:
                    if g.item[i].visible:
                        v.append(i)
                if len(v) > 0:
                    room_desc = room.shortdesc + room.itemstext
                else:
                    room_desc = room.shortdesc
            else:
                room_desc = room.shortdesc
            print_desc(room_desc)
    
    def __action_inventory(g,textinput,action):
        print("You take stock of your possessions. You are carrying the following:\n")
        if len(g.player.inventory) == 0:
            print("Nothing")
        else:
            for item in g.player.inventory:
                print("  ", g.item[item].name)

    def __action_allen(g,textinput,action):
        print("Entering GBF Headquarters\n")
        allen_game()
    
    def __action_start(g,textinput,action):
        if len(textinput.split()) > 1:
            if g.player.room == "factory" and any(x in textinput for x in ["belt","conv"]):
                if "picture" in g.rooms["factory"].items and g.item['picture'].visible == False:
                    print_desc("<p><n>As the belt starts to roll, a small |g.item['picture'].name| suddenly pops out, gives a little twirl mid-air, and slowly flutters down to the floor.")
                    g.item['picture'].description = "It is a picture of the moon. It has been creased slightly."
                    g.item['picture'].visible = True
                    g.item['picture'].damaged = True
                print_desc("<p>.<n><p>..<n><p>...<n><p>A |g.item['widget'].name| emerges from a hole in the left column. It moves along the conveyor belt and stops in front of you.<n> The low whirr of the |g.item['belt'].name| has a pleasing rhythmic quality to it. You can feel a song emerging just below your subconscious.")
                g.points.start_belt.done = True
                g.rooms[g.player.room].items.append('widget')
                g.item['widget'].visible = True
                g.rooms[g.player.room].running = True
            elif g.player.room == "pod" and "screen" in textinput:
                #__action_power(g,textinput,action)
                print("You turn on the screen.")
                g.screenon = True
            else:
                print("There's nothing here to start.")
        else:
            print(choice(["What do you want me to start?","You want to start something?"]))
    
    def __action_go(g,textinput,action):
        # We actually only want exact matches for this action
        if textinput in action.matches:
            print("There are people at conveyor belts as far as the eye can see.")
        else:
            print("I don't understand '%s.'" % textinput)
    
    def __action_cant(g,textinput,action):
        print("You can't do that right now.")
    
    def __action_quit(g,textinput,action):
        print("You can't quit now!  You haven't processed enough widgets yet!")
    
    def __action_show(g,textinput,action):
        text = " ".join(textinput.split()[1:])
        # Match robot picture action
        if any(x in text for x in g.item['supervisor'].matches) and any(x in text for x in g.item['picture'].matches):
            all_this_time(g)
            g.points.robot_picture.done = True
            g.item['supervisor'].sadness = False
            print_desc("Your |g.item['supervisor'].name| blows his nose. Looking up at a security camera, he says loudly, \"Now get back to those widgets!\"  He smiles with a faraway look in his eyes and whispers to you, \"I've never seen the moon.\"<p>He hands you a |g.item['bluepill'].name| and winks.")
            g.player.inventory.append('bluepill')
            g.item['bluepill'].visible = True
    
    def __action_eat(g,textinput,action):
        item = get_item(' '.join(textinput.split()[1:]))
        if item:
            if item.id in g.player.inventory:
                print("You eat the %s." % item.name)
                try:
                    # No matter what it is, if you ate it then it shouldn't be in your inventory anymore.
                    g.player.inventory.remove(item.id)
                except ValueError:
                    pass

                if item.id == "picture":
                    print_desc("<p>.<n><p>..<p><n><n>Your stomach begins to feel queasy. Your pulse races. Slowly, you feel the poisonous ink from |g.item['picture'].name| seeping into your blood.<p><n><n>***** YOU HAVE DIED *****<n><n>")
                    __action_exit(g,"death","eat")
                elif item.id == "redpill":
                    print_desc("  Now you're energized!  Let's process some |g.item['widget'].name|S!<p><n>The song below your subconscious seems to grow louder.")
                    g.points.eat_red_pill.done = True
                elif item.id == "bluepill":
                    print(bcolors.CYAN)
                    print_desc("W H O A<n>.<p>..<p>...<p>Wow seriously dude. You feel GREAT, just, like, super fuzzy but chill?  And you're all, sort of, ITCHY, but in your TEETH?<n><p>Your |g.item['supervisor'].name| makes that \"hang loose\" gesture and leans back. \"Hey buddy, check this out.\"<n><p><p>panel on his chest slides open. There are three |g.item['circuit'].name| that look like they might fit in some |g.item['slots'].name| next to a DESTROY SWITCH.<n><p>They are labeled FEELINGS, SENSE OF SELF, and WILL TO LIVE.<n><p><p>'s a good thing you're high on |g.item['bluepill'].name|, because removing these |g.item['circuit'].name| from your |g.item['supervisor'].name|'s chest will probably kill him.<n><p>The effects of the |g.item['bluepill'].name| are wearing off.<n><p>...")
                    print(bcolors.ENDC)
                    print_desc("<p>..<p>.<p>Uh oh.")
                    g.item['feelings'].visible = True
                    g.item['senseofself'].visible = True
                    g.item['willtolive'].visible = True
                else:
                    print("Nothing happens.")
            else:
                print("You aren't carrying it.")

    def __action_speed(g,textinput,action):
        speed_amount = ' '.join(textinput.split()[1:])
        if speed_amount in ('0','1','2'):
            g.sleep_interval = float(speed_amount)
        else:
            print("Only speeds supported are 0, 1, or 2 (Default)")
    
    def __action_count(g,textinput,action):
        item = get_item(' '.join(textinput.split()[1:]))
        if item:
            if item.id == "credit":
                credit_count = g.player.credits
                if credit_count < 32:
                    print('Only %d credits so far. You need to process more credits!' % credit_count)
                elif 32 <= credit_count < 200:
                    print('%d credits!  Not bad. Almost enough to entertain your goldfish, maybe.' % credit_count)
                elif 200 <= credit_count < 400:
                    print("That's more like it!  With %s credits you can totally watch Bozo's Lament on your screen later. Again." % credit_count)
                elif 400 <= credit_count < 600:
                    print("You have %d credits!  You're going to watch the HECK out of an entertainment when you return to your pod's domicile tonight!" % credit_count)
                elif 600 <= credit_count < 1500:
                    print("Whoa, you have %d credits. That's a lot of credits." % credit_count)
                elif credit_count >= 1500:
                    print("Alright, %d credits?  That's a stupid amount of credits." % credit_count)
            else:
                print("I don't know how to count a", item.name, ".")
        else:
            print("I don't know how to count that.")

    def __action_process(g,textinput,action):
        if len(textinput.split()) <= 1:
            print("What do you want to process?")
        else:
            obj = " ".join(textinput.split()[1:])
            if obj == "widget":
                process_widget(g)
            elif obj == "all widgets":
                process_widget(g,_all=True)
            else:
                print("I don't know how to process that.")
    
    def __action_boring(g,textinput,action):
        print("I know, right?")

    def __action_enterscreen(g,textinput,action):
        seeing_entertainments = [ 
            "You watch 57 minutes of static. Might have been 58.",
            "You watch a riveting tale about a youngling who, after much hardship and trial, achieves their lifelong dream of working at the CONVEYOR BELT.",
            "You watch a young and depressed vampire who doesn't like their dark and cloudy week.",
            "You watch a couple go to Las Vegas in a $20,000 car and come back in a $200,000 Greyhound bus.",
            "You watch an old man sit around and play solitaire all weekend.",
            "You watch a group of teenagers hang out at the mall, eat junk food, and make their mothers ashamed of them.",
            "You watch an aspiring capitalist tycoon pop by his colleague's office down the hall to discuss potential meal plans",
            "You watch how a young extraterrestrial, separated from its family and stranded on Earth, finds friendship with a boy in a wheelchair, who really likes french fries for some reason.",
            "You watch an entertainment depicting a world where water is controlled by the Protectorate. Some orphan/inmates run away from their orphanage jail with a glowing ball to break a dam and free the water.",
            "You watch some dots slowly populate on your screen. Just a few more now...",
            "You observe a small snake as it goes through life, eating apples and growing until it fills the earth.",
            ]
        listening_entertainments = [ 
            "The soothing whir of the contralto female auto-generated voice both filled and thrilled you. It was a TRIUMPH.",
            "You listen to a striking commentary on the wolfishness of the earth, complete with a running score. Me: 0  Big Bad World: 1",
            "You listen to John Cage's 4:33. Archaelogists believe it was also known by the alternate name 'The Sound of Silence.'",
            "You hear a flurry of beeps and boops and an electronic scratching sound. Finally you hear the words 'Welcome. You've got mail.'  You wonder again just what mail is, exactly.", 
            ]

        def _guess_a_number():
            guess_count = 0
            current_guess = 0
            answer = randint(1,100)
            print("Guess a number between 1 and 100 (5 credits per guess)")
            print("Guess in less than 5 and win 50 credits!.")
            while current_guess != answer:
                textinput = input("\nGuess: ")
                guess_count += 1
                if textinput == "quit":
                    print("Maybe next time!")
                    break
                g.player.credits -= 5
                current_guess = int(textinput)
                if current_guess < 1 or current_guess > 100:
                    print("Smart aleck.")
                # 42 is the answer
                if current_guess == answer or current_guess == 42:
                    print("You win!")
                    if guess_count < 5:
                        print("Wicked fast! Have 50 credits.")
                        g.player.credits += 50
                    break
                else:
                    if current_guess < answer:
                        print("Guess was too low. Try again.")
                    elif current_guess > answer:
                        print("Guess was too high. Try again.")
            if g.player.credits == 0:
                print("Alright, I guess you're done guessing. Get some more credits and try again.")
        def _out_of_credits():
            print_desc("You're out of credits. Maybe it's time to go to sleep; get yourself ready for another day at work.<p>")

        def _process_choice(g,c):
            if c == 1:
                if g.player.credits >= 50:
                    print("Seeing ENTERTAINMENTS are the best.")
                    g.player.credits -= 50
                    time.sleep(g.sleep_interval)
                    print_desc("<p>.<p>..<p>")
                    print(choice(seeing_entertainments))
                    print_desc("<p>..<p>.<p>Your ENTERTAINMENT is complete.<p>")
                    g.points.seeing_entertained.done = True
                else:
                    _out_of_credits()
            elif c == 2:
                if g.player.credits >= 20:
                    g.player.credits -= 20
                    print("You lean back.")
                    print_desc("<p>.<p>..<p>")
                    print(choice(listening_entertainments))
                    print_desc("<p>..<p>.<p>Your ENTERTAINMENT is complete.<p>")
                    g.points.hearing_entertained.done = True
                else:
                    _out_of_credits()
            elif c == 3:
                if g.player.credits >= 250:
                    g.player.credits -= 250
                    print_desc("<p>.<p>..<p>")
                    print("Whoa.")
                    print_desc("<p>..<p>.<p>Your ENTERTAINMENT is complete.<p>")
                    g.points.feeling_entertained.done = True
                else:
                    _out_of_credits()
            elif c == 4:
                if g.player.credits >= 10:
                    g.player.credits -= 10
                    _guess_a_number()
                else:
                    _out_of_credits()
            elif c == 5:
                if g.player.credits >= 25:
                    g.player.credits -= 25
                    if g.item['picture'].damaged == True:
                        print_desc("You place |g.item['picture'].name| in front of the screen, and a bright blue beam shoots out and scans the image.<p>.<p>..<p>The light seems to be struggling on the damaged portion of the picture. Now something completely different is coming up:<p><n><p>")
                        allen_game()
                    else:
                        print_desc("You place |g.item['picture'].name| in front of the screen, and a bright blue beam shoots out and scans the image.<p>Here it is:")
                        static_images(g,"picture")
                else:
                    _out_of_credits()
            elif c == 6:
                stats = "\n".join(["DAYS SINCE LAST ACCIDENT:  %d",
                                "CREDITS EARNED TODAY:      %d",
                                "CREDITS TOTAL:             %d",
                                "SCORE (SO FAR/TOTAL):      %s",
                                "IN-GAME MOVES:             %d"])
                print(stats % (g.accidentfreedays, 
                               g.player.daily_credits, 
                               g.player.credits, 
                               str(g.points.count_points()) + "/" + str(g.points_total), 
                               g.moves))
            elif c == 7:
                print_desc("It's been a long day. Time for a well-deserved rest. You turn off your screen and lay...<p>down...<p>...to sleep.<p>Alright, it's a new day. You go to the factory floor.<p><n>")
                g.screenon = False
                g.accidentfreedays += 1
                g.player.daily_credits = 0
                g.player.room = "factory"
                enter_room(g)

        opening_screen = "\n".join(["Welcome to your pod's entertainment system.",
                                    "Select from the following options:",
                                    "",
                                    " (1) - Have a seeing ENTERTAINMENT (50 credits)",
                                    " (2) - Have a listening ENTERTAINMENT (20 credits)",
                                    " (3) - Have a feeling ENTERTAINMENT (250 credits)",
                                    " (4) - Have an interactive ENTERTAINMENT (10 credits)",
                                    " (5) - Scan PICTURE (25 credits)",
                                    " (6) - Statistics (Free)",
                                    " (7) - Sleep (Free)"])

        if g.rooms[g.player.room].id == "pod":
            if g.screenon:
                while g.rooms[g.player.room].id == "pod":
                    g.moves += 1
                    print(opening_screen)
                    textinput = input("\nSelect 1-7: ")
                    try:
                        c = int(textinput)
                        if 7 >= c >= 1:
                            _process_choice(g,c)
                        else:
                            print("You müssen select a number from 1 to 6")
                            time.sleep(g.sleep_interval)
                    except Exception as e:
                        print("You must select a number from 1 to 6")
                        #print(e)
                        time.sleep(g.sleep_interval)
                g.screenon = False
            else:
                print_desc("The |g.item['screen'].name| is off.")
        else:
            print("You can't do that here.")
    
    def __action_help(g,textinput,action):
        if len(textinput.split()) == 1:
            print("Type 'help <action>' to learn about your life.")
        else:
            try:
                action = get_action(g,textinput.split()[1])
                if action:
                    print(action.description)
            except Exception as e:
                print("You can't do that right now.")
                #print(e)
    
    def __action_exit(g,textinput,action):
        print("Thanks for playing. You played for a total of %s moves, and your score was %s out of a possible %s." % (g.moves, g.points.count_points(), g.points_total))
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
            "matches"       : [ "start", "turn on", "power on", "turn", "power" ],
            "description"   : "For starting stuff.",
            "run"           : __action_start
        },
        {
            "id"            : "count",
            "matches"       : [ "count" ],
            "description"   : "Useful in primitive cultures as well as advanced ones.",
            "run"           : __action_count
        },
        {
            "id"            : "speed",
            "matches"       : [ "speed" ],
            "description"   : "For those who don't want to wait.  Choose 0, 1, or 2",
            "run"           : __action_speed
        },
        {
            "id"            : "allengame",
            "matches"       : [ "thereisnocowlevel" ],
            "description"   : "Show me the money!",
            "run"           : __action_allen
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
            "matches"       : [ "quit", "logout" ],
            "description"   : "Try to leave the game, the wrong way. (The right way is 'exit')",
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
            "matches"       : [ "go", "go north", "go south", "go east", "go west", "go n", "go s", "go e", "go w", "n", "s", "e", "w" ],
            "description"   : "For going into other rooms. YMMV.",
            "run"           : __action_go
        },
        {
            "id"            : "action",
            "matches"       : [ "action", "<action>" ],
            "description"   : "Don't be a smart aleck.",
            "run"           : __action_cant
        },
        {
            "id"            : "nonono",
            "matches"       : [ "rip", "kill", "sing", "love", "block" ],
            "description"   : "All the things you can't do in this game.",
            "run"           : __action_cant
        },
        {
            "id"            : "screen",
            "matches"       : [ "screen", "enter", "enter screen", "log into screen", "log in", "press enter", "read screen" ],
            "description"   : "Log into your SCREEN.",
            "run"           : __action_enterscreen
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
            "description"   : "Leave the game forever. Actually you can play again at any time.",
            "run"           : __action_exit
        }
    ]
    for action in action_dict:
        obj = Action()
        for k, v in list(action.items()):
            setattr(obj, k, action[k])
        actions[action['id']] = obj

    g.actions = actions
    
    a = get_action(g,textinput)
    if a is not None:
        try:
            a.run(g,textinput,a)
        except Exception as e:
            #print(e)
            print("What's the point?")

def run_game(g):
    reset_game(g)
    while True:
        room = g.rooms[g.player.room]
        try:
            room.time_in_room += 1
            if room.id == "factory" and room.time_in_room == room.hint_length + 1 and not room.running:
                print_desc(room.hint)
        except Exception as e:
            print("ERROR", e)
            pass
        # The old games don't support awesome features like readline
        # or autocomplete, so I'm not going to do it here.
        textinput = input("\n>")
        text_sanitized = " ".join([ x for x in textinput.lower().split() if x not in g.word_ignore ])
        process_action(g, text_sanitized)
        g.moves += 1

###
#  Easter Egg
###

game_function = \
"ZGVmIGFsbGVuX2dhbWUoKToKICAgICMjCiAgICAjIEFsbGVuJ3MgYXdlc29tZSBnYW1lCiAgICAjIwoKICAgIGNsYXNzIFBsYWNlKCk6CiAgICAgICAgZGVmIF9faW5pdF9fKHNlbGYpOgogICAgI" \
"CAgICAgICBzZWxmLnRleHQgICAgICAgPSAiIgogICAgICAgICAgICBzZWxmLmNob2ljZXRleHQgPSAiIgogICAgICAgICAgICBzZWxmLmNob2ljZXMgICAgPSBbXQogICAgICAgICAgICBzZWxmLn" \
"Bhc3N3b3JkICAgPSBGYWxzZQoKICAgIGRlZiBfaW5pdF9wbGFjZXMoKToKICAgICAgICBwbGFjZXMgPSB7fQoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHBsYWNlc1siYmxhbmsiXSA9IHA" \
"KCiAgICAgICAgcC5wYXNzd29yZCA9IFRydWUKICAgICAgICBwbGFjZXNbIndhbGtfb25fb25lIl0gPSBwCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAiWW91IGdldCBpbiB5" \
"b3VyIHNoaXAuIgogICAgICAgIHAuY2hvaWNldGV4dCA9ICJHZXQgaW4geW91ciBzaGlwLiIKICAgICAgICBwLmNob2ljZXMgPSBbICJtYXJzb3V0cG9zdCIsICJ0aXRhbiIsICJlYXJ0aCIsICJsZ" \
"WF2ZXN5c3RlbSIsICJhc3Rlcm9pZGJlbHQiIF0KICAgICAgICBwbGFjZXNbInNoaXAiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC50ZXh0ID0gIm5vIHJlc3BvbnNlIjsgcC5jaG9pY2V0ZX" \
"h0ID0gImdvIHRvIG1hcnMgb3V0cG9zdCB4IjsgcGxhY2VzWyJtYXJzb3V0cG9zdCJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJXZWxjb21lIGJhY2sgaG9tZSE" \
"gSSBiZXQgeW91ciBmYW1pbHkgd2lsbCBiZSBoYXBweSB0byBzZWUgeW91ISIKICAgICAgICBwLmNob2ljZXRleHQgPSAiZ28gdG8gZWFydGhzIHN5c3RlbSIKICAgICAgICBwLmNob2ljZXMgPSBb" \
"ICJzaGlwIiwgImVhcnRoX2ZhbWlseSIsICJlYXJ0aF9yZWxheCIgXQogICAgICAgIHBsYWNlc1siZWFydGgiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAieW91I" \
"HJlbGF4LiIKICAgICAgICBwLmNob2ljZXRleHQgPSAicmVsYXgiCiAgICAgICAgcC5jaG9pY2VzID0gWyAic2hpcCIsICJlYXJ0aF9mYW1pbHkiIF0KICAgICAgICBwbGFjZXNbImVhcnRoX3JlbG" \
"F4Il0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gIndlbGNvbWUgdG8gdGhlIGxpYnJhcnkhIgogICAgICAgIHAuY2hvaWNlcyA9IFsgInR5bG9uIiwgInJpdG1lbiI" \
"sICJzaW1ib28iLCAic2hpcCIgXQogICAgICAgIHAuY2hvaWNldGV4dCA9ICJnbyB0byB0aGUgc3RhdGlvbiBsaWJyYXJ5IDwtLSIKICAgICAgICBwbGFjZXNbImxpYnJhcnkiXSA9IHAKICAgICAg" \
"ICAKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJ0aGUgdHlsb24gYXJlIG9uZSBvZiB0aGUgbW9zdCBhZHZhbmNlZCBhbmQgc2F2YWdlIHJhY2VzIGtub3duIVxud2UgZ290I" \
"G1vc3Qgb2YgYXJlIHdlcG9ucyBmcm9tIGEgZnJlbmRseSBncm91cCBvZiB0eWxvbiB0aGF0IGFyZSBub3cgYSByZWJlbGxpb24uXG50aGUgdHlsb24gYXJlIGp1c3Qgb25lIHN0ZXAgZG93biBmcm" \
"9tIGh1bWFucyBpbiB0ZWNobm9sb2d5LiIKICAgICAgICBwLmNob2ljZXRleHQgPSAidGhlIHR5bG9uIgogICAgICAgIHBsYWNlc1sidHlsb24iXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICA" \
"gICAgICBwLnRleHQgPSAidGhlIHJpdG1lbiBhcmUgYSBnZW50bGUgcmFjZS4gIHRoZXkgc3BlY2lhbGl6ZSBpbiB0ZWNobm9sb2d5Llxud2UgZ290IG1vc3Qgb2YgYXJlIG1lZGljaW5lIGZyb20g" \
"dGhlIHJpdG1lbi5cbnRoZXkgYWxzbyBoZWxwZWQgdXMgd2l0aCBhcmUgdHlub2lkIHRocnVzdGVycy4iCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gInRoZSByaXRtZW4iCiAgICAgICAgcGxhY2VzW" \
"yJyaXRtZW4iXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAidGhlIHNpbWJvbyBhcmUgYSB2ZXJ5IG15c3RlcmlvdXMgcmFjZS4iCiAgICAgICAgcC5jaG9pY2V0ZX" \
"h0ID0gInRoZSBzaW1ib28iCiAgICAgICAgcGxhY2VzWyJzaW1ib28iXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAiY29vcmRpbmF0ZXMgc2V0LCB0aHJ1c3RlcnM" \
"gZnVuY3Rpb25hbC4gIGJsYXN0IG9mZiEiCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gImdvIHRvIHN5c3RlbSAxIgogICAgICAgIHAuY2hvaWNlcyA9IFsgImxpYnJhcnkiLCAibG9uZXBsYW5ldCIg" \
"XQogICAgICAgIHBsYWNlc1sic3lzdGVtMSJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJ5b3UgbGFuZCBvbiBhIGxhbmRpbmcgcGFkLiIKICAgICAgICBwLmNob" \
"2ljZXMgPSBbICJjaXR5IiwgInNoaXAiIF0KICAgICAgICBwLmNob2ljZXRleHQgPSAidmlzaXQgbG9uZSBidXQgaW5oYWJpdGF0ZWQgcGxhbmV0IHgiCiAgICAgICAgcGxhY2VzWyJsb25lcGxhbm" \
"V0Il0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gInlvdSBoZWFkIHRvIHRoZSB0aXRhbiBjb2xvbnksXG4gYnV0IHlvdXIgZ2V0aW5nIHVudXN1YWwgcmVhZGluZ3M" \
"uLi4gYXMgeW91IGxhbmQgeW91IHJlYWxpemUgdGhhdFxuIGl0IHdhcyBkZXN0cm95ZWQuIgogICAgICAgIHAuY2hvaWNldGV4dCA9ICJnbyB0byB0aXRhbiBjb2xvbnkiCiAgICAgICAgcC5jaG9p" \
"Y2VzID0gWyAidGl0YW4xIiwgInNoaXAiIF0KICAgICAgICBwbGFjZXNbInRpdGFuIl0gPSBwCiAgICAgICAgcCA9IFBsYWNlKCk7IHAuY2hvaWNldGV4dCA9ICJmaW5kIG91dCB3aGF0IGhhcHBlb" \
"mVkIHgiOyBwbGFjZXNbInRpdGFuMSJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAuY2hvaWNldGV4dCA9ICJsZWF2ZSBzb2xhciBzeXN0ZW0iCiAgICAgICAgcC5jaG9pY2VzID" \
"0gWyAic3lzdGVtMSIsICJzeXN0ZW0yIiwgInN5c3RlbTMiLCAic3lzdGVtNCIsICJzeXN0ZW01IiwgImVhcnRoIiBdCiAgICAgICAgcGxhY2VzWyJsZWF2ZXN5c3RlbSJdID0gcAoKICAgICAgICB" \
"wID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJjb29yZGluYXRlcyBzZXQsIHRocnVzdGVycyBmdW5jdGlvbmFsLiAgYmxhc3Qgb2ZmIVxuLi4uLi4uLi4uLi4uIgogICAgICAgIHAuY2hvaWNl" \
"dGV4dCA9ICJnbyB0byBzeXN0ZW0gMiA8LS0iCiAgICAgICAgcC5jaG9pY2VzID0gWyAiYWJhbmRvbmVkX291dHBvc3QiLCAibGlmZWxlc3NwbGFuZXQiIF0KICAgICAgICBwbGFjZXNbInN5c3Rlb" \
"TIiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC5jaG9pY2V0ZXh0ID0gImdvIHRvIHN5c3RlbSAzIHgiOyBwbGFjZXNbInN5c3RlbTMiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC5jaG" \
"9pY2V0ZXh0ID0gImdvIHRvIHN5c3RlbSA0IHgiOyBwbGFjZXNbInN5c3RlbTQiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC5jaG9pY2V0ZXh0ID0gImdvIHRvIHN5c3RlbSA1IHgiOyBwbGF" \
"jZXNbInN5c3RlbTUiXSA9IHAKICAgICAgCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAiV2VsY29tZSB0byB0aGUgYXN0ZXJvaWQgYmVsdCBvdXRwb3N0LiAgTG90cyBvZiB0" \
"cmFkaW5nIGdvZXMgb24gaGVyZSEiCiAgICAgICAgcC5jaG9pY2VzID0gWyAic2hpcCIsICJ0cmFkZXN0YXRpb24iIF0KICAgICAgICBwLmNob2ljZXRleHQgPSAiZ28gdG8gYXN0ZXJvaWQgYmVsd" \
"CAod2lsbCBlcmFzZSBwcm9ncmVzISkiCiAgICAgICAgcGxhY2VzWyJhc3Rlcm9pZGJlbHQiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC5jaG9pY2V0ZXh0ID0gImdvIHRvIHRyYWRlIHN0YX" \
"Rpb24geCI7IHBsYWNlc1sidHJhZGVzdGF0aW9uIl0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gIllvdSB2aXNpdCB5b3VyIGZhbWlseS4gWW91IGhhdmUgYSB3b25" \
"kZXJmdWwgdGltZSEiCiAgICAgICAgcC5jaG9pY2VzID0gWyAic2hpcCIsICJlYXJ0aF9yZWxheCIgXQogICAgICAgIHAuY2hvaWNldGV4dCA9ICJ2aXNpdCBmYW1pbHkiCiAgICAgICAgcGxhY2Vz" \
"WyJlYXJ0aF9mYW1pbHkiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAieW91IGxhbmQgaW4gYSBwaWxlIG9mIHJ1YmJsZSB0aGF0IHVzZWQgdG8gYmUgYSBsYW5ka" \
"W5nIHBhZC5cblNvbWV0aGluZ3Mgbm90IHJpZ2h0LCB0aGVyZSBzaG91bGQgYmUgbW9yZSBwZW9wbGUuIgogICAgICAgIHAuY2hvaWNlcyA9IFsgImxpZmVsZXNzcGxhbmV0X2NpdHkiLCAic2hpcC" \
"IgXQogICAgICAgIHAuY2hvaWNldGV4dCA9ICJ2aXNpdCBsaWZlbGVzcyBwbGFuZXQiCiAgICAgICAgcGxhY2VzWyJsaWZlbGVzc3BsYW5ldCJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICA" \
"gICAgIHAudGV4dCA9ICJ5b3UgZ28gdG8gdGhlIGFiYW5kb25lZCBjaXR5XG55b3UgcGF0IHlvdXIgYmVsdCB0byBtYWtlIHN1cmUgeW91IHBsYXNtYSBibGFzdGVyIGlzIHRoZXJlLCBpdCBpcywg" \
"eW91IGhlYWQgZm9yIHRoZSBjaXR5LlxuICAgIAlUaW1lIHBhc3Nlcy4uLlxuICAgIAkJVGltZSBwYXNzZXMuLi5cbnlvdSBmaW5hbGx5IGdldCB0aGVyZSEgSXRzIHNvLi4uIEVtcHR5LiAgWW91I" \
"HN1ZGRlbmx5IGhlYXIgc29tZXRoaW5nISIKICAgICAgICBwLmNob2ljZXMgPSBbICJncmFiYmxhc3RlciIsICJrZWVwd2Fsa2luZyIgXQogICAgICAgIHAuY2hvaWNldGV4dCA9ICJnbyB0byB0aG" \
"UgYWJhbmRvbmVkIGNpdHkiCiAgICAgICAgcGxhY2VzWyJsaWZlbGVzc3BsYW5ldF9jaXR5Il0gPSBwCiAgICAgICAgcCA9IFBsYWNlKCk7IHAudGV4dCA9ICIiOyBwLmNob2ljZXRleHQgPSAiZ3J" \
"hYiB5b3VyIHBsYXNtYSBibGFzdGVyIGFuZCBrZWVwIHdhbGtpbmciOyBwbGFjZXNbImdyYWJibGFzdGVyIl0gPSBwCiAgICAgICAgcCA9IFBsYWNlKCk7IHAudGV4dCA9ICIiOyBwLmNob2ljZXRl" \
"eHQgPSAia2VlcCB3YWxraW5nIjsgcGxhY2VzWyJrZWVwd2Fsa2luZyJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJ5b3UgZ28gdG8gdGhlIGNpdHkuICBpdHMgY" \
"SByaXRtZW4gY2l0eS5cbnlvdSBnbyBjaGVrIGludG8gYSBob3RlbC4gIHRoZW4gd2hhdCBkbyB5b3UgZG8/IgogICAgICAgIHAuY2hvaWNlcyA9IFsgImNpdHlfc2thdGluZyIsICJjaXR5X21ha2" \
"VmcmllbmRzIiwgImNpdHlfb3B0aW9uMyIsICJjaXR5X29wdGlvbjQiIF0KICAgICAgICBwLmNob2ljZXRleHQgPSAiZ28gdG8gdGhlIGNpdHkiCiAgICAgICAgcGxhY2VzWyJjaXR5Il0gPSBwCiA" \
"gICAgICAgcCA9IFBsYWNlKCk7IHAudGV4dCA9ICJZb3Ugd2VudCBza2F0aW5nLiBUaGF0IHdhcyBmdW4hIjsgcC5jaG9pY2V0ZXh0ID0gImdvIHNrYXRpbmciOyBwbGFjZXNbImNpdHlfc2thdGlu" \
"ZyJdID0gcAogICAgICAgIHAgPSBQbGFjZSgpOyBwLnRleHQgPSAiWW91IG1hZGUgc29tZSBtb3JlIGZyaWVuZHMuIEdvb2QgZm9yIHlvdSEiOyBwLmNob2ljZXRleHQgPSAibWFrZSBzb21lIGZya" \
"WVuZHMiOyBwbGFjZXNbImNpdHlfbWFrZWZyaWVuZHMiXSA9IHAKICAgICAgICBwID0gUGxhY2UoKTsgcC50ZXh0ID0gIm9wdGlvbjMiOyBwLmNob2ljZXRleHQgPSAib3B0aW9uMyI7IHBsYWNlc1" \
"siY2l0eV9vcHRpb24zIl0gPSBwCiAgICAgICAgcCA9IFBsYWNlKCk7IHAudGV4dCA9ICJvcHRpb240IjsgcC5jaG9pY2V0ZXh0ID0gIm9wdGlvbjQiOyBwbGFjZXNbImNpdHlfb3B0aW9uNCJdID0" \
"gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJ5b3UgcmVhZCB0aGUgcGFwZXIsIGl0cyB0b3JuIHByZXR0eSBiYWRseSBidXQgeW91IGNhbiBtYWtlIG91dCBzb21ldGhp" \
"bmcuLi5cbnBhc3N3b3JkIDc0My4gIGhtbW1tbS4uLiBhIHBhc3N3b3JkLCBidXQgZm9yIHdoYXQ/IgogICAgICAgIHAuY2hvaWNldGV4dCA9ICJwaWNrIHVwIHBhcGVyIgogICAgICAgIHAuY2hva" \
"WNlcyA9IFsid2Fsa19vbl9vbmUiXQogICAgICAgIHBsYWNlc1sicGlja191cF9wYXBlciJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICIgeW91IG9wZW4gdGhlIG" \
"Rvb3IhICB0aGVyZSBpcyBsb3RzIG9mIHN0dWYgaW5zaWRlIVxueW91IHdvbiBvbmUgb2YgdGhlIHdheXMgdG8gd2luISIKICAgICAgICBwLmNob2ljZXRleHQgPSAidW5sb2NrIGRvb3IiCiAgICA" \
"gICAgcGxhY2VzWyJ1bmxvY2tfb25lIl0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gInlvdSBrZWVwIHdhbGtpbmcsIHlvdSBjb21lIHRvIGEgc2VhbGQgZG9vci4g" \
"J3Bhc3N3b3JkPycgaXQgYXNrcyB5b3UuXG50eXBlIGluIHRoZSBwYXNzd29yZCEiCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gIndhbGsgb24iCiAgICAgICAgcC5jaG9pY2VzID0gWyAiYmxhbmsiI" \
"F0KICAgICAgICBwLnBhc3N3b3JkID0gVHJ1ZQogICAgICAgIHBsYWNlc1sid2Fsa19vbl9vbmUiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAieW91IGxhbmQgaW" \
"4gYSBwaWxlIG9mIHJ1YmJsZSB0aGF0IHVzZWQgdG8gYmUgYSBsYW5kaW5nIHBhZC5cblNvbWV0aGluZ3Mgbm90IHJpZ2h0LCB0aGVyZSBzaG91bGQgYmUgbW9yZSBwZW9wbGUuIgogICAgICAgIHA" \
"uY2hvaWNldGV4dCA9ICJ2aXNpdCBsaWZlbGVzcyBwbGFuZXQiCiAgICAgICAgcC5jaG9pY2VzID0gWyAiYWJhbmRvbmVkX2NpdHkiLCAic2hpcCIgXQogICAgICAgIHBsYWNlc1sibGlmZWxlc3Nw" \
"bGFuZXQiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAiZ28gdG8gdGhlIGFiYW5kb25lZCBjaXR5XG55b3UgcGF0IHlvdXIgYmVsdCB0byBtYWtlIHN1cmUgeW91I" \
"HBsYXNtYSBibGFzdGVyIGlzIHRoZXJlLCBpdCBpcywgeW91IGhlYWQgZm9yIHRoZSBjaXR5LlxuICAgVGltZSBwYXNzZXMuLi5cbiAgICAgIFRpbWUgcGFzc2VzLi4uXG4gICAgeW91IGZpbmFsbH" \
"kgZ2V0IHRoZXJlISBJdHMgc28uLi4gRW1wdHkuICBZb3Ugc3VkZGVubHkgaGVhciBzb21ldGhpbmchIgogICAgICAgIHAuY2hvaWNldGV4dCA9ICJnbyB0byB0aGUgYWJhbmRvbmVkIGNpdHkiCiA" \
"gICAgICAgcC5jaG9pY2VzID0gWyAiZ3JhYl9ibGFzdGVyIiwgImtlZXBfd2Fsa2luZyIgXQogICAgICAgIHBsYWNlc1siYWJhbmRvbmVkX2NpdHkiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkK" \
"ICAgICAgICBwLnRleHQgPSAieW91IGtlZXAgd2Fsa2luZy4gIHRoZSBzb3VuZCBvZiBHQkYgQmF0dGxlIHNoaXBzIGZpbGwgdGhlIGFpci5cbgl5b3Ugd29uZGVyIGlmIGFueSBmbG9yYSBvciBmY" \
"XVuYSBsaXZlIG9uIHRoaXMgZGVzb2xhdGUgcGxhbmV0LiB0aGUgdGltZSBpcyAxMTozMFxuCQkJdGltZSBwYXNzZXMuLi5cbgkJCQl0aW1lIHBhc3Nlcy4uLlxuCQkJCQl0aW1lIHBhc3Nlcy4uLl" \
"xuCXRpbWUgcGFzc2VzLi4uIHlvdSBjaGVjayB5b3VyIHdhdGNoIHRvIHNlZSBob3cgbG9uZyBpdHMgYmVlbiwgMzAgbWludXRlLlxuCQkJCQkJCXRpbWUgcGFzc2VzLi4uXG4JCXRpbWUgcGFzc2V" \
"zLi4uXG4JCQkJCQkJCQl0aW1lIHBhc3Nlcy4uLlxuCXlvdSBmYW5hbGx5IGdldCBzb21lIHdoZXJlLiAgaXRzIDE6MjcuICB5b3UgZ28gaW4uICBhIHBhcGVyIGlzIG9uIHRoZSBmbG9vci4iCiAg" \
"ICAgICAgcC5jaG9pY2V0ZXh0ID0gImtlZXAgb24gd2Fsa2luZyIKICAgICAgICBwLmNob2ljZXMgPSBbICJwaWNrX3VwX3BhcGVyIiwgIndhbGtfb25fb25lIiBdCiAgICAgICAgcGxhY2VzWyJrZ" \
"WVwX2V4cGxvcmluZ19vbmUiXSA9IHAKCiAgICAgICAgcCA9IFBsYWNlKCkKICAgICAgICBwLnRleHQgPSAieW91IGtlZXAgd2Fsa2luZywgeW91IGhhdmUgdGhlIGZlZWxpbmcgeW91ciBiZWluZy" \
"B3YXRjaGVkLi4uXG5TdWRkZW5seSB0aHJlZSBwZW9wbGUganVtcCBvdXQgaW4gZnJvbnQgb2YgeW91IGFuZCBvcGVuIGZpcmUhXG5Zb3UgZ3JhYiBmb3IgeW91ciBibGFzdGVyIGJ1dCBpdHMgdG8" \
"gbGF0ZSEgIFlvdSBmYWxsIHRvIHRoZSBncm91bmQgZGVhZC5cbgkJWW91IGhhdmUgZGllZC4iCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gImtlZXAgd2Fsa2luZyIKICAgICAgICBwbGFjZXNbImtl" \
"ZXBfd2Fsa2luZyJdID0gcAoKICAgICAgICBwID0gUGxhY2UoKQogICAgICAgIHAudGV4dCA9ICJpdHMgMTE6MzAgYXQgMTI6MDAgYSBzaGlwIGxhbmRzIGFuZCBhIHNxdWFkIGdldHMgb3V0LFxue" \
"W91IHRlbGwgdGhlIHNxdWFkIHdoYXQgaGFwcGVuZCwgaXRzIDEyOjExLiIKICAgICAgICBwLmNob2ljZXMgPSBbICJzaGlwIiwgInN5c3RlbTIiIF0KICAgICAgICBwLmNob2ljZXRleHQgPSAid2" \
"FpdCBmb3IgYmFja3VwIgogICAgICAgIHBsYWNlc1sid2FpdF9mb3JfYmFja3VwIl0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gInlvdSBrZWVwIHdhbGtpbmcsIHl" \
"vdSBoYXZlIHRoZSBmZWVsaW5nIHlvdXIgYmVpbmcgd2F0Y2hlZC4uLlxuU3VkZGVubHkgdGhyZWUgcGVvcGxlIGp1bXAgb3V0IGluIGZyb250IG9mIHlvdSBhbmQgb3BlbiBmaXJlISAgWW91IGRp" \
"dmUgZm9yIGNvdmVyIGFuZCByZXR1cm4gZmlyZSFcbllvdSBjb21lIG91dCBmcm9tIHlvdXIgY292ZXIgYW5kIGNvbnRhY3QgR0JGIChHYWxhY3RpYyBCYXR0bGUgRmxlZXQpIGFuZCBhc2sgZm9yI" \
"GJhY2t1cC4iCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gImdyYWIgeW91ciBwbGFzbWEgYmxhc3RlciBhbmQga2VlcCB3YWxraW5nIgogICAgICAgIHAuY2hvaWNlcyA9IFsgIndhaXRfZm9yX2JhY2" \
"t1cCIsICJrZWVwX2V4cGxvcmluZ19vbmUiLCAic2hpcCIgXQogICAgICAgIHBsYWNlc1siZ3JhYl9ibGFzdGVyIl0gPSBwCgogICAgICAgIHAgPSBQbGFjZSgpCiAgICAgICAgcC50ZXh0ID0gInl" \
"vdSBoZWFkIHRvIHRoZSBhYmFuZG9uZWQgb3V0cG9zdC5cbidIbW1tbW0gdGhlIHNlbnNvcnMgZ2V0aW5nIHVudXN1YWwgcmVhZGluZ3MuLi4nXG5zdWRkZW5seSBhIHNxdWFkIG9mIHR5bG9uIGRp" \
"c3J1cHRlcnMgYXBwZWFyIVxubHVja2lseSB0aGVyZSBzaGlsZWRzIGFyZSBubyBtYWNoIGZvciB5b3VyIHBob3RvbiB0b3JwZWRvZXMuXG55b3UgZ2V0IHRvIHRoZSBhYmFuZG9uZWQgb3V0cG9zd" \
"CB0byBmaW5kIGl0cyBhIGJ1bmNoIG9mIHJ1YmJsZS4iCiAgICAgICAgcC5jaG9pY2V0ZXh0ID0gImdvIHRvIGFiYW5kb25lZCBvdXRwb3N0IgogICAgICAgIHAuY2hvaWNlcyA9IFsgImxpZmVsZX" \
"NzcGxhbmV0IiwgImxlYXZlc3lzdGVtIiBdCiAgICAgICAgcGxhY2VzWyJhYmFuZG9uZWRfb3V0cG9zdCJdID0gcAoKICAgICAgICBwbGFjZXNbImN1cnJlbnQiXSA9ICJzeXN0ZW0xIgogICAgICA" \
"gIHBsYWNlc1siZGVhZCJdID0gRmFsc2UKICAgICAgICByZXR1cm4gcGxhY2VzCgogICAgZGVmIF9zaG93X2Nob2ljZXMocGxhY2VzKToKICAgICAgICBjdXJyZW50ID0gcGxhY2VzW3BsYWNlc1si" \
"Y3VycmVudCJdXQogICAgICAgIHByaW50KGN1cnJlbnQudGV4dCkKICAgICAgICBjb3VudCA9IDEKICAgICAgICBmb3IgY2hvaWNlIGluIGN1cnJlbnQuY2hvaWNlczoKICAgICAgICAgICAgcHJpb" \
"nQoIiglZCkgJXMiICUgKGNvdW50LCBwbGFjZXNbY2hvaWNlXS5jaG9pY2V0ZXh0KSkKICAgICAgICAgICAgY291bnQgKz0gMQogICAgICAgIHByaW50KCIoVHlwZSAneCcgdG8gZXhpdCkiKQoKIC" \
"AgIGRlZiBfcHJvY2VzcyhwbGFjZXMsdCk6CiAgICAgICAgbmV3cGxhY2UgPSBwbGFjZXNbcGxhY2VzWyJjdXJyZW50Il1dLmNob2ljZXNbaW50KHQpLTFdCiAgICAgICAgaWYgbmV3cGxhY2UgPT0" \
"gImtlZXBfd2Fsa2luZyI6CiAgICAgICAgICAgIHBsYWNlc1siZGVhZCJdID0gVHJ1ZQogICAgICAgIGlmIGxlbihwbGFjZXNbbmV3cGxhY2VdLmNob2ljZXMpID4gMDoKICAgICAgICAgICAgcGxh" \
"Y2VzWyJjdXJyZW50Il0gPSBuZXdwbGFjZQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIHByaW50KHBsYWNlc1tuZXdwbGFjZV0udGV4dCkKICAgICAgICByZXR1cm4gcGxhY2VzCgogICAgZGVmI" \
"F9ydW4oKToKICAgICAgICBwbGFjZXMgPSBfaW5pdF9wbGFjZXMoKQogICAgICAgIHdoaWxlIFRydWU6CiAgICAgICAgICAgIF9zaG93X2Nob2ljZXMocGxhY2VzKQogICAgICAgICAgICBjdXJyZW" \
"50ID0gcGxhY2VzW3BsYWNlc1siY3VycmVudCJdXQogICAgICAgICAgICB0ZXh0aW5wdXQgPSBzdHIoaW5wdXQoIlxuYWxsZW5AZ2JmX2V4cGxvcmVyOn4+ICIpKQogICAgICAgICAgICBpZiB0ZXh" \
"0aW5wdXQgIT0gIiI6CiAgICAgICAgICAgICAgICBpZiBjdXJyZW50LnBhc3N3b3JkOgogICAgICAgICAgICAgICAgICAgIGlmIHRleHRpbnB1dCA9PSAiNzQzIjoKICAgICAgICAgICAgICAgICAg" \
"ICAgICAgcGxhY2VzWyJjdXJyZW50Il0gPSAidW5sb2NrX29uZSIKICAgICAgICAgICAgICAgICAgICAgICAgcHJpbnQoIiB5b3Ugb3BlbiB0aGUgZG9vciEgIHRoZXJlIGlzIGxvdHMgb2Ygc3R1Z" \
"iBpbnNpZGUhXG55b3Ugd29uIG9uZSBvZiB0aGUgd2F5cyB0byB3aW4hIikKICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgIC" \
"AgICAgICAgICAgICBwcmludCgiWW91IGVudGVyICclcyciICUgdGV4dGlucHV0KQogICAgICAgICAgICAgICAgICAgICAgICBwcmludCgiVGhlIGRvb3Igd29uJ3QgYnVkZ2UuIikKICAgICAgICA" \
"gICAgICAgICAgICAgICAgcGxhY2VzWyJ3YWxrX29uX29uZSJdLnRleHQgPSAiJ3Bhc3N3b3JkPycgaXQgYXNrcyB5b3UiCiAgICAgICAgICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgICAg" \
"IGlmIHRleHRpbnB1dCA9PSAieCI6CiAgICAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgIHQgPSBpbnQodGV4d" \
"GlucHV0KQogICAgICAgICAgICAgICAgICAgICAgICBwbGFjZXMgPSBfcHJvY2VzcyhwbGFjZXMsIHQpCiAgICAgICAgICAgICAgICAgICAgZXhjZXB0OgogICAgICAgICAgICAgICAgICAgICAgIC" \
"BwcmludCgiSSBkb24ndCBrbm93ICclcycuIFBpY2sgYSBudW1iZXIuIiAlIHRleHRpbnB1dCkKICAgICAgICAgICAgaWYgcGxhY2VzWyJkZWFkIl06CiAgICAgICAgICAgICAgICBwcmludCgiR29" \
"vZCBnYW1lLiIpCiAgICAgICAgICAgICAgICBicmVhawoKICAgIHRyeToKICAgICAgICBfcnVuKCkKICAgICAgICBwcmludCgiWW91IHJldHVybiB0byB5b3VyIFNDUkVFTi4iKQogICAgZXhjZXB0" \
"IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KGUpCiAgICAgICAgcHJpbnQoIkFsbGVuJ3MgY29tcHV0ZXIgY3Jhc2hlZC4iKQoK"

eval(compile(base64.b64decode(game_function), "allen_game", "exec"))
# Loads the function. Invoke with: allen_game()

if __name__ == "__main__":
    g = Globals()
    static_images(g,"post")
    g.player = Player()
    # Only support pidgin English. Aooga.
    g.word_ignore = [ "the", "of", "in", "to", "into", "on", "at", "a" ]
    run_game(g)
