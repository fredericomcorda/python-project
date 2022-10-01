#!/usr/bin/env python
# coding: utf-8

# Libraries
import sys
import time
import os
from pygame import mixer
import minigame as tuna
import highscore as hs
import pyautogui as pg

os.system("title _-+[ O Nome do Jogo - Escape Room ]+-_")
time.sleep(1)

pg.getWindowsWithTitle("O Nome do Jogo - Escape Room")[0].maximize()

# Player

player = {
    "name": "unknow",
    "life": 100,
    "current_room": None,
    "total time": None
}

# define rooms and items
# toilet
toilet_room = {
    "name": "toilet room",
    "type": "room",
}

door_toilet = {
    "name": "toilet door",
    "type": "door",
}

key_toilet = {
    "name": "key for toilet",
    "type": "key",
    "target": door_toilet,
}

mirror = {
    "name": "mirror",
    "type": "furniture",
}
##########

# Bedroom
bedroom_room = {
    "name": "bedroom",
    "type": "room",
}

teddy_bear = {
    "name": "teddy bear",
    "type": "furniture",
}

door_bedroom = {
    "name": "bedroom door",
    "type": "door",
}

key_bedroom = {
    "name": "key for bedroom",
    "type": "key",
    "target": door_bedroom,
}

plant = {
    "name": "plant",
    "type": "furniture",
}

bed = {
    "name": "bed",
    "type": "furniture",
}


table = {
    "name": "bedside table",
    "type": "furniture",
}

##########

# Living Room
livingroom_room = {
    "name": "living room",
    "type": "room",
}

door_livingroom = {
    "name": "living room door",
    "type": "door",
}

key_livingroom = {
    "name": "key for living room",
    "type": "key",
    "target": door_livingroom,
}

book_shelf = {
    "name": "book shelf",
    "type": "furniture",
}

couch = {
    "name": "couch",
    "type": "furniture",
}

television = {
    "name": "television",
    "type": "furniture",
}

flower_pot = {
    "name": "flower pot",
    "type": "furniture",
}
##########

# Kitchen

kitchen_room = {
    "name": "kitchen",
    "type": "room",
}
door_kitchen = {
    "name": "kitchen door",
    "type": "door",
}

key_kitchen = {
    "name": "key for kitchen",
    "type": "key",
    "target": door_kitchen,
}

balcony = {
    "name": "balcony",
    "type": "furniture",
}

microwave = {
    "name": "microwave",
    "type": "furniture",
}
###########

# Outside
outside = {"name": "outside"}


all_rooms = [toilet_room, bedroom_room, livingroom_room, kitchen_room, outside]

all_doors = [door_toilet, door_bedroom, door_livingroom, door_kitchen]

# define which items/rooms are related

object_relations = {
    "toilet room": [mirror, door_toilet],
    "living room": [couch, television, book_shelf, flower_pot, door_livingroom, door_toilet],
    "kitchen": [balcony, door_kitchen, microwave],
    "bedroom": [bed, mirror, table, door_bedroom],
    "bed": [key_bedroom],
    "mirror": [key_toilet],
    "balcony": [key_kitchen],
    "couch": [key_livingroom],
    "outside": [outside],
    "toilet door": [toilet_room, livingroom_room],
    "living room door": [livingroom_room, bedroom_room],
    "bedroom door": [bedroom_room, kitchen_room],
    "kitchen door": [kitchen_room, outside],
    "balcony": [key_kitchen],
    "book shelf": [key_livingroom],
}

# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": all_rooms[0],
    "keys_collected": [],
    "target_room": outside,
}


def clear_terminal():
    """this function clears the console text"""
    print('\x1b[0m')
    os.system("cls" if os.name == "nt" else "clear")


def print_slow(string, speed=0.06, color=None):  # added
    """This function will write a terminal message in a slow way so that
    the user can keep track of what is happening"""
    print('\x1b[0m')
    if color == "red":
        print('\x1b[1;37;41m')
    elif color == "green":
        print('\x1b[7;30;42')
    else:
        print('\x1b[0m')
    for letter in string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(speed)
    print('\x1b[0m')
    # linebreak()


def linebreak():
    """
    Print a line break
    """
    print("\n")


def start_game():
    """
    Start the game
    """
    print_slow(
        "You wake up on the floor and find yourself in a strange room with no windows, where you have never been before, it seems to be a toilet room for sure. \nYou don't remember why you are here and what had happened before...", color="red")
    print_slow(
        "I feel some unknown danger is approaching and I must try get out, NOW!", color="red")
    get_user_name()
    play_room(game_state["current_room"])


