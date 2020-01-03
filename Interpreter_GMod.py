import time

from HMind import *
import glob

print("Running Garry's mod layer")


class Purpose(enum.Enum):
    atck = 0
    defs = 1


def lossATK(agent, target, path):
    return len(path)


def heuristic(vec1, vec2):
    squaredDistance = ((vec1[2] - vec2[2]) ** 2)*5  # 0.5  # 10
    squaredDistance += ((vec1[1] - vec2[1]) ** 2)*1
    squaredDistance += ((vec1[0] - vec2[0]) ** 2)*1
    return numpy.sqrt(squaredDistance)


def distanceEuclid3D(vec1, vec2):
    squaredDistance = 0
    for d in range(0, 2):
        squaredDistance += (vec1[d] - vec2[d])**2
    return numpy.sqrt(squaredDistance)


def writeOrders(HMind):
    lines = ""
    for agent in HMind.agents:
        try:
            output = agent.iD
            path = ""
            for vec in agent.path:
                vecS = str(vec)[:-1]
                vecS = vecS.replace(" ", "")
                path += vecS[1:] + ">"
            path = path[:-1]
            lines += output+"~"+path+"\n"
        except:
            HMind.removeAgent(agent)
    file = open(orderPath, "w")
    file.write(lines)
    file.close()


def updateEntityData():
    entityDataFile = open(dataPath, 'r')
    entitiesS = entityDataFile.read().split("\n")
    for entityS in entitiesS:
        attributes = entityS.split("\t")
        if attributes[0] == "player":  # type
            location = GraphBuilder.StringToVec(attributes[2])
            target = Target(attributes[1], attributes[1], Purpose.atck, location)
            HMind.addTarget(target)
            #print(target)
        elif attributes[0] == "agent":  # type
            id = attributes[3]
            type = attributes[2]
            if type == "hk":
                purpose = Purpose.atck
                loss = lossATK
            location = GraphBuilder.StringToVec(attributes[4])
            agent = Agent(id, "agent", purpose, location, loss, 99999)
            if attributes[1] == "online":
                HMind.addAgent(agent)
            else:
                HMind.removeAgent(agent)
            #print(agent)


# file paths
graphPath = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data\e2files\nodegraph_gm_bigcity.txt"
orderPath = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data\e2files\orders.txt"
dataPath = r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod\data\e2files\entities.txt"

# graph
navGraph = GraphBuilder.grabGraphDataFromTxt(graphPath)

# HMind
HMind = HMind(navGraph, heuristic, distanceEuclid3D)

#updateEntityData()
#updateAgentData()


while True:
    print("updating")
    updateEntityData()
    #updateAgentData()
    HMind.coordinate()
    for agent in HMind.agents:
        print(agent.target)
    writeOrders(HMind)
    time.sleep(0.5)#0.1

'''
def updateAgentData():
    agentFiles = glob.glob(orderPath + "\\" + "out_ace*")

    for agentFile in agentFiles:
        agentFile = open(agentFile, 'r')
        attributes = agentFile.read().split("\n")[0].split(":")
        if attributes[0] == "online":
            location = GraphBuilder.StringToVec(attributes[1])
            agent = Agent(1, "ace-hk-1", Purpose.atck, location, lossATK, 99999)
            HMind.addAgent(agent)
            print(agent)
'''

'''
def getEuclideanDistanceNDim(vec1, vec2, dimNum):
    squaredDistance = 0
    for d in range(0, dimNum-1):
        squaredDistance += (vec1[d] - vec2[d])**2
    return numpy.sqrt(squaredDistance)

'''

'''
def writeOrders(HMind):
    for agent in HMind.agents:
        try:
            file = open(orderPath + "\\in_" + str(agent.name) + ".txt", "r")
            lines = file.readlines()
            firstLine = lines[0]
            status = firstLine.split(":")[0]
            if status != "online":
                HMind.removeAgent(agent)
            file.close()
            file = open(orderPath + "\\in_" + str(agent.name) + ".txt", "w")
            output = ""
            for vec in agent.path:
                vecS = str(vec)[:-1]
                vecS = vecS.replace(" ", "")
                output += vecS[1:] + ":"
            output = output[:-1]
            file.write(firstLine+output)
            file.close()
        except:
            HMind.removeAgent(agent)
'''