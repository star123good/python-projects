# Python program for implementation of Ford Fulkerson algorithm 
# Complexity : (E*(V^3)) 
# CreateNewGraph and BFS => V^2 times 

#This class represents a directed graph using adjacency matrix representation 
class Graph: 

	def __init__(self,graph): 
		self.graph = graph # residual graph 
		self. ROW = len(graph) 
		#self.COL = len(gr[0]) 
		

	'''Returns true if there is a path from source 's' to sink 't' in 
	residual graph. Also fills parent[] to store the path '''
	def BFS(self,s, t, parent): 

		# Mark all the vertices as not visited 
		visited =[False]*(self.ROW) 
		
		# Create a queue for BFS 
		queue=[] 
		
		# Mark the source node as visited and enqueue it 
		queue.append(s) 
		visited[s] = True
		
		# Standard BFS Loop 
		while queue: 

			#Dequeue a vertex from queue and print it 
			u = queue.pop(0) 
		
			# Get all adjacent vertices of the dequeued vertex u 
			# If a adjacent has not been visited, then mark it 
			# visited and enqueue it 
			for ind, val in enumerate(self.graph[u]): 
				if visited[ind] == False and val > 0 : 
					queue.append(ind) 
					visited[ind] = True
					parent[ind] = u 

		# If we reached sink in BFS starting from source, then return 
		# true, else false 
		return True if visited[t] else False
			
	
	# Returns tne maximum flow from s to t in the given graph 
	def FordFulkerson(self, source, sink): 

		# This array is filled by BFS and to store path 
		parent = [-1]*(self.ROW) 

		max_flow = 0 # There is no flow initially 

		# Augment the flow while there is path from source to sink 
		while self.BFS(source, sink, parent) : 

			# Find minimum residual capacity of the edges along the 
			# path filled by BFS. Or we can say find the maximum flow 
			# through the path found. 
			path_flow = float("Inf") 
			s = sink 
			while(s != source): 
				path_flow = min (path_flow, self.graph[parent[s]][s]) 
				s = parent[s] 

			# Add path flow to overall flow 
			max_flow += path_flow 

			# update residual capacities of the edges and reverse edges 
			# along the path 
			v = sink 
			while(v != source): 
				u = parent[v] 
				self.graph[u][v] -= path_flow 
				self.graph[v][u] += path_flow 
				v = parent[v] 

		return max_flow 


# create new Graph from edges and vertices
def CreateNewGraph(graph, vertices):
    result = []
    ROW = len(graph)
    
    # create empty graph 2D array
    for u in range(2*ROW):
        result.append([])
        for v in range(2*ROW):
            result[u].append(0)

    # fill in the blanks of result array with graph array
    for u in range(ROW):
        for v in range(ROW):
            result[2*u+1][2*v] = graph[u][v]

    # fill in the blanks of result array with vertices array
    for u in range(ROW):
        result[2*u][2*u+1] = vertices[u]

    return result


def main():
    # Create a graph given in the above diagram 

    graph = [[0, 16, 13, 0, 0, 0], 
            [0, 0, 10, 12, 0, 0], 
            [0, 4, 0, 0, 14, 0], 
            [0, 0, 9, 0, 0, 20], 
            [0, 0, 0, 7, 0, 4], 
            [0, 0, 0, 0, 0, 0]] 

    # Create a vertices with weights

    vertices = [25, 10, 18, 21, 26, 24]

    # Create a new graph from graph and vertices

    new_graph = CreateNewGraph(graph, vertices)

    g = Graph(new_graph) 

    # start node
    source = 0
    #end node
    sink = 10

    print ("The maximum possible flow is %d " % g.FordFulkerson(source, sink)) 



if __name__ == '__main__':
    main()