def get_user_name():
    """Get player name"""
    print_slow("You need to focus! Try to remember, what is my name?")
    player["name"] = input("Write your name here: \n" +
                           "\x1b[0;37;41m").capitalize()
    while not tuna.check_name(player["name"]):
        print('\x1b[0m')
        clear_terminal()
        get_user_name()
    print("\x1b[0m")
    print_slow(
        f"Yes! My name is {player['name']}! \n Now I need to get out of here!!!", color="red")


def play_room(room, new_room=True):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    # def
    if player["current_room"] is None:
        player["current_room"] = all_rooms[0]
    game_state["current_room"] = room
    if game_state["current_room"] == game_state["target_room"]:
        print_slow("\nYou made it! You escaped the house!")
    else:
        if new_room is True:
            print_slow(f"Ok, I'm in {room['name']}...")
        print_slow(("What should I do now? Explore? Or Examine some object?"))
        intended_action = None
        while intended_action is None:
            intended_action = (
                input(
                    "Write " + "\x1b[1;37;41m" + "'Explore'" + "\x1b[0m" + " to explore all the objects in the room or " +
                    "\x1b[1;37;41m" + "'Examine'" + "\x1b[0m" +
                    " to examine one of the objects:" + "\x1b[0;37;41m" + "\n"
                ).strip()
            ).upper()
            if intended_action == "EXPLORE":
                explore_room(room)
                play_room(room, new_room=False)
            elif intended_action == "EXAMINE":
                print_slow("\nWhat should I examine?")
                examine_item(
                    input("Write the object name to examine:" + "\n" + "\x1b[0;37;41m").strip())
                print("\x1b[0m")
            else:
                print_slow("I'm confused...")
                play_room(room, new_room=False)
            linebreak()


def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    # index_elements = [i+1 for i in range(len(object_relations[room["name"]]))]
    # combination = list(zip(index_elements, items))
    # list_items = str(combination).replace("[", "").replace("]","")
    print_slow(
        f"\nLet me explore the {room['name']}. I can see the objects \x1b[0;37;41m{','.join(items)}\x1b[0m . I should examine them... \n"
        #    f"\nLet me explore the {room['name']}. I can see {list_items}. I should examine them... \n"
    )
    # selection = int(input('Write the number of the object to examine: ')) - 1
    # print(f'you have selected {combination[selection][1]}')
    # input()


def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if not current_room == room:
            return room
    return None


def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            output = "Let me check " + item_name + ". "
            if item["type"] == "door":
                have_key = False
                for key in game_state["keys_collected"]:
                    if key["target"] == item:
                        # if tuna.minigame():
                        have_key = True
                        # else:
                        #    print_slow("oh no it's not the correct answer")
                if have_key:
                    output += "I have the key to unlock this door!"
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "This door is locked and I don't have the necessary key... dammit! I need to examine more objects!"
                    play_sound("door_locked.wav", 1)
            else:
                if item["name"] in object_relations and len(object_relations[item["name"]]) > 0:
                    if tuna.minigame():
                        have_key = True
                        item_found = object_relations[item["name"]].pop()
                        game_state["keys_collected"].append(item_found)
                        output = f"\nCorrect! I've found {item_found['name']}! it must the door key! I need to go to the door and get out!\n"
                    else:
                        print_slow("oh no it's not the correct answer")
                else:
                    output += "I couldn't find anything here..."
            print_slow(output)
            break
    if output is None:
        print_slow(
            f"Hm I can't find a {item_name} in this room... did I spell it wrong?")
    if next_room and input("Should I go to the next room? Enter 'yes' or 'no': " + "\n" + "\x1b[0;37;41m").strip() == "yes":
        play_sound("door_open.wav", 2)
        time.sleep(1)
        # print('\x1b[0m')
        clear_terminal()
        play_room(next_room)
    else:
        play_room(current_room)


def play_sound(file="ambient.wav", channel=0, loop=False):
    if loop is True:
        mixer.Channel(channel).play(
            mixer.Sound(f'{path}/sound/{file}'), loops=-1)
        return
    mixer.Channel(channel).play(mixer.Sound(f'{path}/sound/{file}'))
    return


game_state = INIT_GAME_STATE.copy()

# get path
path = os.path.dirname(__file__)

# hide the support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# clear the terminal
clear_terminal()


# Iniciate mixer for audio
mixer.init()

# highscore module
start_time = hs.Timerfuntion("start game")

# start sound
play_sound(loop=True)

start_game()

# game is finished
player['total time'] = hs.Timerfuntion("end game", start_time)


def the_end():
    print_slow(
        f'Congrats! you have finished the game in {round(player["total time"]/60,1)}m and you have exit the house!')
    print_slow('lets see the hightscores...')
    hs.add_record(player["name"], player["total time"])
    print('\n')
    print_slow("write 'exit' to exit the game\n")
    exit_game = False
    while not exit_game:
        if (input()).lower() == "exit":
            exit_game = True
    exit()


the_end()
