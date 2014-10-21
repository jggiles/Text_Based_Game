# ------------------------------------------------------------------------------
# item.py
# Andrew Ortego
# v. 1.0
# Moved line 22 (call to pattern_match) inside the if-statement
# ------------------------------------------------------------------------------
import obj, tokenizer, interface, room
from interface import format_output

def start_game():    
    # Print the start message, toggle tutorial mode
    print('\n')
    format_output('-' * obj.current_game.console_width)
    format_output(interface.copyright)
    format_output('-' * obj.current_game.console_width)
    obj.current_game.tutorial_choice()
    
    # Print the 'look' command after setting the current room
    print ('\n')
    obj.current_game.current_room = room.FirstRoom()
    format_output(obj.current_game.current_room.name)
    interface.look()

    while(True):
        ''' Get the user's input, create tokens out of it, and process them.'''
        #current_game.print_header()
        user_input = [word for word in input(\
            obj.current_game.prompt_char).split()]
        if user_input:
            tokenized_input = tokenizer.get_token(user_input)
            if tokenized_input:
                token_pattern = tokenizer.pattern_match(tokenized_input)
                if token_pattern:
                    tokenizer.execute_command(
                        tokenized_input,
                        token_pattern,
                        obj.current_game)
            else:
                pass
        else:
            print("Pardon?")

if __name__ == "__main__":
    start_game()
    
    
