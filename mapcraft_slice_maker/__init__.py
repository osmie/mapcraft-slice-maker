import sys
import argparse
import fiona
import osmwriter
from collections import defaultdict

def write_data(inputdata, outputfilename):
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


    writer = osmwriter.OSMWriter(outputfilename)
    for (x, y), nodeid in sorted(nodes.items(), key=lambda x: x[1]):
        writer.node(nodeid, y, x, version=1)

    max_way_id = 1
    for shape in inputdata:
        if shape['geometry']['type'] == 'Polygon':
            way_nodes = []
            way_id = max_way_id
            max_way_id += 1
            outer_ring = shape['geometry']['coordinates'][0]
            for x, y in outer_ring:
                way_nodes.append(nodes[(x, y)])
            way_nodes.append(nodes[outer_ring[0]])
            writer.way(way_id, {}, way_nodes, version=1)
        elif shape['geometry']['type'] == 'MultiPolygon':
            for poly in shape['geometry']['coordinates']:
                way_nodes = []
                way_id = max_way_id
                max_way_id += 1
                outer_ring = poly[0]
                for x, y in outer_ring:
                    way_nodes.append(nodes[(x, y)])
                way_nodes.append(nodes[outer_ring[0]])

                writer.way(way_id, {}, way_nodes, version=1)
        else:
            raise NotImplementedError()

    writer.close()





def convert(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Group by this field value", default=None)
    parser.add_argument("inputfile", help="Input shp/geojson file", metavar="INPUT")
    parser.add_argument("outputfile", help="Output OSM XML filename, or prefix", metavar="OUTPUT")

    options = parser.parse_args(args)

    with fiona.open(options.inputfile) as fp:
        inputdata = list(fp)

    if options.group:
        grouped = defaultdict(list)
        for shape in inputdata:
            grouped[shape['properties'].get(options.group)].append(shape)

        for key in grouped.keys():
            write_data(grouped[key], "{}{}.osm".format(options.outputfile, key))

    else:
        write_data(inputdata, options.outputfilename)


def main():
    return convert(sys.argv[1:])

if __name__ == '__main__':
    main()
