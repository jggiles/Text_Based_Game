# ------------------------------------------------------------------------------
# item.py
# Andrew Ortego
# v. 1.0
# ------------------------------------------------------------------------------
from interface import format_output
import events

class Item:
    def __init__(self):
        ''' The parent class for all item objects in the '''
        self.alias = '<Item ID>'
        self.can_contain = False # Allows other items to be held within itself.
        self.containable = False # Used in <take_from>; True if it can be stored
        self.contained = False # True if self is contained inside another item.
        self.contains_item = False # True if the item contains another item.
        self.description = "<Item Description>"
        self.dropped = False # True implies the item was <taken> at one point.
        self.has_item = False # True implies something is placed on the item.
        self.is_open = False # not closed!
        self.is_taken = False # True if the item is in the actor's inventory.
        self.name = ("<Item Name>", "<Item Name 2>")
        self.placed = False # Used to indicate an item rests upon another item.
        self.size = None # 1 = small, 2 = medium, 3 = venti.
        self.takeable = False # Allows items to be added to actor's inventory.
        self.visible = False # True if the item is printed by the <look> command

    def ask(self, noun = None):
        format_output("The {0} doesn't seem to have much to say.".format(\
            self.name[0]))
        
    def ask_about(self, noun):
        self.ask(noun)
        
    def ask_for(self, noun):
        self.ask(noun)

    def close(self):
        format_output("You cannot open the {}, let alone close it.".format(\
            self.name[0]))

    def drop(self):
        if self in obj.inventory_map['actor']:
            obj.inventory_map['actor'].remove(self)
            current_room_obj = obj.current_game.current_room.__class__.__name__
            if obj.current_actor.up_tree:
                obj.inventory_map['NorthWoods'].append(self)
                format_output("You drop the {0} and it falls to the ground\
                    below.".format(self.name[0]))
            else:
                obj.inventory_map[current_room_obj].append(self)
                format_output("You have dropped the {}.".format(self.name[0]))
            self.is_taken = False
            self.dropped = True
        else:
            format_output("You are not carrying the {}.".format(self.name[0]))

    def eat(self):
        format_output('''I don't think that the {} would agree with you.
            '''.format(self.name[0]))
            
    def enter(self):
        format_output('''There is no enterance here.''')

    def examine(self):
        format_output('''There doesn't seem to be anything particularly special
            about the {}.'''.format(self.name[0]))
        
    def exit(self):
        format_output('''There is no exit here.''')
        
    def hug(self):
        format_output('''You want to what?!''')
        
    def kiss(self):
        format_output('''How's that {0} taste?'''.format(self.name[0]))
        
    def l(self):
        self.look()

    def look(self):
        format_output(self.description)
        
    def move(self):
        format_output("You cannot move the {}.".format(self.name[0]))

    def open(self):
        format_output('''That doesn't look like something you can open.''')

    def place_in(self, containing_item):
        self.place_inside(containing_item)

    def place_inside(self, containing_item):
        ''' self is the item being placed inside the containing_item.'''
        if self.taken == False:
            format_output("You are not currently carrying the {0}".format(\
                self.name[0]))
        elif containing_item.can_contain == False:
            format_output("You cannot place items inside the {0}".format(\
                containing_item.name[0]))
        elif self.size > containing_item.size:
            format_output("The {0} is too large to fit inside the {1}.".format(\
                self.name[0], containing_item.name[0]))
        elif containing_item.is_open == False:
            format_output("The {} is currently closed.".format(\
                containing_item.name[0]))
        elif containing_item.contains_item:
            stored_item = obj.inventory_map.get(\
                containing_item.__class__.__name__)[0]
            format_output("The {0} already contains a {1}.".format(\
                containing_item.name[0], stored_item.name[0]))
        else:
            containing_item_name = containing_item.__class__.__name__
            obj.inventory_map[containing_item_name].append(self)
            obj.inventory_map['actor'].remove(self)
            containing_item.contains_item = True
            self.contained = True
            format_output("The {0} is now in the {1}.".format(\
                self.name[0], containing_item.name[0]))
                
    def place_on(self, containing_item):
        if self.taken == False:
            format_output("You are not currently carrying the {0}".format(\
                self.name[0]))
        elif containing_item.can_contain == False:
            format_output("You cannot place items on the {0}".format(\
                containing_item.name[0]))
        elif self.size > containing_item.size:
            format_output("The {0} is too large to fit on the {1}.".format(\
                self.name[0], containing_item.name[0]))
        elif containing_item.has_item == True:
            format_output("The {0} already has the {1} on top of it.".format(\
                containing_item.name[0], 
                obj.inventory_map[containing_item.__class__.__name__][0]))
        else:
            containing_item_name = containing_item.__class__.__name__
            obj.inventory_map[containing_item_name].append(self)
            obj.inventory_map['actor'].remove(self)
            containing_item.has_item = True
            self.placed = True
            format_output("The {0} is now on top of the {1}.".format(\
                self.name[0], containing_item.name[0]))
                
            if self.name[0] == 'pawn' and containing_item.name[0] == 'board':
                format_output('''A door to the east suddenly appears!''')
                events.pawn_on_board = True
                obj.secondroom.description = obj.secondroom.description + \
                    ''' A secret door has opened to the east.'''

    def put_in(self, containing_item):
        self.place_inside(containing_item)

    def put_inside(self, containing_item):
        self.place_inside(containing_item)
        
    def put_on(self, containing_item):
        self.place_on(containing_item)

    def r(self):
        self.read()

    def read(self):
        format_output("You cannot read the {}.".format(self.name[0]))

    def remove(self):
        if self.is_taken:
            self.drop()
        elif self.contained:
            self.take()
        elif self.placed():
            self.take()

    def remove_from(self, containing_item):
        self.take_from(containing_item)

    def take(self):
        if not self.takeable:
            format_output("You cannot take the {}.".format(self.name[0]))
        elif self in obj.inventory_map['actor']:
            format_output("You already have the {}.".format(self.name[0]))
        elif self.contained or self.placed:
            # Remove the item from the ITEM that contains it, add to inventory.
            current_room_obj = obj.current_game.current_room.__class__.__name__
            for i in obj.inventory_map[current_room_obj]:
                if i.can_contain:
                    containing_item = i.__class__.__name__
                    if self in obj.inventory_map[containing_item]:
                        obj.inventory_map[containing_item].remove(self)
                        i.contains_item = False
            obj.inventory_map['actor'].append(self)
            format_output("You have taken the {}.".format(self.name[0]))
            self.placed = False
            obj.chessboard.has_item = False
            self.is_taken = True
            self.taken()
        else:
            if self.first_take and obj.current_game.tutorial_mode:
                format_output('''** Great, you took the pawn. You can check your
                    inventory to see what you're carrying by typing 'inventory',
                    or 'i' as a shortcut. In fact, lots of common commands have
                    shortcuts, such as 'n' for 'north', and 'se' for
                    southeast...''')
                self.first_take = False
                obj.chesspiece= self
                input('')
                format_output('''** You can interact with some items by
                    placing other items on top of them. Try placing an item from
                    your inventory on something else in this room...''')
                input('')
            # Remove the item from the ROOM that contains it, add to inventory.
            current_room_obj = obj.current_game.current_room.__class__.__name__
            obj.inventory_map[current_room_obj].remove(self)
            obj.inventory_map ['actor'].append(self)
            format_output("You have taken the {}.".format(self.name[0]))
            
        if obj.chesspiece in obj.inventory_map['actor']:
            if events.pawn_on_board:
                events.pawn_on_board = False
                format_output('''The secret door slides shut.''')
                obj.secondroom.description = '''This room is completely black,
                    and the only source of light comes from the white room to
                    the south illuminating a chess board towards the back of the
                    room.'''

    def take_from(self, containing_item):
        if not self.containable:
            format_output("The {0} might be a little too big to be placed in\
                another item.".format(self.name[0]))
        elif not containing_item.can_contain:
            format_output("The {0} does not allow anything to be stored in \
                it.".format(containing_item.name[0]))
        elif not containing_item.is_open:
            format_output("The {0} does not appear to be open.".format(\
                containing_item.name[0]))
        elif not containing_item.contains_item:
            fromat_output("The doesn't appear to be anything in the {0}."\
                .format(containing_item.name[0]))
        elif containing_item.contains_item:
            for i in obj.inventory_map[containing_item.__class__.__name__]:
                if i.name == self.name:
                    self.take()
                else:
                    format_output("The {0} is not inside the {1}".format(\
                        self.name[0], containing_item.name[0]))

    def taken(self):
        ''' Performs an action upon taking an item. Does nothing by default.'''
        pass

    def throw(self):
        current_room_obj = obj.current_game.current_room.__class__.__name__
        if self in obj.inventory_map['actor']:
            format_output("You throw the {}.".format(self.name[0]))
            self.drop()
        elif self in obj.inventory_map[current_room_obj]:
            format_output("You do not have the {}.".format(self.name[0]))
            
    def use(self):
        format_output('''How would you like to use the {}?'''.format(\
            self.name[0]))

    def x(self):
        self.examine()
        
        
