import enum
from dataclasses import dataclass

import numpy

import GraphBuilder
import networkx
import heapq

@dataclass
class HMind:
    navGraph: networkx.DiGraph
    agents: []
    targets: []

    def __init__(self, navGraph, heuristic, distance):
        self.navGraph = navGraph
        self.heuristic = heuristic
        self.distance = distance

        self.agents = []
        self.targets = []

    def setGraphFile(self, filePath):
        """
        Creates a node graph from the file and sets it to be used as the HMinds navigation graph
        :param filePath:
        """
        self.navGraph = GraphBuilder.grabGraphDataFromTxt(filePath)

    def pathToTargetNetX(self, loc1, loc2):
        """
        Finds a series of nodes that when traversed, leads leads from loc1 to loc2
        Uses A* with the heuristic function given in the HMind init with weights being cost
        :param loc1:
        :param loc2:
        :return:
        """
        shortestPath = networkx.astar_path(self.navGraph, loc1, loc2, heuristic=self.heuristic, weight='cost')
        return shortestPath

    def coordinate(self):
        """
        Finds the optimal target to agent assignments by finding every possible assignment and evaluating it with the agents loss function
        Once found, the targets are assigned to their respective best match if the loss for that match up is under the agents threshold
        :return: nothing, used to exit when there are no agents or targets
        """
        # check if enough actors
        if len(self.agents) < 1 or len(self.targets) < 1:
            print("not enough actors")
            return

        # update agents closest nodes
        self.assignClosestNodesToActors()

        # generate possible plans
        options = []
        for target in self.targets:
            plan = []
            error = 0
            for agent in self.agents:
                path = self.pathToTargetNetX(agent, target)
                loss = agent.loss(agent, target, path)
                error += loss
                order = (path, agent, target, loss)
                plan.append(order)
            option = (plan, error)
            options.append(option)

        # find best plan
        bestPlan = options[0]
        leastError = bestPlan[1]
        for plan in options:
            error = plan[1]
            if error < leastError:
                leastError = error
                bestPlan = plan

        # assign orders to agents from plan
        bestPlanOrders = bestPlan[0]
        for order in bestPlanOrders:
            agent = order[1]  # agent
            target = order[2]  # target
            path = order[0] # path from agent to target
            if agent.loss(agent, target, path, loss) >= agent.threshold:
                agent.target = target
                agent.path = path
            else:
                if agent.home is not None:
                    agent.path = self.pathToTargetNetX(agent.location, agent.home)

    def addAgent(self, agent):
        """
        Checks if the agent has been added before. If the agent is new, it is added. If it has already been added, the agent will be updated
        :param agent:
        """
        # check if the agent has been added before
        if agent not in self.agents:  # add the new agent
            self.agents.append(agent)
        else:  # otherwise update agent existing data
            index = self.agents.index(agent)
            self.agents[index] = agent

    def removeAgent(self, agent):
        """
        Removes the agent from the list of agents
        :param agent:
        """
        # remove the agent
        self.agents.remove(agent)

    def addTarget(self, target):
        """
        Checks if the target has been added before. If the target is new, it is added. If it has already been added, the target will be updated
        :param agent:
        """
        # check if the target has been added before
        if target not in self.targets:  # add the new target
            self.targets.append(target)
        else:  # otherwise update existing target data
            index = self.targets.index(target)
            self.targets[index] = target

    def removeTarget(self, target):
        """
        Removes the agent from the list of target
        :param target:
        """
        # remove the target
        self.targets.remove(target)

    # Assumes nodes are x,y,z points
    def assignClosestNodesToActors(self):
        """
        Uses the distance function provided in the HMind init to assign a node to agents and targets
        Actors will snap to the closest node to them in the navGraph
        """
        navGraph = self.navGraph
        navNodes = navGraph.nodes

        for agent in self.agents:
            nearest = None
            minDist = self.distance(navNodes[0], agent.location)
            for node in navNodes:
                dist = self.distance(node, agent.location)
                if dist < minDist:
                    minDist = dist
                    nearest = node
            agent.node = nearest

        for target in self.targets:
            nearest = None
            minDist = self.distance(navNodes[0], target.location)
            for node in navNodes:
                dist = self.distance(node, target.location)
                if dist < minDist:
                    minDist = dist
                    nearest = node
            target.node = nearest


@dataclass
class Target:
    iD: int# id of target
    name: str# string name of target
    purpose: str  # role of target
    priority: int  # priority of target
    location: ()  # actual position of target
    node: ()  # node the target is closest to

    def __init__(self, iD, name, purpose,  location):
        """
        Creates an target will the provided parameters
        :param iD: ID of target
        :param name: Name of Target
        :param purpose: Why does the target exist
        :param location: location of the target, may or may not be a node
        """
        self.iD = iD
        self.name = name
        self.purpose = purpose
        self.location = location

    def __eq__(self, other):
        return self.iD == other.iD

    def __repr__(self):
        return str(self.iD)+" Target "+self.name+", is at: "+str(self.location)


@dataclass
class Agent:
    # agent data
    iD: int  # id of agent
    name: str  # name of agent
    purpose: str  # role of agent
    threshold: int  # max loss

    # other
    #loss: function

    # location data
    home: ()  # position agent should return to when no appropriate target is present
    location: ()  # actual position of agent
    node: ()  # node the agent is closest to

    # agent orders
    target: Target  # target of agent
    path: []  # list of nodes to visit

    def __init__(self, iD, name, purpose,  location, loss, threshold):
        """
        Creates an agent will the provided parameters
        :param iD: ID of agent
        :param name: Name of agent
        :param purpose: Why does the agent exist
        :param location: location of the agent, may or may not be a node
        :param loss: How good is a target match up? lower numbers are assumed to be better
        :param threshold: The maximum tolerable loss
        """
        self.iD = iD
        self.name = name
        self.purpose = purpose
        self.location = location
        self.loss = loss
        self.threshold = threshold

    def __eq__(self, other):
        return self.iD == other.iD

    def __repr__(self):
        agentStr = "Agent: "+str(self.iD)+": "+self.name+", is at: "+str(self.location)
        #targetStr = " is pursuing: "+str(self.iD)+" Target: "+self.target.name+", at: "+str(self.target.location)
        return agentStr#+targetStr

