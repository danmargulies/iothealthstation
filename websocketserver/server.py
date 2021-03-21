from websocket_server import WebsocketServer
from kinesis_reader import CKinesisReader
import threading
import time

# import random
# import json
# import sys

exitFlag = 0
ck = CKinesisReader("formatted-stream", "us-east-1")
print(ck.my_shard_id)


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        # print_time(self.name, self.counter, 5)
        send_raw_data(self.name)
        print("Exiting " + self.name)


def send_raw_data(threadName):
    ck.startPolling(server.send_message_to_all)


def print_time(threadName, delay, counter):
    while True:
        time.sleep(delay)
        server.send_message_to_all("Hey all, a message from the new thread")
        print("waiting %s: %s" % (threadName, time.ctime(time.time())))


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client["id"])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client["id"])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + ".."
    print("Client(%d) said: %s" % (client["id"], message))


PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)

# run my thread
# Create two threads as follows
thread1 = myThread(1, "Thread-1", 1)
thread1.start()
server.set_fn_message_received(message_received)
print("starting local server")
server.run_forever()
