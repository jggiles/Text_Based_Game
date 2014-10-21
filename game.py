# ------------------------------------------------------------------------------
# game.py
# Andrew Ortego
# v. 1.0
# ------------------------------------------------------------------------------
from interface import format_output

class Game:
    def __init__(self):
        self.brief_msg = False
        #self.console_width = int(os.popen('stty size', 'r').read().split()[0])
        self.completed_moves = 0
        self.console_width = 70
        self.current_room = None
        self.prompt_char = "\n> "
        self.tutorial_mode = None
        self.verbose_msg = True
        
    @property
    def current_room(self):
        return self._current_room
        
    @current_room.setter
    def current_room(self, new_room):
        self._current_room = new_room

    def brief(self):
        ''' Activates brief descriptions for rooms. Deactivates verbose
            descriptions.'''
        if self.brief_msg:
            format_output("Brief descriptions are already activated.")
        else:
            self.brief_msg = True
            self.verbose_msg = False
            format_output("Brief descriptions are now on.")
        obj.current_game = self
        
    def help(self):
        ''' Prints a list of available commands.'''
        print ("The Help Menu! Coming soon! Or not ever!")
        
    def hint(self):
        ''' Invoked from tokenizer; prints the hint for the current room.'''
        from obj import leaflet, current_game
        if not leaflet.is_taken:
            format_output("You don't have the item needed to use that command.")
        elif leaflet.is_taken:
            current_game.current_room.hint()
        else:
            print("You hit an error with the <hint> command! --Drew")
        
    def inventory(self):
        ''' Formats and prints the current items in the actor's inventory.'''
        from obj import inventory_map
        if inventory_map['actor'] == []:
            format_output("You don't have anything in your inventory.")
        else:
            item_list = [i for i in inventory_map['actor']]
            inventory_message = "You are currently carrying "
            for i in item_list:
                inventory_message += "a {}".format(i.name[0])
                if item_list.index(i) + 1 == len(item_list):
                    inventory_message += "."
                elif item_list.index(i) + 2 == len(item_list):
                    inventory_message += ", and "
                else:
                    inventory_message += ", "
            format_output(inventory_message)
            
    def i(self):
        ''' Shortcut to the "inventory" command.'''
        self.inventory()
        
    def load(self):
        print("Coming soon!")
        
    def moves(self):
        ''' Displays the number of successful moves that have been made.'''
        format_output("You have executed {} valid commands.".format(\
            self.completed_moves))
            
    def print_header(self):
        ''' Prints the current room's name and number of moves.'''
        move_msg = "moves: " + str(self.moves)
        spaces = self.console_width -len(self.current_room.name) -len(move_msg)
        print(); print()
        print(self.current_room.name + (" " * spaces) + move_msg)
        print("-" * self.console_width)
    
    def prompt(self, new_prompt = ""):
        ''' Creates a new prompt to precede the user's input. Updates the 
            "prompt_char" attribute of the game object.'''
        if new_prompt == "":
            new_prompt = input("Type a new prompt and press <Enter>: ")
        self.prompt_char = "\n" + new_prompt + " "
        
    def save(self):
        print("Coming soon!")
        
    def tutorial_choice(self):
        format_output('''Welcome to the game demo! If you haven't played this
            before then there are a few things you'll need to know. If you have
            played before then you can totally skip this intro stuff.''')
        while self.tutorial_mode == None:
            prompt = input('''Have you played this game before? (y/n) ''' + \
                self.prompt_char)
            if prompt.lower() in ['yes', 'y']:
                self.tutorial_mode = False
            elif prompt.lower() in ['no', 'n']:
                self.tutorial_mode = True
            else:
                format_output('''I didn't understand your input. Type 'yes' or 
                    'no' and press Enter.''')
            
    def quit(self):
        ''' Prompts user for verification to exit the game.'''
        prompt = input("Are you sure you want to quit? " + self.prompt_char)
        if prompt.lower() == 'yes' or prompt.lower() == 'y':
            print ("It's game over, man! GAME OVER!!\n")
            raise SystemExit
        else:
            print ("OK, nevermind then.")

    def verbose(self):
        ''' Activates verbose descriptions for rooms. Deactivates brief
            descriptions.'''
        if self.verbose_msg:
            format_output("Verbose is already on.")
        else:
            self.brief_msg = False
            self.verbose_msg = True
            format_output("Maximum verbosity.")
        obj.current_game = self
        
    def win(self):
        format_output("Congrats! You've completed the game!")
        raise SystemExit
                          
import obj


