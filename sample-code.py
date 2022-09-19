#!/usr/bin/env python
# coding: utf-8

# Libraries
import sys
import time
import os


# Player

player = {
    "name": "unknow",
    "life": 100,
    "current_room": None
}

# define rooms and items
# toilet
toilet_room = {
    "name": "toilet room",
    "type": "room",
}

door_toilet = {
    "name": "door toilet",
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

door_bedroom = {
    "name": "door bedroom",
    "type": "door",
}

key_bedroom = {
    "name": "key for bedroom",
    "type": "key",
    "target": door_bedroom,
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
    "name": "door living room",
    "type": "door",
}

key_livingroom = {
    "name": "key for living room",
    "type": "key",
    "target": door_livingroom,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

couch = {
    "name": "couch",
    "type": "furniture",
}
##########

# Kitchen

kitchen_room = {
    "name": "kitchen room",
    "type": "room",
}
door_kitchen = {
    "name": "door kitchen",
    "type": "door",
}

key_kitchen = {
    "name": "key for toilet",
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
    "living room": [couch, piano, door_livingroom],
    "kitchen room": [balcony, door_kitchen, microwave],
    "bedroom": [bed, mirror, table],
    "bed": [key_bedroom],
    "mirror": [key_toilet],
    "outside": [door_toilet],
    "door toilet": [toilet_room, outside],
    "balcony": [key_kitchen],
    "couch": [key_livingroom],
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


def print_slow(string, speed=0.01):
    """This function will write a terminal message in a slow way so that
    the user can keep track of what is happening"""
    for letter in string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(speed)
    linebreak()


def linebreak():
    """
    Print a line break
    """
    print("\n")


def start_game():
    """
    Start the game
    """
    # print_slow(
    #    """You wake up on a couch and find yourself in a strange division with no windows which you have never been to before, it's a toilet for sure. You don't remember why you are here and what had happened before...\n You feel some unknown danger is approaching and you must get out of the house, NOW!"""
    # )
    # get_user_name()
    play_room(game_state["current_room"])


def get_user_name():
    """Get player name"""
    print_slow("You need to focus! try to remenber, what is your name?")
    player["name"] = input("Right your name here: ")
    print_slow(
        f"Yes! my name is {player['name']}! \n Now I need to get out of here!!!")


def play_room(room, new_room=True):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    if player["current_room"] is None:
        player["current_room"] = all_rooms[0]
    game_state["current_room"] = room
    if game_state["current_room"] == game_state["target_room"]:
        print_slow("\nYou made it! You escaped the house!")
    else:
        if new_room is True:
            print_slow(f"I think I'm in {room['name']}... looks like it")
        print_slow(("What should I do? explore? or examine some object?"))
        intended_action = None
        while intended_action is None:
            intended_action = (
                input(
                    "Write 'Explore' to explore all the objects in the room or 'Examine' to examine one of the objects: "
                ).strip()
            ).upper()
            if intended_action == "EXPLORE":
                explore_room(room)
                play_room(room, new_room=False)
            elif intended_action == "EXAMINE":
                print_slow("What should I examine?")
                examine_item(
                    input("Write the object name to examine: ").strip())
            else:
                print_slow("I'm confused...")
                play_room(room, new_room=False)
            linebreak()


def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print_slow(
        f"Let's explore the {room['name']}. I can see {', '.join(items)}. I should examine them... \n"
    )


def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if not current_room == room:
            return room


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
            output = "Let's see what I can find in this " + item_name + ". "
            if item["type"] == "door":
                have_key = False
                for key in game_state["keys_collected"]:
                    if key["target"] == item:
                        have_key = True
                if have_key:
                    output += "I have a key to unlock this door!"
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "The door is locked and I don't have the key... dammit! I need to examine more objects!"
            else:
                if (
                    item["name"] in object_relations
                    and len(object_relations[item["name"]]) > 0
                ):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += f"Yes! I've found {item_found['name']}. I need to go to the door next!"
                    next_room = all_rooms[1]
                else:
                    output += "I couldn't find anything interesting here..."
            print_slow(output)
            break
    if output is None:
        print_slow(
            f"Hm I can't find a {item_name} in this room... have I spell it wrong?")
    if (
        next_room
        and input("Should I go to the next room? Enter 'yes' or 'no'").strip() == "yes"
    ):
        del all_rooms[0]
        play_room(next_room)
    else:
        play_room(current_room, new_room=False)


game_state = INIT_GAME_STATE.copy()

os.system("cls" if os.name == "nt" else "clear")
start_game()
