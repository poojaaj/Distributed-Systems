import socket
from Tkinter import *
import time
import threading

import simpleeval as se

# initial value is set at 1
initial_value = '1'

upload_exp = ''

global prev_expression
prev_expression = None

global connected
connected = False


text = ''


# function to create socket and start the program
def receive_message_from_server():
    global client_socket
    #   socket created
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #   client connected to server via below IP and port number
    client_socket.connect(('127.0.0.1', 54321))

    #   GUI function is called on the main thread
    gui_for_client()




def gui_for_client():
    global root
    #   contractor is created to open the blank GUI
    root = Tk()
    #   setting the GUI dimensions
    root.geometry("500x300")

    # this is a label to display "Name of the client:"
    name_label = Label(root, text="Name of the client:")
    name_label.pack()

    # this is a label to display "Name of the client:"
    value_label = Label(root, text="Value to be calculated:")
    value_label.pack()

    global name_of_client, exp_entered_by_user

    # this will provide a textbox to input name of the client
    name_of_client = StringVar()
    entry1 = Entry(root, textvariable=name_of_client)

    #on click of the button the client sends the name to the server
    send_name = Button(root, text="Send name", command=send_name_to_server)

    # this will provide a textbox to input expression
    exp_entered_by_user = StringVar()
    entry2 = Entry(root, textvariable=exp_entered_by_user)

    # on click of the button the expression calculated
    calculate_button = Button(root, text="Calculate", command=function_for_button)
    quit_button = Button(root, text="Quit", command=root.quit, width=20)

    # these will allign the labels
    name_label.grid(row=0)
    value_label.grid(row=1)
    send_name.grid(row=0, column=2)
    calculate_button.grid(row=1, column=2)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    quit_button.grid(row=4, column=1)

    # label created to append text to the GUI
    global label
    label = Label(root, text="")
    # label.pack()

    #thread created  to perform socket operation function
    threading.Thread(target=perform_socket_operation).start()
    root.mainloop()


#this function will send name to the server
def send_name_to_server():
    ntext = name_of_client.get()
    client_socket.send(str((ntext)))
    global connected
    connected = True
    return


# This is where the execution starts

def perform_socket_operation():
    global connected
    while not connected:
        pass

    while True:
        try:
            time.sleep(0.5)
            client_socket.send("##")
            #   sending data to server
            data_from_server = client_socket.recv(2048)

            print('Received ', str(data_from_server))

            # this is to keep connection alive and not end up in read dead lock.
            if '##' in data_from_server:
                data_from_server = data_from_server.replace("#", "")
            if 'poll_req' in data_from_server:
                client_socket.send('upload:' + upload_exp + '$$')
                global prev_expression
                prev_expression = ''
                print "in prev"
            elif 'server_value' in data_from_server:
                print "entered elseif"
                data = data_from_server.replace('server_value:', '')
                global initial_value
                initial_value = data
                global text
                text += "\n{}".format(str('Server Value: ' + initial_value))
                label.config(text=text)
        except Exception as e:
            print('exc: ', e)
            text += "\n{}".format('Server disconnected unexpectedly.')
            label.config(text=text)
            break
    return


# this function will check and resolve the expression

def function_for_button():
    global prev_expression
    exp_entered = exp_entered_by_user.get()
    if prev_expression == None:
        global local_copy
        local_copy = se.simple_eval(initial_value + ' ' + exp_entered)
        prev_expression = exp_entered
    else:
        local_copy = se.simple_eval(initial_value + ' ' + prev_expression + ' ' + exp_entered)
        prev_expression = prev_expression + ' ' + exp_entered

    global upload_exp
    upload_exp = prev_expression
    print(upload_exp)
    message_to_display_on_GUI = "\n Value for " + str(prev_expression) + " is :" + str(local_copy)
    label.config(text=message_to_display_on_GUI)
    label.pack(side="bottom")
    return


#   main function
if __name__ == '__main__':
    print("Waiting for connection...")
    #    main thread starts here
    receive_message_from_server()

#   to excute from terminal type python client.py
