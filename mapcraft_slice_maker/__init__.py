import sys
import argparse
import fiona
import osmwriter

def convert(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")

    options = parser.parse_args(args)

    with fiona.open(options.inputfile) as fp:
        inputdata = list(fp)


    nodes = {}
    max_node_id = 1
    for shape in inputdata:
        if shape['geometry']['type'] == 'Polygon':
            for ring in shape['geometry']['coordinates']:
                for x, y in ring:
                    if (x, y) not in nodes:
                        nodes[(x, y)] = max_node_id
                        max_node_id += 1
        elif shape['geometry']['type'] == 'MultiPolygon':
            for poly in shape['geometry']['coordinates']:
                for ring in poly:
                    for x, y in ring:
                        if (x, y) not in nodes:
                            nodes[(x, y)] = max_node_id
                            max_node_id += 1

        else:
            raise NotImplementedError()


    writer = osmwriter.OSMWriter(options.outputfile)
    for (x, y), nodeid in sorted(nodes.items(), key=lambda x: x[1]):
        writer.node(nodeid, y, x, version=1)

    max_way_id = 1
    for shape in inputdata:
        way_nodes = []
        way_id = max_way_id
        max_way_id += 1
        if shape['geometry']['type'] == 'Polygon':
            outer_ring = shape['geometry']['coordinates'][0]
            for x, y in outer_ring:
                way_nodes.append(nodes[(x, y)])
            way_nodes.append(nodes[outer_ring[0]])
        elif shape['geometry']['type'] == 'MultiPolygon':
            for poly in shape['geometry']['coordinates']:
                outer_ring = poly[0]
                for x, y in outer_ring:
                    way_nodes.append(nodes[(x, y)])
                way_nodes.append(nodes[outer_ring[0]])
        else:
            raise NotImplementedError()
        writer.way(way_id, {}, way_nodes, version=1)

    writer.close()




def main():
    return convert(sys.argv[1:])

if __name__ == '__main__':
    main()
