# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:59:03 2020

@author: Landon Work
"""
#from Rooms import Room

class Room:
    
    def __init__(self,name:str,objects=[],doors=[],extras=[]):
        self.name = name
        self.details = {'objects':objects,'doors':doors,'extras':extras}
        self.make_text()
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.text
    
    def remove(self,name,text):
        if bool(name):
            self.details[name].remove(text)
        else:
            for i in self.details:
                i.remove(text)
        self.make_text()
    
    def add(self, name: str, li: list):
        self.details[name].extend(li)
        self.make_text()
        
    def replace(self,name,obj,new_obj):
        self.details[name]=[new_obj if x==obj else x for x in self.details[name]]
        self.details[name].sort()
        self.make_text()
    
    def make_text(self):
        
        intro = f'You are in the {self.name}.'
        
        objs = ''
        if len(self.details['objects']) > 2 :
            objs = objs + ' In the room, there is '
            for obj in self.details['objects'][:-1]:
                objs = objs + obj + ', '
            objs = objs + 'and ' + self.details['objects'][-1] + '.'
        elif len(self.details['objects']) > 1 :
            objs = objs + ' In the room, there is ' + self.details['objects'][0] + ' and ' + self.details['objects'][1] + '.'
        elif len(self.details['objects']) == 1 :
            drs = drs + ' In the room, there is ' + self.details['objects'][0] + '.'
        else:
            pass
        
        drs = ''
        if len(self.details['doors']) > 2 :
            drs = drs + ' There are doors to the '
            for dr in self.details['doors'][:-2]:
                drs = drs + dr + ', the '
            drs = drs + self.details['doors'][-2] + ', and the ' + self.details['doors'][-1] + '.'
        elif len(self.details['doors']) > 1 :
            drs = drs + ' There are doors to the ' + self.details['doors'][0] + ' and the ' + self.details['doors'][1] + '.'
        elif len(self.details['doors']) == 1 :
            drs = drs + ' There is a door to the ' + self.details['doors'][0] + '.'
        else:
            pass
        
        extra = ' '
        for x in self.details['extras']:
            extra = extra + x.capitalize() + '. '
            
        self.text = intro + objs + drs + extra

#from Items import Item
#from Events import Event
#from People import Person

def run_game():
        
    # Room constants here
    LIVING_ROOM = 0
    KITCHEN     = 1
    BEDROOM    = 2
    HALLWAY     = 3
    BACKYARD    = 4
    # FOYER = 1
    # BASEMENT = 5
    # ATTIC = 6
    
    # Declare the state-of-the-world variable
    game = {'loc': 0, 'inv': [], 'rooms': [], 'game_end': None}
    
    # Win/lose constants
    WIN = True
    LOSE = False
    
    # Initialize inventory
    game['inv'].append('key')
    
    # Initialize rooms
    living_room = Room('living room',[],[],[])
    living_room.add('objects',['a navy blue sofa', 'a large flat screen TV','two recliners'])
    living_room.add('doors',['kitchen','hallway'])
    living_room.add('extras',['you hear a bird squawk'])
    
    kitchen = Room('kitchen',[],[],[])
    kitchen.add('doors',['backyard','living room'])
    hallway = Room('hallway',[],[],[])
    hallway.add('doors',['bathroom','bedroom','living room'])
    bedroom = Room('bedroom',[],[],[])
    bedroom.add('doors',['hallway'])
    
    game['rooms'].extend([living_room,kitchen,bedroom,hallway])
    
    # def take_action(inp,game):
    #     # Take the first 3 letters of each word and put into a list
    #     pass
        
    # def action_switch(action):
    #     switch = {
    #         'liv': move
    #         'kit': move
    #         'hal': move
    #         'bac': move
    #         'bat': move
    #         }
        
    # def move(inp):
    #     game['loc']=game['rooms'].index(inp)
    
    while (game_end == None):
        print(game['rooms'][game['loc']])
        inp = input('What would you like to do?')
        event = take_action(inp,game)
        game = event.activate(game)
        
        if win_condition:
            game_end = WIN
            break
        if lose_condition:
            game_end = LOSE
            break
    
    return game_end