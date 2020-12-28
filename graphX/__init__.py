import algorithmx as ax
from pathlib import Path
import os

def _remove_dupes(x):
  return list(dict.fromkeys(x))

class Node:
    def __init__(self, val):
        self.val = str(val)
        self.attrs = {}

    def __repr__(self):
        """this is what the node will look like if it was printed"""
        return f"Node('{self.val}', {self.attrs})"

    def __str__(self):
        """This is the string representation of the node, and will be used in setting edges and getting specific nodes"""
        return self.val  

    def set_attr(self, attr, val):
        """sets a nodes specific attribute (eg. seen, size, etc.)"""
        self.attrs[attr] = val

    def get_attr(self, attr):
        """returns an attribute"""
        return self.attrs[attr]

class Graph:
    def __init__(self, is_jupyter=False, port=5050, width=300, height=200, custom_ui=None):
        self.nodes = {}
        self.edges = {}
        self.canvas = ""
        self.port = port
        if is_jupyter:
            self.canvas = ax.jupyter_canvas()
            self.canvas.size((width, height))
            # print("loaded Canvas")
            display(self.canvas)
        else:
            if custom_ui == None:
                # finds the interface html. This is more complicated than it should be
                base_path = os.path.relpath(__file__)
                #custom_ui = str((base_path / "/ui.html").resolve())
                custom_ui = f"{Path(base_path).parent}/ui.html"
            print("serving ui found at", custom_ui)
            self.server = ax.http_server(port=port, file=custom_ui)
            self.canvas = self.server.canvas()
            

    # boring running stuff for web
    def run_web(self, func):
        def wrapper():
            self.canvas.onmessage('start', func)
            print(f"staring server on http://localhost:{self.port} — press ctrl+c to quit")
            # TODO: use custom html template that removes algX branding.
            self.server.start()
        return wrapper

    def _dispactch_dict(self, dict):
        self.canvas.dispatch({"hello":"cool"})
    # Nodes
    def add_node(self, n):
        """adds node "n" to the graph"""
        self.nodes[n] = Node(n)
        self.canvas.node(Node(n)).add(color="#423f39")

    def add_nodes(self, n_list):
        """runs "add_node" for each node in the iterable"""
        for n in n_list:
            self.add_node(n)
    
    def get_nodes(self):
        """returns a list of all the nodes in a graph"""
        return [self.nodes[i] for i in self.nodes]
    
    def get_node(self, val):
        """returns a specific node"""
        return self.nodes[val]

    def del_node(self, val):
        """deletes a specified node"""
        self.nodes.pop(val, None)
        self.canvas.node(val).remove()
    # Edges
    def add_edge(self, source, target, value=1, directed=False):
        """adds edges between source and target nodes. if it isn't directed it will also add a target to source edge."""
        # adds dict to source node edges if there are no other edges
        if source not in self.edges:
            self.edges[source] = {}
        # adds dict to target node edges if there are no other edges
        if target not in self.edges:
            self.edges[target] = {}
        # sets the s->t edge to be equal to value
        self.edges[source][target] = value
        # if it isn't directed, add the edge the other way as well.
        if not directed:
            self.edges[target][source] = value
        # draw the s->t edge on the canvas.
        self.canvas.edge((source, target)).add(directed=directed, color="#c8c3b8")

    def del_edge(self, source, target):
        """deletes a specified edge between a target and a source"""
        self.edges[source].pop(target, None)
        # checks if the edge is stored the other way around as well (undirected)
        if source in self.edges[target]:
            print("[warning]", "deleting undirected edge", f"{source}->{target}")
            self.edges[target].pop(target, None)
        # deletes the edge from the canvas
        self.canvas.edge((source, target)).remove()

    def traverse_edge(self, source, target, color="#4a83ff"):
        """plays a little animation going from the source node to the target node along their edge"""
        self.canvas.edge((source, target)).traverse(color)

    # general, graph-wide, methods 
    def pause(self, time=1):
        """pauses the animation for `time` seconds"""
        self.canvas.pause(time)

if __name__ == "__main__":
    g = Graph()

    @g.run_web
    def start():
        """for i in "graphX":
            g.add_node(i)
            g.pause(0.5)
        g.pause()
        for i in "graphX":
            for j in "graphX":
                g.add_edge(i, j)
                g.pause(0.25)
        g.pause()
        for i in range(len("graphX") -1):
            g.traverse_edge("graphX"[i], "graphX"[i+1])
            g.pause(0.5)
        print(g.get_nodes())"""
        for i in "ab":
            g.add_node(i)
        g.pause()
        g.add_edge("a", "b")
        g.pause()
        g.traverse_edge("b", "a")
        g.pause()
        g.del_edge("b", "a")
        #g._dispactch_dict({})
    start()


""" # Create a new HTTP server on port 5050
server = ax.http_server(port=4000)
# Create a new canvas
canvas = server.canvas()

def start():
    # Use the library normally, for example:
    canvas.nodes([1, 2]).add()
    canvas.edge((1, 2)).add()

    canvas.pause(1)

    canvas.node(1).highlight().size('1.5x').pause(0.5)
    canvas.edge((1, 2)).traverse('blue')

# A 'start' message is sent by the client whenever the
# user clicks the start or restart button
canvas.onmessage('start', start)

# Start the server, blocking all further execution on
# the current thread. Use 'ctrl-c' to exit the script.
server.start() """