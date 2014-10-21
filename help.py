import interface
from obj import current_game
from interface import format_output
from collections import OrderedDict as OD
      
class Menu:
    def __init__(self):
        self.confusing = True
        self.cursor = '> '
        self.header = None # Set in print_title()
        self.width = current_game.console_width
        
        self.functions = {
            '1' : self.print_me,
            '2' : self.print_me,
            '3' : self.print_me,
            '4' : self.load_game,
            '5' : self.flip_menu,
            }
        
        self.fun_menu = OD()
        self.fun_menu['1'] = 'What is this? Where am I? Who are you?'
        self.fun_menu['2'] = 'How do I play this thing?'
        self.fun_menu['3'] = 'Let\'s start a game from the beginning!'
        self.fun_menu['4'] = 'I want to continue where I left off.'
        self.fun_menu['5'] = 'I don\'t understand. I am confused.'

        self.boring_menu = OD()
        self.boring_menu['1'] = 'About This Game'
        self.boring_menu['2'] = 'Instructions'
        self.boring_menu['3'] = 'Start a New Game'
        self.boring_menu['4'] = 'Load a Saved Game'
        
        self.current_menu = self.fun_menu
        
    def print_menu(self):
        ''' Prints the contents of one menu or the other.'''
        if self.confusing:
            self.current_menu = self.fun_menu
        else:
            self.current_menu = self.boring_menu
        for k, v in self.current_menu.items():
            print('  ', k, ':', v)
        
    def print_title(self):
        ''' Print the title of the main menu.'''
        if self.confusing:
            self.header = 'Drew\'s Text-Based Game Demo'
        else:
            self.header = 'The Main Menu'
        stars = '-' * ((self.width//2) - len(self.header) + 1)
        print(stars, self.header, stars)
                
    def flip_menu(self):
        '''This actually toggles the two menu's on and off, but I left option 
           '5' out of the "boring" menu. It's funnier that way.'''
        if self.confusing:
            print('Oh, I\'m sorry... here, try this one...')
        else:
            print('Make sense now?')
        print('\n')
        self.confusing = not self.confusing
        
    def load_game(self):
        '''Option 4'''
        print('Load Game')
        format_output('''Well, you could do that, but you haven't saved a game
            yet. You know how I know that? Because there isn't even a function 
            to save the game yet. So nice try. Also, please write that function 
            if you can. Or pay someone else to do it. Better yet, pay Drew to do
            it! Now back to the menu with you!!''')
        print('\n')
        input('Press any key to return to the menu.')
        
    def print_me(self):
        print('TODO...')
        
    def menu_loop(self):
        ''' Prompts the user to select a menu item.'''
        while(True):
            self.print_title()
            self.print_menu()
            choice = input(self.cursor)
            print('\n')
            if choice not in (self.current_menu.keys()):
                print('That\'s not a choice... let\'s try this again...')
                print('\n')
            else:
                self.functions[choice]()
            
        

print('\n')
format_output(interface.copyright)
print('\n')
m = Menu()
m.menu_loop()        
    
    
