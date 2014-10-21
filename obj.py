# ------------------------------------------------------------------------------
# obj.py
# Andrew Ortego
# v. 1.0
# ------------------------------------------------------------------------------
import actor, game, item, room

current_game  = game.Game()
current_actor = actor.Actor()

# Rooms ----------------------------------
firstroom  = room.FirstRoom()
secondroom = room.SecondRoom()
thirdroom = room.ThirdRoom()

# Items ----------------------------------
cake = item.Cake()
chessboard = item.ChessBoard()
chesspiece = item.ChessPiece()

# Inventory Map keeps track of the location of each item in the game. Items that
# can contain objects are also mapped in this dictionary.
# Each room and can_contain-enabled item must be mapped here.

inventory_map = {
    # Inventory ----------------------------------
    'actor' : [],

    # Rooms --------------------------------------
    'FirstRoom': [],
    'SecondRoom' : [chesspiece, chessboard],
    'ThirdRoom' : [cake,],

    # Items --------------------------------------
    'ChessBoard' : [],
    }

    
