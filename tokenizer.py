 # ------------------------------------------------------------------------------
# tokenizer.py
# Andrew Ortego
# v. 1.0
# TODO fleshing out the pattern_match function to indicate which word is invalid
# TODO process two-word noun's (e.g. small mailbox) as a single noun.
# ------------------------------------------------------------------------------
import commands, item, obj, interface
from interface import format_output
from operator import methodcaller
from random import randint

valid_patterns = ( # Globally accessible to pattern_match and process_tokens
    ['verb'],
    ['direction'],
    ['noun'],
    ['interface'],
    ['verb', 'noun'],
    ['noun', 'verb'],
    ['verb', 'direction'],
    ['verb', 'preposition', 'noun'],
    ['verb', 'preposition', 'preposition', 'noun'],
    ['verb', 'noun', 'combine', 'noun'],
    ['verb', 'preposition', 'noun', 'combine', 'noun'],
    ['verb', 'noun', 'combine', 'preposition', 'noun'],
    ['verb', 'preposition', 'noun', 'combine', 'preposition', 'noun']
    )

def get_token(user_input):
    ''' Tokenizes the given input and returns a list element. Skips over the
        ignore commands.'''
    tokenized_words = []
    for word in user_input:
        if word in commands.verbs:
            tokenized_words.append({'verb': word})

        elif word in commands.nouns:
            tokenized_words.append({'noun': word})

        elif word in commands.directions:
            tokenized_words.append({'direction': word})

        elif word in commands.combine:
            tokenized_words.append({'combine': word})

        elif word in commands.interface:
            tokenized_words.append({'interface': word})

        elif word in commands.preposition:
            tokenized_words.append({'preposition': word})

        else:
            print("I don't recognize the word {0}.".format(word))
            return []

    return tokenized_words

def pattern_match(tokenized_input):
    ''' Compares the word-type pattern of the user's input to a list of valid
        patterns. If valid, returns True.'''
    global valid_patterns
    user_pattern = [list(token_key.keys())[0] for token_key in tokenized_input]
    if user_pattern in valid_patterns:
        return user_pattern
    else:
        format_output("I didn't understand that sentence.")
        return False

def execute_command(tokenized_input, token_pattern, current_game):
    ''' Processes a valid input-pattern and executes command(s).'''
    global valid_patterns

    if token_pattern == ['direction']:
        token_dir(tokenized_input, current_game)

    elif token_pattern == ['verb']:
        token_verb(tokenized_input, current_game)

    elif token_pattern == ['noun']:
        token_noun(tokenized_input, current_game)

    elif token_pattern == ['interface']:
        token_interface(tokenized_input, current_game)

    elif token_pattern == ['verb', 'noun']:
        token_verb_noun(tokenized_input, current_game)

    elif token_pattern == ['verb', 'preposition', 'noun'] or \
         token_pattern == ['verb', 'preposition', 'preposition', 'noun']:
        stripped_list = strip_preposition(tokenized_input, current_game)
        token_verb_noun(stripped_list, current_game)

    elif token_pattern == ['noun', 'verb']:
        token_noun_verb(tokenized_input, current_game)

    elif token_pattern == ['verb', 'direction']:
        token_verb_direction(tokenized_input, current_game)

    elif token_pattern == ['verb', 'noun', 'combine', 'noun']:
        token_combined_nouns(tokenized_input, current_game)

    elif token_pattern == ['verb', 'preposition', 'noun', 'combine', 'noun']:
        stripped_list = strip_preposition(tokenized_input, current_game)
        token_combined_nouns(stripped_list, current_game)

    elif token_pattern == ['verb', 'noun', 'combine', 'preposition', 'noun']:
        stripped_list = strip_preposition(tokenized_input, current_game)
        token_combined_nouns(stripped_list, current_game)

    elif token_pattern == ['verb', 'preposition', 'noun',
        'combine', 'preposition', 'noun']:
        stripped_list = strip_preposition(tokenized_input, current_game)
        token_combined_nouns(stripped_list, current_game)

def get_key(token):
    ''' Returns the key of a token dict. Python3 doesn't allow for iterable
        dict's, thus we have to cast the dict to a list and return an index.'''
    return list(token.keys())[0]

def get_value(token):
    ''' Same as get_key, but for dict value's. FYI: iteritems won't work since
        the dictionary items are seperate and must maintain a specific order.'''
    return list(token.values())[0]

