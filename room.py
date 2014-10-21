# ------------------------------------------------------------------------------
# room.py
# Andrew Ortego
# v. 1.0
# ------------------------------------------------------------------------------
import item, obj, events
from interface import format_output

class Room:
    def __init__(self):
        self.name = "<Room Name>"
        self._description = "<Decorator Room Description>"
        self.default_direction = "You can't go that way."
        
    @property
    def description(self):
        return self._description
                          
    def hint(self):
        '''<game.hint()> calls this function on the current_room.'''
        format_output("The leaflet is blank.")
    
    def look(self):
        ''' Print information about the current room.'''
        format_output(self.description)
                    
        if item.inventory_map[self.name]:
            for i in item.inventory_map[self.name]:
                print ("There is a", i.name, "here.")
                    
    def north(self): return {'message' : self.default_direction}
    def east(self) : return {'message' : self.default_direction}
    def south(self): return {'message' : self.default_direction}
    def west(self) : return {'message' : self.default_direction}
    def northeast(self): return {'message' : self.default_direction}
    def southeast(self): return {'message' : self.default_direction}
    def southwest(self): return {'message' : self.default_direction}
    def northwest(self): return {'message' : self.default_direction}
    def up(self)   :  return {'message' : "You can't go that way."}
    def down(self) :  return {'message' : "You can't go that way."}
    
    def n(self) : return self.north()
    def e(self) : return self.east()
    def s(self) : return self.south()
    def w(self) : return self.west()
    def ne(self): return self.northeast()
    def se(self): return self.southeast()
    def sw(self): return self.southwest()
    def nw(self): return self.northwest()
    def u(self) : return self.up()
    def d(self) : return self.down()
    
    
class FirstRoom(Room):
    def __init__(self):
        Room.__init__(self)
        self.first_visit  = True
        self.default_direction = 'You cannot go that way from here.'
        self.description = '''You are in a well-lit, completely white room. The
            walls are glossy, and it's hard to differentiate the dimensions of
            this room. There is a black passageway to the north.'''
        self.name = 'White Room'
        self.tutorial_message_1 = '''** Here we go... this game is divided up
            into a series of rooms. You can navigate between rooms by entering
            the direction you want to travel, such as 'north' or 'southeast'...
            '''
        self.tutorial_message_2 = '''** Once you enter a room you'll see the
            name of the room printed out, followed by a description of the room.
            Press any key to see this, and try to move out of the room...'''
        self.tutorial_message_3 = '''** Nice, you got yourself out of the White
            Room, and now you're about to enter a new room...'''
        self.tutorial_message_4 = '''** Note that this room has two items in 
            it-- a chess piece and a chess board. You can interact with these 
            items with commands like 'look' and 'examine.' Try using those 
            commands by saying something like 'examine board'...'''
        
        if obj.current_game.tutorial_mode and self.first_visit == True:
            format_output(self.tutorial_message_1)
            input('Press any key to continue...')
            print('\n')
            format_output(self.tutorial_message_2)
            input('\n')
            
    @property
    def description(self):
        return self._description
        
    @description.setter
    def description(self, description):
        self._description = description
            
    def east(self):
        if obj.chesspiece in obj.inventory_map['ChessBoard']:
            return {'movement' : obj.thirdroom}
        else:
            return {'message' : self.default_description}  
        
    def north(self):
        if obj.current_game.tutorial_mode and self.first_visit == True:
            format_output(self.tutorial_message_3)
            input('\n')
            format_output(self.tutorial_message_4)
            input('\n')
            self.first_visit = False
            obj.firstroom = self # Update/hack so that 'visited' persists
        return {'movement' : obj.secondroom}
        
        
class SecondRoom(Room):
    def __init__(self):
        Room.__init__(self)
        self.default_direction = 'You cannot go that way.'
        self.description = '''This room is completely black, and the only source
            of light comes from the white room to the south illuminating a chess
            board towards the back of the room.'''
        self.first_visit = True
        self.name = 'Black Room'
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, new_desc):
        self._description = new_desc
        
    def east(self):
        if events.pawn_on_board:
            if obj.current_game.tutorial_mode:
                format_output('''** Well done! You're about to move into the
                    third and final room of this demo. Can you solve the 
                    diabolical last puzzle too!?''')
                input('')
            return {'movement' : obj.thirdroom}
        else:
            return {'message' : self.default_direction}
        
    def south(self):
        return {'movement' : obj.firstroom}
        
        
class ThirdRoom(Room):
    def __init__(self):
        Room.__init__(self)
        self.default_direction = 'You cannot go that way.'
        self.description = '''The final room! There's a cake for you here so
            that you can celebrate beating the demo.'''
        self.name = 'Gray Room'
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, new_desc):
        self._description = new_desc
        
    def west(self):
        return {'movement' : obj.secondroom}
        
        
