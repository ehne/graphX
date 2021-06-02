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

    def get_size(self):
        """returns the approximate length the node's graph representation would have to be to show all the text"""
        size = 0  # in milinches
        for s in self.val:
            if s in "lij|' ":
                size += 1.3
            elif s in "![]fI.,:;/\\t":
                size += 2
            elif s in '`-(){}r"':
                size += 2
            elif s in "*^zcsJkvxy":
                size += 3
            elif s in "aebdhnopqug#$L+<>=?_~FZT0123456789":
                size += 3.5
            elif s in "BSPEAKVXY&UwNRCHD":
                size += 4
            elif s in "QGOMm%W@—":
                size += 5
            else:
                size += 5
        # above code slightly adjusted from: https://stackoverflow.com/questions/16007743/roughly-approximate-the-width-of-a-string-of-text-in-python
        # print("node" ,f"'{self}'", "length before padding", size, "after", size + 5)
        return size + 5


class Graph:
    def __init__(
        self, is_jupyter=False, port=5050, width=300, height=200, custom_ui=None
    ):
        self.nodes = {}
        # stores edges in the form source: target
        self.edges = {}
        # reverse edges dict is used to store the edges in the form of target: source
        self.reverse_edges = {}
        self.canvas = ""
        self.port = port
        if is_jupyter:
            self.canvas = ax.jupyter_canvas()
            self.canvas.size((width, height))
            # print("loaded Canvas")
            display(self.canvas)
        else:
            if custom_ui is None:
                # finds the interface html. This is more complicated than it should be
                base_path = os.path.relpath(__file__)
                # custom_ui = str((base_path / "/ui.html").resolve())
                custom_ui = f"{Path(base_path).parent}/ui.html"
            print("serving ui found at", custom_ui)
            self.server = ax.http_server(port=port, file=custom_ui)
            self.canvas = self.server.canvas()#.edgelayout("individual")

    # boring running stuff for web
    def run_web(self, func):
        def wrapper():
            self.canvas.onmessage("start", func)
            print(
                f"staring server on http://localhost:{self.port} — press ctrl+c to quit"
            )
            self.server.start()

        return wrapper

    def _dispactch_dict(self, dispatch_dict):
        self.canvas.dispatch(dispatch_dict)

    # Nodes
    def add_node(self, n):
        """adds node "n" to the graph"""
        self.nodes[n] = Node(n)
        self.canvas.node(Node(n)).add(
            color="#423f39", size=(Node(n).get_size(), 12), shape="rect"
        )

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
    def add_edge(self, source, target, value=1, directed=False, weight=1):
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
        # update the reverse dict
        self._update_reverse_edge_dict()
        # draw the s->t edge on the canvas.
        self.canvas.edge((source, target)).add(directed=directed, color="#c8c3b8", labels={0:{'text':weight}})

    def del_edge(self, source, target):
        """deletes a specified edge between a target and a source"""
        self.edges[source].pop(target, None)
        # checks if the edge is stored the other way around as well (undirected)
        if source in self.edges[target]:
            print("[warning]", "deleting undirected edge", f"{target}->{source}")
            self.edges[target].pop(target, None)
        # update the reverse dict
        self._update_reverse_edge_dict()
        # deletes the edge from the canvas
        self.canvas.edge((source, target)).remove()

    def traverse_edge(self, source, target, color="#4a83ff"):
        """plays a little animation going from the source node to the target node along their edge"""
        self.canvas.edge((source, target)).traverse(color)

    def get_edge(self, source, target):
        return self.edges[source][target]

    def get_outgoing_edges(self, source):
        """returns the edges (as tuples) leaving the source node"""
        return [(source, target) for target in self.edges[source]]

    def get_incoming_edges(self, target):
        """returns the edges (as tuples) that are entering the target node"""
        return [(source, target) for source in self.reverse_edges[target]]
    def _update_reverse_edge_dict(self):
        # clear the dict so that deleted edges don't play havoc.
        self.reverse_edges = {}
        for target in self.nodes:
            self.reverse_edges[target] = {}
        for source, target_dict in self.edges.items():
            for target, val in target_dict.items():
                self.reverse_edges[target].update({source: val})
    # general, graph-wide, methods
    def pause(self, time=1):
        """pauses the animation for `time` seconds"""
        self.canvas.pause(time)


if __name__ == "__main__":
    g = Graph()

    @g.run_web
    def start():

        g.add_nodes([1,2,3,4])

        g.add_edge(4, 2, weight=60)
        g.add_edge(1, 2, weight=80)
        g.add_edge(1, 3, weight=120)
        g.add_edge(2, 3, weight=70)
        g.add_edge(3, 4, weight=90)
        print(g.edges)
        print(g.reverse_edges)
        print(g.get_incoming_edges(1))
        # g._dispactch_dict({})

    start()