def is_available(noun, location = 'all'):
    ''' Returns an item-object if the given noun is currently available to the
        actor. The "location" parameter accepts a string which indicates the
        location of the noun being searched for.'''
    current_room = obj.current_game.current_room.__class__.__name__

    if location == 'all' or location == 'room':
        for i in obj.inventory_map[current_room]:
            if noun in i.name:
                return i

            elif i.contains_item or i.has_item:
                stored_item = obj.inventory_map.get(i.__class__.__name__)[0]
                if noun in stored_item.name and stored_item.visible:
                    return stored_item

    if location == 'all' or location == 'actor':
        for i in obj.inventory_map['actor']:
            if noun in i.name:
                return i

    else:
        return None

# ------------------------------------------------------------------------------
# Input-processing functions (called from execute_command)
# ------------------------------------------------------------------------------

def token_dir(tokenized_input, current_game):
    ''' Process a single direction command.'''
    get_direction = methodcaller(get_value(tokenized_input[0]))
    direction = get_direction(current_game.current_room)

    if get_key(direction) is 'message':
        format_output(get_value(direction))

    elif get_key(direction) is 'movement':
        current_game.current_room = get_value(direction)
        format_output(current_game.current_room.name)
        if current_game.verbose_msg:
            interface.look()
    current_game.completed_moves += 1

def token_verb(tokenized_input, current_game):
    ''' Process a single verb-command. "look" is unique as it can be used with
        or without an item.'''
    verb = get_value(tokenized_input[0])
    if verb == 'look' or verb == 'l':
        interface.look()
    else:
        format_output("What do you want to {}?".format(verb))
    current_game.completed_moves += 1

def token_noun(tokenized_input, current_game):
    ''' Process a single noun-command.'''
    noun = get_value(tokenized_input[0])
    if is_available(noun):
        format_output("What would you like to do with the {}?".format(noun))
    else:
        format_output("I don't see a {} here.".format(noun))
    current_game.completed_moves += 1

def token_interface(tokenized_input, current_game):
    ''' Process an interface-command.'''
    command = methodcaller(get_value(tokenized_input[0]))
    command(current_game)

def token_verb_noun(tokenized_input, current_game):
    ''' Process an action upon a noun. First, determine if the item is present,
        then-- if so-- execute it's corresponding verb command.'''
    noun = get_value(tokenized_input[1])
    noun_obj = is_available(noun)
    if noun_obj:
        verb = get_value(tokenized_input[0])
        command = methodcaller(verb)
        command(noun_obj)
    else:
        format_output("I don't see a {} here.".format(noun))
    current_game.completed_moves += 1

def token_noun_verb(tokenized_input, current_game):
    ''' Reverse the contents of tokenized_input and process as a verb-noun.'''
    tokenized_input = tokenized_input[::-1]
    token_verb_noun(tokenized_input, current_game)

def token_verb_direction(tokenized_input, current_game):
    ''' Processes verbs associated with movement, but ultimately just executes
        a lone direction command.'''
    verb = get_value(tokenized_input[0])
    if verb in ['move']:
        direction = []
        direction.append(list(tokenized_input)[1])
        token_dir(direction, current_game)
    else:
        format_output("You used the word {} in a way I don't understand.".\
            format(verb))
        current_game.completed_moves += 1

def token_combined_nouns(tokenized_input, current_game):
    ''' Uses a 'combine' command to allow two items to interact. Agnostic to
    the noun's location.'''
    verb  = get_value(tokenized_input[0])
    noun1 = get_value(tokenized_input[1])
    action = get_value(tokenized_input[2])
    noun2 = get_value(tokenized_input[3])

    noun_obj1 = is_available(noun1)
    noun_obj2 = is_available(noun2)

    if noun1 == noun2:
        format_output("I don't recogni... wait, what?")
    elif noun_obj1 == None:
        format_output("I don't see a {} here.".format(noun1))
    elif noun_obj2 == None:
        format_output("I don't see a {} here.".format(noun2))
    else:
        function_name = '_'.join([verb, action])
        m = [method for method in dir(noun_obj1) if callable(getattr(noun_obj1,\
            method))]
        if function_name in m:
            command = methodcaller(function_name, noun_obj2)
            command(noun_obj1)
        else:
            format_output("You combined the words '{0}' and '{1}' in way I \
                didn't understand".format(verb, action))
    current_game.completed_moves += 1

def strip_preposition(tokenized_input, current_game):
    ''' Strip out the preposition(s) and call the token_combined_nouns func.'''
    preposition_removed = []
    for t in tokenized_input:
        if get_key(t) != 'preposition':
            preposition_removed.append(t)
    return preposition_removed
    
    
