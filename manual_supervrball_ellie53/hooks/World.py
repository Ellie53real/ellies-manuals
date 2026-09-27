# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat, remove_specific_item

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    This is the earliest hook called during generation, before anything else is done.
    Use it to check or modify incompatible options, or to set up variables for later use.
    """
    if world.options.game_version == 0:
        if world.options.include_reverse_levels == False:
            if world.options.pack_requirement >= 4:
                world.options.pack_requirement.value = 4
    if world.options.game_version == 1:
        if world.options.include_reverse_levels == False:
            if world.options.pack_requirement >= 3:
                world.options.pack_requirement.value = 3
        else:
            if world.options.pack_requirement >= 6:
                world.options.pack_requirement.value = 6
    if world.options.game_version == 2:
        if world.options.pack_requirement >= 3:
            world.options.pack_requirement.value = 3
        if world.options.include_reverse_levels == True:
            world.options.include_reverse_levels.value = False
    pass

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove
    if world.options.game_version == 2:
        if world.options.include_shortcuts:
            locationNamesToRemove.append("Island 5 - Cliff Shortcut")
            locationNamesToRemove.append("Volcano 4 - Floats Shortcut")
            locationNamesToRemove.append("Desert 5 - Float Around The Back Shortcut")
        if world.options.include_golden_melons:
            locationNamesToRemove.append("Island 5 - Golden Melon On Top of Cliff")
            locationNamesToRemove.append("Space 5 - Golden Melon #1 On High Asteroid Rings")
            locationNamesToRemove.append("Space 5 - Golden Melon #2 On Middle Asteroid Rings")
            locationNamesToRemove.append("Space 5 - Golden Melon #3 On Low Asteroid")
            locationNamesToRemove.append("Space 5 - Golden Melon #4 On Low Asteroid Rings")
            locationNamesToRemove.append("Space 5 - Golden Melon #5 On Low Asteroid Rings")
            locationNamesToRemove.append("Toxic 4 - Golden Melon #1 On Side Rail")
            locationNamesToRemove.append("Toxic 4 - Golden Melon #2 On Side Rail")
            locationNamesToRemove.append("Toxic 5 - Golden Melon #1 On Pipe Behind Ship")
            locationNamesToRemove.append("Toxic 5 - Golden Melon #2 Near Rocks After 3rd Tunnel")
        if world.options.include_secret_melons:
            locationNamesToRemove.append("Space 5 - Secret Melon #1 Below Middle Asteroid Rings")
            locationNamesToRemove.append("Space 5 - Secret Melon #2 On Final Asteroid Before Goal Post")
    if world.options.game_version != 1:
        if world.options.include_mega_melons:
            locationNamesToRemove.append("Swamp 6 - Mega Melon #1 Before First Bounce Pad")
            locationNamesToRemove.append("Swamp 6 - Mega Melon #2 On First Stump After Third Bounce Pad")
            locationNamesToRemove.append("Swamp 6 - Mega Melon #3 On Second Stump Before Final Bounce Pad")
            locationNamesToRemove.append("Swamp 6 - Mega Melon #4 Below Golden Melon")
    if world.options.game_version != 2:
        if world.options.include_golden_melons:
            locationNamesToRemove.append("Toxic 5 - Golden Melon On Middle Pipe")
            locationNamesToRemove.append("Desert 5 - Golden Melon #1 On Left Corner Float")
            locationNamesToRemove.append("Desert 5 - Golden Melon #2 On Right Corner Float")
            locationNamesToRemove.append("Desert 5 - Golden Melon #3 Above Pyramid Entrance")
        if world.options.include_secret_melons:
            locationNamesToRemove.append("Toxic 5 - Secret Melon #1 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #2 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #3 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #4 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #5 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #6 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #7 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #8 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #9 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #10 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #11 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #12 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #13 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #14 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #15 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #16 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #17 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #18 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #19 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #20 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #21 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #22 On Inner Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #23 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #24 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #25 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #26 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #27 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #28 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #29 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #30 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #31 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #32 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #33 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #34 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #35 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #36 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Toxic 5 - Secret Melon #37 On Outer Edge Of Pipes")
            locationNamesToRemove.append("Desert 5 - Secret Melon #1 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #2 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #3 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #4 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #5 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #6 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #7 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #8 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #9 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #10 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #11 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #12 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #13 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #13 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #14 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #15 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #16 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #17 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #18 Along Fence")
            locationNamesToRemove.append("Desert 5 - Secret Melon #19 Along Fence")
        if world.options.include_mega_melons:
            locationNamesToRemove.append("Desert 6 - Mega Melon Behind Pyramid")
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if world.options.game_version == 2:
                    if "Castle" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Winter" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Swamp" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Spring King" in location.name:
                        locationNamesToRemove.append(location.name)
                if world.options.game_version != 0:
                    if "PC" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Retro" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Glitch" in location.name:
                        locationNamesToRemove.append(location.name)
                    if "Digital Dilemma" in location.name:
                        locationNamesToRemove.append(location.name)
                if world.options.game_version != 2:
                    if "Community" in location.name:
                        locationNamesToRemove.append(location.name)
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    if world.options.game_version == 0:
        item_config["Level Pack Completion"] = 8 if world.options.include_reverse_levels else 4
        item_config["Progressive Digital Dilemma (Reverse)"] = 3 if world.options.include_reverse_levels else 0
    if world.options.game_version == 1:
        item_config["Level Pack Completion"] = 6 if world.options.include_reverse_levels else 3
    if world.options.game_version == 2:
        item_config["Level Pack Completion"] = 3
    item_config["Auto Brake"] = 0 if world.options.game_version == 2 else 1
    item_config["Progressive Spring King"] = 0 if world.options.game_version == 2 else 3
    item_config["Wooden Planks"] = 0 if world.options.game_version == 2 else 50
    item_config["Snowball"] = 0 if world.options.game_version == 2 else 50
    item_config["Lily Pad"] = 0 if world.options.game_version == 2 else 50
    item_config["Progressive Digital Dilemma"] = 3 if world.options.game_version == 0 else 0
    item_config["RAM Stick"] = 50 if world.options.game_version == 0 else 0
    item_config["Tetromino"] = 50 if world.options.game_version == 0 else 0
    item_config["Corruption"] = 50 if world.options.game_version == 0 else 0
    item_config["Progressive Community Levels"] = 3 if world.options.game_version == 2 else 0
    item_config["Star Ball"] = 1 if world.options.game_version == 2 else 0
    item_config["Snowman Ball"] = 1 if world.options.game_version == 2 else 0
    item_config["Bauble Ball"] = 1 if world.options.game_version == 2 else 0
    item_config["Present Ball"] = 1 if world.options.game_version == 2 else 0
    item_config["LED Lights Ball"] = 1 if world.options.game_version == 2 else 0
    item_config["Red Beach Ball"] = 0 if world.options.game_version == 0 else 1
    item_config["Green Beach Ball"] = 0 if world.options.game_version == 0 else 1
    item_config["Blue Beach Ball"] = 0 if world.options.game_version == 0 else 1
    item_config["LGBTQIA+ Ball"] = 0 if world.options.game_version == 0 else 1
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        remove_specific_item(item_pool, item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # remove_specific_item(item_pool, item_to_place)
    location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Kula Cruise - Pack Complete")
    item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
    location.place_locked_item(item_to_place)
    remove_specific_item(item_pool, item_to_place)
    location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Twilight Tour - Pack Complete")
    item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
    location.place_locked_item(item_to_place)
    remove_specific_item(item_pool, item_to_place)
    if world.options.game_version != 2:
        location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Spring King - Pack Complete")
        item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
        location.place_locked_item(item_to_place)
        remove_specific_item(item_pool, item_to_place)
    if world.options.game_version == 0:
        location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Digital Dilemma - Pack Complete")
        item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
        location.place_locked_item(item_to_place)
        remove_specific_item(item_pool, item_to_place)
    if world.options.game_version != 2:
        if world.options.include_reverse_levels:
            location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Kula Cruise (Reverse) - Pack Complete")
            item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
            location.place_locked_item(item_to_place)
            remove_specific_item(item_pool, item_to_place)
    if world.options.game_version != 2:
        if world.options.include_reverse_levels:
            location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Twilight Tour (Reverse) - Pack Complete")
            item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
            location.place_locked_item(item_to_place)
            remove_specific_item(item_pool, item_to_place)
    if world.options.game_version != 2:
        if world.options.include_reverse_levels:
            location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Spring King (Reverse) - Pack Complete")
            item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
            location.place_locked_item(item_to_place)
            remove_specific_item(item_pool, item_to_place)
    if world.options.game_version == 0:
        if world.options.include_reverse_levels:
            location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Digital Dilemma (Reverse) - Pack Complete")
            item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
            location.place_locked_item(item_to_place)
            remove_specific_item(item_pool, item_to_place)
    if world.options.game_version == 2:
        location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Community Levels - Pack Complete")
        item_to_place = next(i for i in item_pool if i.name == "Level Pack Complete")
        location.place_locked_item(item_to_place)
        remove_specific_item(item_pool, item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    """
        Called when Universal Tracker wants to perform a fake generation
        Use this if you want to use or modify the slot_data for passed into re_gen_passthrough
    """
    return slot_data
