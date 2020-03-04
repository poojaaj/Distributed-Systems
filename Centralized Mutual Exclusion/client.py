import socket
from Tkinter import *
import random
import thread
import time

text = ""


# function to create socket and start the program
def receive_message_from_server():
    global client_socket
    #   socket created
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #   client connected to server via below IP and port number
    client_socket.connect(('127.0.0.1', 5432))
    #   new thread created to handle the socket function seperatly
    thread.start_new_thread(perform_socket_operation, ())
    #   GUI function is called on the main thread
    gui_for_client()


def gui_for_client():
    global root
    #   contractor is created to open the blank GUI
    root = Tk()
    #   setting the GUI dimensions
    root.geometry("400x700")
    global input_text_variable
    input_text_variable = StringVar()
    # input text box created to accept input data
    input_text = Entry(root, textvariable=input_text_variable)
    #   submit button created
    submit_button = Button(root, text="submit", command=function_for_button)
    # quit button created to close the GUI
    quit_button = Button(root, text="quit", command=root.quit)
    global label
    label = Label(root, text="")
    input_text.pack()
    submit_button.pack()
    quit_button.pack()
    label.pack()

    root.mainloop()


def perform_socket_operation():
    global text
    while True:
        try:
            #   sending data to server
            data_from_server = client_socket.recv(2048)
            print('Received ', str(data_from_server))
            http_msg = genheaders(data_from_server)
            print(http_msg)
            text += "\n{}".format(str(data_from_server))

            # ----------------


            if 'server has slept' in http_msg:
                end = time.time()
                time_waited_for = int(end-start)
                text += "\nClient waited for " + str(time_waited_for) + " seconds."

            label.config(text=text)
            #    calling the random function to generate a random number
            random_function()
            start = time.time()

            
            #  ---------------------
        except:
            print('exc')
            text += "\n{}".format('Server disconnected unexpectedly.')
            label.config(text=text)
            break
    return


def genheaders(message):
    global http_message
    http_message = ''
    http_message = 'POST / HTTP/1.1\n'
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    http_message += 'Date: ' + current_date + '\n'
    http_message += 'Content-Type: text/xml; charset="utf-8"\n'
    http_message += 'host: 127.0.0.1:6542\n'
    http_message += 'User-Agent: Socket-Client\n'
    http_message += "\r\n" + str(message)

    return http_message


#   function for the button created in the GUI
def function_for_button():
    #   takes input fro the textbox on the GUI
    ntext = input_text_variable.get()
    label = Label(root, text=ntext)
    label.pack()
    #   sends the input text to server
    client_socket.send(str(genheaders(ntext)))
    return


def random_function():
    #   generates a random number
    rand = random.randint(5, 15)
    print ("random number generated", rand)
    #   random number is sent to the server
    client_socket.send(genheaders(rand))
    return


#   main function
if __name__ == '__main__':
    print("Waiting for connection...")
    #    main thread starts here
    receive_message_from_server()

#   to excute from terminal type python client.py
