# name : Pooja Ashok Jeergyal
# Id : 100686373

# importing libraries
import socket
from Tkinter import *
import time
import threading
import Queue as q
import simpleeval as se

poll_requested = False

global clients
clients = []

global client_dict
client_dict = {}

qq = q.Queue()
client_count = 0

global eval_result
eval_result = ''

global eval_done
eval_done = False

global initial_value
initial_value = '1'
text = ""


def func_checker():
    global eval_done
    global initial_value
    global eval_result
    while True:
        if client_count > 0 and qq.qsize() == client_count:
            print('in while -> if')
            expr = initial_value
            while not qq.empty():
                expr = expr + qq.get()
            print ("before main eval", expr)
            eval_result = str(se.simple_eval(expr))
            initial_value = eval_result
            eval_done = True
    time.sleep(0.2)


def gui_for_server():
    global root
    #   contractor is created to open the blank GUI
    root = Tk()
    #   setting the GUI dimensions
    root.geometry("400x500")

    submit_button = Button(root, text="Poll", command=function_for_button)
    quit_button = Button(root, text="Quit", command=root.quit)
    submit_button.pack()
    quit_button.pack()

    # submit_button.grid(row=4)
    #
    # quit_button.grid(row=5)

    global label
    label = Label(root, text="")
    label.pack()
    root.mainloop()


def function_for_button():
    global poll_requested
    poll_requested = True
    global client_dict
    client_dict = {x: True for x in clients}
    print(client_dict)


def thread_for_client(conn, addr):

    print ("connected by", addr)
    global received_from_client
    received_from_client = conn.recv(2048)
    clients.append(received_from_client)
    print ("Hello %s" % received_from_client)
    print_message_in_client = "connected by " + received_from_client
    global text
    text += "\n{}".format(print_message_in_client)
    label.config(text=text)

    global eval_result
    global eval_done
    while True:
        global client_dict
        if received_from_client in client_dict.keys() and client_dict[received_from_client]:
            conn.send("poll_req")
            print('poll req sent')
            client_dict[received_from_client] = False
            eval_done = False
        data_from_client = conn.recv(2048)

        if '##' in data_from_client:
            conn.send('##')
        if 'upload' in data_from_client:
            print('Received: ', data_from_client)
            text += "\n{}".format(data_from_client)
            label.config(text=text)
            expression = data_from_client.replace('upload:', '')
            expression = expression.split('$$')[0]
            print(expression)


            qq.put(expression)
            while not eval_done:
                time.sleep(0.1)
            print(eval_result)
            text += "\n{}".format(eval_result)
            label.config(text=text)

            conn.send('server_value:' + eval_result)





def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 54321))
    server_socket.listen(3)
    print("server is listening")
    global client_count
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=thread_for_client, args=(conn, addr)).start()
        client_count = client_count + 1
        # conn.send(msg)


threading.Thread(target=func_checker).start()
threading.Thread(target=server).start()
gui_for_server()