# README


### The Game
Ricochet Robots!

This is a competitive board game [boardgamegeek link](https://boardgamegeek.com/boardgame/51/ricochet-robots) where you have a 16x16 grid of squares, some with walls between them, and some with destination symbols on top of them. The game pieces on top of the board are 5 robots with unique colors, and take up a space on the board, with no overlapping allowed. Robots move in a cardinal direction until bumping into an obstacle, similar to [Pokemon ice physics](https://bulbapedia.bulbagarden.net/wiki/Ice_tile#Slippery_ice_tile). These obstacles are: the sides of the board, one of the walls within the board, a center block of walls, or another robot. For each of the 17 destination symbols on the board, there is a corresponding token that is printed on one side, and hidden on the other. Each of these symbols has a color that corresponds to one of the robot pieces on the board, with one multi-color symbol that accepts any robot. The number of players is uncapped, with at least 2 because the game is competitive. A "turn" of the game is as follows:
* Flip one of the destination tokens at random
* All in your head, figure out a path to get the robot with the color of the symbol to that square on the grid
* Once you have figured out such a path, call out the number of moves it would take you to get there, and begin a 30-second timer
* Before the timer expires, any player (including the initial one who called it) may find paths to the same destination with fewer moves, and can call it out
* When the timer expires, the player who last called a number (it should be the minimal number of moves found), performs the moves and earns the symbol token, which is worth one point
* Note that the robots now have different initial positions for the next turn

After you finish the turn for the last symbol token, you tally the total number of points for each player to determine the winner.


### The Repository
The repository here is a simulator for the above board game. The features included are:
* N/A