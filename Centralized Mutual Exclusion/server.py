#name : Pooja Ashok Jeergyal
#Id : 100686373



import socket
import time
import thread
import threading
import os
from Tkinter import *

import Queue

text=""


global q
q = Queue.Queue()


def perform_server_operation(conn,addr):
    global text
    print ("connected by", addr, conn)
    while True:
        received_from_client = conn.recv(1024)
        rand = received_from_client.decode('utf-8').split("\r\n")[-1]
        http_message = received_from_client.decode("utf-8")
        print(http_message)
        #   check if its a int or str
        try:
            ret = int(rand)
            isInt = True
        except ValueError:
            isInt = False
        #   if number is receieved server will sleep
        if isInt == True:
            print("number receieved is % s " % rand)
            #   sleep function invoked

            #-----------


            # for queue module referred to : https://docs.python.org/2/library/queue.html
            # for event referred to : https://docs.python.org/2.0/lib/event-objects.html

            event = threading.Event()
            #  put event object associated with current thread in queue.
            q.put(event)
            #  wait() call will halt the current thread indefinitely for event  to be set,
            #  which will wake up this current thread from the wait() and then go on do the task.
            event.wait() # referred to : http://blog.acipo.com/python-threading-events/

            event.clear()

            time.sleep(float(rand))
            event.set()


            #-----------

            global message
            message = "server has slept for " + rand + " seconds"
            print(_gen_headers(message))

            #   send msg back to client
            conn.send(str(message))
        else :
            # if not number send the str
            print ("connected to ", rand)
            conn.send("Hello % s " % rand)
            print_message_in_client = "connected by " + rand
            text += "\n{}".format(str(print_message_in_client))
            label.config(text=text)
        if not received_from_client:
            #   close the connection
            conn.close()
            break

def btn_exit():
    os._exit(0)

def gui_for_client():
    global root
    #   contractor is created to open the blank GUI
    root = Tk()
    #   setting the GUI dimensions
    root.geometry("400x700")
    # quit button created to close the GUI
    quit_button = Button(root, text = "quit", command = btn_exit)
    global label
    label = Label(root, text="")
    quit_button.pack()
    label.pack()
    global mainthread
    mainthread = threading.Thread(target=server).start()
    root.mainloop()




def _gen_headers(message):
    global http_message
    http_message = ''

    http_message = 'HTTP/1.1 200 OK\n'
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    http_message += 'Date: ' + current_date + '\n'
    http_message += 'Content-Type: text/xml; charset="utf-8"\n'
    http_message += 'host: 127.0.0.1:6542\n'
    http_message += 'User-Agent: Socket-Client\n'
    http_message += "\r\n" + str(message)

    return http_message


def coordinator():
    while True:
        e = q.get(block=True)
        e.set()
        time.sleep(0.2)
        e.wait()
        time.sleep(0.2)



def server():
    #   socket created
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #   bind the IP and the port
    sock.bind(('127.0.0.1', 5432))
    #   listen to incoming client
    sock.listen(3)
    print ('Server listening....')
    while True:
        #   accept the client
        conn, addr = sock.accept()
        #   create new thread to run perform_server_operation seperatly
        thread.start_new_thread(perform_server_operation, (conn, addr))


threading.Thread(target=coordinator).start() # start co-ordinator thread

gui_for_client()



