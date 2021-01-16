# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:59:48 2020

Streamlining branches in classes

@author: lando
"""

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
            objs = objs + ' In the room there is '
            for obj in self.details['objects'][:-1]:
                objs = objs + obj + ', '
            objs = objs + 'and ' + self.details['objects'][-1] + '.'
        elif len(self.details['objects']) > 1 :
            objs = objs + ' In the room there is ' + self.details['objects'][0] + ' and ' + self.details['objects'][1] + '.'
        elif len(self.details['objects']) == 1 :
            drs = drs + ' In the room there is ' + self.details['objects'][0] + '.'
        else:
            pass
        
        drs = ''
        if len(self.details['doors']) > 2 :
            drs = drs + ' There are doors to the '
            for dr in self.details['doors'][:-1]:
                drs = drs + dr + ', the '
            drs = drs + 'and the ' + self.details['doors'][-1] + '.'
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
    

living_room = Room('living room')
living_room.add('objects',['a navy blue sofa', 'a large flat screen TV','two recliners'])
living_room.add('doors',['kitchen','hallway'])
living_room.add('extras',['you hear a bird squawk'])

print(living_room)

living_room.remove('objects','a large flat screen TV')
living_room.replace('objects','a navy blue sofa','a bright red futon')

print(living_room)

