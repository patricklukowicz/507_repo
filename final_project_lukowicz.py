#########################################
##### Name: Patrick Lukowicz        #####
##### Uniqname: lukowicz            #####
#########################################

import plotly.graph_objects as go
import scrape_cache as scrape
import scrape_cache_2 as scrape2
from collections import deque

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,weight=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], weight)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

def BFS(startpoint, endpoint, graph):
    q = deque()
    q.append(startpoint)

    while q:
        startpoint = q.popleft()
        print(startpoint)
        for edge in graph.VertList[startpoint]:
            if not endpoint[edge]:
                edge = True
                q.append(edge)

    return q

if __name__ == "__main__":
    MC5_Band = scrape.MC5_info
    Detroit_Bands = scrape2.band_urls
    xvals = [MC5_Band]
    yvals = [Detroit_Bands]
    bar_data = go.Bar(x=xvals, y=yvals)
    basic_layout = go.Layout(title='Detroit Music Relationships')
    fig = go.Figure(data=bar_data, layout=basic_layout)

    while True:
        bad_queries = ['', ' ']
        query = str(input('Enter a Detroit band or "exit" to quit: '))
        if query in bad_queries:
            print("Ope, invalid entry, please re-enter search term.")
            continue
        if query == "exit":
            print("Bye!")
            break
        if query.isascii():
            fig.show()
            continue
