import networkx


def StringToVec(string):
    """
    Converts a string such as "[1,2,3]" to a triple: (1,2,3)
    :param string:
    :return: a triple representing the vector that was in string form
    """
    # '[-14000,-14000,103000]'
    # Remove brackets
    string = string.replace('[', '')
    string = string.replace(']', '')
    # Split into coords
    xyzStrings = string.split(",")
    xyz = []
    try:
        for cord in xyzStrings:
            xyz.append(float(cord))
        vec = (xyz[0], xyz[1], xyz[2])
        return vec
    except:
        return "malformed"


def grabGraphDataFromTxt(filePath):
    """
    Creates a node graph from the file given
    The file is assumed to be in the format: "[x1,y1,z1]:[x2,y2,z2]:...:[xn,yn,zn]"
    Each line is assumed to represent a vector and its neighbors, the first vector is chosen as the node
    :param filePath:
    :return: A graph built from the vectors in the file
    """
    graph = networkx.Graph()
    graphFile = open(filePath, 'r')

    lines = graphFile.readlines()
    #print(lines)

    centersList = []
    neighborsList = []
    for line in lines:
        # Remove unwanted characters
        line = line.rstrip("\n\r")
        # Break line apart by the ':' character
        neighborStrings = line.split(":")
        # pop center off of list and convert to a vector
        center = StringToVec(neighborStrings.pop(0))
        if center != "malformed":
            graph.add_node(center)
            for neighbor in neighborStrings:
                graph.add_edge(center, StringToVec(neighbor))
        else:
            print("mal:", center)
    print("nodeCount:", graph.number_of_nodes())
    print("edgeCount:", graph.number_of_edges())

    return graph
