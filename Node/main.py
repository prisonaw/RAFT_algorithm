from platform import node
import socket
import threading
import os
from heartbeat import AppendEntryMessage, RequestVoteRPC
import heartbeat
import nodes
import json
import random
import time
import traceback

# persistent data
voted_for = None
global which_term
which_term = 0
Log = []
# node1 = nodes.nodes[0].name
global state
state = "follower"
global votes_receieved
votes_receieved = 0


# references: https://docs.python.org/3/howto/sockets.html
def send_heartbeat(skt, name):
    print("leader is executed")
    msg = AppendEntryMessage(
        {"leaderId": name, "Entries": [], "prevLogIndex": -1, "prevLogTerm": which_term}
    )

    #  does this need to be an infinite loop
    for x in nodes.nodes:
        if x.name != name:
            skt.sendto(json.dumps(msg).encode("utf-8"), (x))

def send_vote_request(skt):
    


def listener(skt: socket):
    state = "follower"
    global endOfTimeout
    while True:
        t = random.uniform(100, 500)
        skt.settimeout(t)
        timeNow = time.monotonic()
        try:
            (msg, addr) = skt.recvfrom(1024)
            print("here1")
            StrVal = msg.decode("utf-8")
            JsonVal = json.loads(StrVal)
            print("received heartbeat from:", JsonVal["leaderId"])
        except:
            print("timeout")

            if state == "follower":
                print("here4")
                which_term += 1
                state = "candidate"
                votes_receieved += 1
                voteReq = RequestVoteRPC(which_term, "node", -1, 0)

                # request vote from other nodes
            else:
                print("state is: ", state, timeNow)
                # possible issue that the value keeps reseting everytime it doesn't recieve a heartbeat, essentially pushing the timedout val later andlater
                # timeout = random.uniform(100, 500)
                # endOfTimeout += timeout
                # endOfTimeout = time.monotonic() + timeout

    # start election if timeout reached


if __name__ == "__main__":

    # Creating Socket and binding it to the target container IP and port
    skt = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    host = "127.0.0.1"
    # Bind the node to sender ip and port
    skt.bind((host, 5555))

    threading.Thread(target=listener, args=[skt]).start()

    time.sleep(10)
