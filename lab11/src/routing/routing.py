from deepdiff import DeepDiff
import copy

net1 = {
    0 : {3 : 7, 2 : 3, 1 : 1},
    1 : {0 : 1, 2 : 1},
    2 : {1 : 1, 0 : 3, 3 : 2},
    3 : {0 : 7, 2 : 2},
}

net2 = {
    0 : {3 : 1, 2 : 3, 1 : 1},
    1 : {0 : 1, 2 : 1},
    2 : {1 : 1, 0 : 3, 3 : 2},
    3 : {0 : 1, 2 : 2},
}

def send(net, routing, boxes):
    for src, data in routing.items():
        for dst, info in data.items():
            cost, _, new = info
            for ip, queue in boxes.items():
                if src in net[ip] and new:
                    queue.append((src, dst, cost))
                    data[dst] = (info[0], info[1], False)

def calc(net, routing, boxes):
    new = copy.deepcopy(routing)
    for ip, queue in boxes.items():
        for src, dst, cost in queue:
            if dst == ip:
                continue
            cost = cost + net[ip][src]
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
        for dst, cost in data.items():
            routing[src][dst] = (cost, dst, True)
    return routing

def create_boxes(net):
    boxes = {}
    for src, _ in net.items():
        boxes[src] = []
    return boxes

def print_net(net):
    for src, data in net.items():
        for dst, cost in data.items():
            print(f"{src} -> {dst}, cost={cost}")

def print_routing(routing):
    for src, data in routing.items():
        print(f"src={src}")
        for dst, (cost, next, _) in data.items():
            print(f"dst={dst} next={next} cost={cost}")

def simulate(net):
    routing = create_routing(net)
    boxes = create_boxes(net)
    next = True
    while next:
        send(net, routing, boxes)
        new = calc(net, routing, boxes)
        next = DeepDiff(new, routing)
        routing = new
    print_routing(routing)

print("Simulation for net1")
print_net(net1)
simulate(net1)

print("Simulation for net2")
print_net(net2)
simulate(net2)