# ------------------------------------------------------------------------------
# In-game items
# ------------------------------------------------------------------------------
class Cake(Item):
    def __init__(self):
        Item.__init__(self)
        self.description = "A delicious-looking cake!"
        self.name = ('cake',)
        
    def cut(self):
        format_output('''You have nothing that can cut the cake.''')
        
    def eat(self):
        format_output('''You enjoy the spoils of puzzle-solving by indulging in
            a slice of the cake.''')
        obj.current_game.win()
        
    def slice(self):
        format_output('''You have nothing with which you can slice the cake.''')
        
        
class ChessBoard(Item):
    def __init__(self):
        Item.__init__(self)
        self.can_contain = True
        self.description = "A marble chess board."
        self.first_examine = True
        self.has_item = False
        self.name = ('board',)
        self.size = 2
        
    def examine(self):
        message = self.description
        if self.first_examine and obj.current_game.tutorial_mode:
            format_output('''** Excellent; now you'll see some detailed
                information about how you can interact with the chess board. Try
                to find something else in the room you can 'take'...''')
            input('')
            self.first_examine = False
            obj.chessboard = self
        if events.pawn_on_board:
            message += ' All the pieces of the chess board are now in place.'
        else:
            message += ' It is set up for a game, but a single pawn is missing.'
        format_output(message)
        
        
class ChessPiece(Item):
    def __init__(self):
        Item.__init__(self)
        self.alias = 'piece'
        self.containable = True
        self.description = "A small, black, marble pawn from a chess set."
        self.first_take = True
        self.name = ('pawn',)
        self.size = 1
        self.takeable = True
        self.visible = True
        
    def examine(self):
        format_output('''It's one of the black pawns from a chess board.''')


# Stop deleting here -----------------------------------------------------------
import obj


