from deepdiff import DeepDiff
import copy
import json
import sys

def read_net(file):
    with open(file) as f:
        return json.load(f)

def send(net, routing, boxes):
    for src, data in routing.items():
        for dst, info in data.items():
            cost, _, new = info
            for ip, queue in boxes.items():
                if src in net[ip] and new:
                    queue.append((src, dst, cost))
                    data[dst] = (info[0], info[1], False)

def calc(_, routing, boxes):
    new = copy.deepcopy(routing)
    for ip, queue in boxes.items():
        for src, dst, cost in queue:
            if dst == ip:
                continue
            cost = cost + 1
            cost = min(cost, 16)
            if dst in new[ip]:
                if new[ip][dst][0] > cost:
                    new[ip][dst] = (cost, src, True)
            else:
                new[ip][dst] = (cost, src, True)
        queue.clear()
    return new

def create_routing(net):
    routing = {}
    for src, _ in net.items():
        routing[src] = {}
    for src, data in net.items():
        for dst in data:
            routing[src][dst] = (1, dst, True)
    return routing

def create_boxes(net):
    boxes = {}
    for src, _ in net.items():
        boxes[src] = []
    return boxes

def print_net(net):
    for src, data in net.items():
        for dst in data:
            print(f"{src} -> {dst}")

def print_routing(routing):
    for src, data in routing.items():
        print(f"src={src}")
        for dst, (cost, next, _) in data.items():
            print(f"dst={dst} next={next} cost={cost}")

def simulate(net, verbose):
    routing = create_routing(net)
    boxes = create_boxes(net)
    next = True
    i = 1
    while next:
        if verbose:
            print(f"Step {i}")
            print_routing(routing)
        send(net, routing, boxes)
        new = calc(net, routing, boxes)
        next = DeepDiff(new, routing)
        routing = new
        i += 1
    print("Final")
    print_routing(routing)

net = read_net(sys.argv[1])
verbose = len(sys.argv) == 3
print("Simulation")
print_net(net)
simulate(net, verbose)
