import yapgvb

def generate_graph(game):
    graph = yapgvb.Graph("game_graph")
    
    nodes = {}
    for node in game.boardLayout.nodes:
        nodes[node] = graph.add_node(str(node), label=hex(node))
        
        # Is house
        if game.boardLayout.nodes[node].owner != None:
            nodes[node].shape = yapgvb.shapes.house
        
        # Harbour
#        if game.boardLayout.nodes[node].harbor != 0:
#            nodes[node].shape = yapgvb.shapes.doublecircle
        
    for road in game.boardLayout.roads.values():
        edge = graph.add_edge(nodes[road.n1], nodes[road.n2])
        
    for tile,node in game.boardLayout.tiles.items():
        n = graph.add_node(str(tile), label=hex(tile), fontsize=16)
        n.shape = yapgvb.shapes.circle
        for i in range(1, 7):
            id = getattr(node, "n%d"%i)
            e = graph.add_edge(n, nodes[id])
            e.decorate = True
    
        
    graph.layout(yapgvb.engines.neato)
    format = yapgvb.formats.png
    graph.render("world-dump.%s" % format)

"""
def generate_random_graph(nnodes = 20, nedges = 80):
    import random
    graph = yapgvb.Digraph("my_graph")

    for i in xrange(nnodes):
        # Create a node named str(i)
        node = graph.add_node(str(i))

        # Assign a random shape and color
        node.shape = random.choice(yapgvb.shapes.values())
        node.color = random.choice(yapgvb.colors.values())

    # Get all of the nodes as a list 
    # (the graph.nodes attribute is an iterator)
    nodes = list(graph.nodes)

    for i in xrange(nedges):
        head = random.choice(nodes)
        tail = random.choice(nodes)
        edge = tail >> head
        edge.color = random.choice(yapgvb.colors.values())

    return graph

if __name__ == '__main__':
    print "Generating a random directed graph..."
    graph = generate_random_graph()
    
    print "Using dot for graph layout..."
    graph.layout(yapgvb.engines.dot)
    
    demo_formats = [
#        yapgvb.formats.jpg,
        yapgvb.formats.png,
#        yapgvb.formats.ps,
#        yapgvb.formats.svg,
    ]
    
    for format in demo_formats:
        filename = 'graph.%s' % format

        print "  Rendering %s ..." % filename

        graph.render(filename)
        
"""