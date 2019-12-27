# HMind is an agent coordinator designed to be used in the PC game Garry's Mod.
Built and designed with the purpose of versitle, HMind communicates with programs running within Garry's Mod for the purpose of controlling various agents within the game.

HMind coordinates agents through a series of files, each agent has a file it uses to give and recieve information and orders while targets are found in a list of entities written to the directory by a supporting script that mines data on players, props, and other in-game objects. The data is the processed and made available to HMind in the form of the Agent and Target classes. HMind then uses this data on command to find the best path to the targets as well as which agent-target match ups are optimal.

The pathfinding is done with A* from NetworkX with a herusitic given to HMind in the init function. The heuristic is used is the eculidian distance between two nodes (points) where the z differnce is weighted higher. The reason for the weighting is so that the agents would make an effort to use roads and alleyes instead of just flying over obstacles.

Targets are assigned using an agents loss function; the sum of the agents loss values for a set of agent-target pairings is used to evaluate the set. The set with the least loss is chosen. If the loss for a pairing is below a threshold, the agent will be assigned that path and target to act on, otherwise it is told to do nothing.


For a broad view, HMind and the agents, along with the supporting scripts, read and edit files to achieve inter-process communication. The reason a better solution for shared memory was not chosen is that the in-game scipting language for Garry's Mod is extremely limited and has only extremely basic options.
This language is from wiremod addon and focuses on in-game operations like moving objects or displaying visual effects and does not have any way to communicate with programs running outside of the game other than writing and reading files from a single local directory.
For this reasons HMind had to be designed around Garry's mod, hence the obscure formating requirements.

# NetworkX citation:
Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008
