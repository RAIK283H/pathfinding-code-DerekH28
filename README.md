# Pathfinding Starter Code
This is a game to test the effectiveness of depth first search, breath first search, Dijkstra, and random pathing. The game works by pre creating paths and having a each search technique, represented by a player, find a target and then find an exit. 

In terms of changes made by me I worked on all the search and random path functions as well as scoreboard updates to display a new objectives reached variable and display and decide a winner on the scoreboard.

The only current known issue is a issue that exists with the pyglet, for some reason the depressed keyword does not work with the current version of pyglet so I could not run the game because I could not use the depressed button.

The depth first search function was created using a helper function that actually calulates the depth first search and then an assert statement that cycles through the path given and finds any potential post condition errors.

Breath first search uses two while loops to find both the path to the target node and then the path to the exit node, it uses a queue in order to keep track of nodes that have been visited. 