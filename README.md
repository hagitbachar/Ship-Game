# Ship-Game

hagitba
208349746
Hagit Bachar

I discussed the exercise with: Paz Cohen ,yechzkel raff, Josh Hershkovitz,
 Liron sade

web pages:

http://stackoverflow.com


==================
=  Description:  =
==================
This program creates a game.
There is two classes, the first one is 'ship':
every ship has 4 params:
pos- minimum coordinate
length- the length of the ship
direction- first direction of the ship
board size- the size of the square-shaped board

The role of class ship is to represent a ship, class ship has some function:
'move' function moves all the ship, the function notice that each ship don't
 exceed from the board.
'hit' function updates the ship if the ship has damaged
'terminated' function checks if the ship is damaged
'__contain__' function checks if the ship in specific coordinate
'coordinates' function return a list of all the coordinates of each ship
'damaged cell' function return a list of all the damaged coordinates
'direction' function return the last direction of the ship
'cell status' function return the status of a specific coordinate
'__repr__' function return the represent of the ship

The role of class game is to run the game, the main function in class game are:
'play one round'- this function run a single turn, in every turn the user
insert a coordinate of bomb, the bomb placed on the board, all the ships move
one step by their direction, the ships updated vulnerability, the bombs
updated on the on the board, there is screen printing board, and there is a
user reports on the number of injuries and terminated ships at the last turn.

and 'play' function director the game.

The progress of the game:
Game Progress:
Each time the user has to enter the coordinates of a bomb, the ships move one step in their direction, if the bomb is in one of the coordinates of the ship, coordinates become *, if each ship is destroyed, the ship is removed from the board.
