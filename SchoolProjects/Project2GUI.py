# This coding example is greatly influenced and inspired by an online example written by Saurabh Chaturvedi #
# URL: https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import random


# Two scripts, one for the server, one for the client #
# Server #

# Constants
client_list = {}
address_list = {}
HOST = ""
PORT = 33000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

# Tasks:
    # Accept New Connections
    # Broadcast Messages
    # Handling Clients

# Server Code #
# new_connection continuously waits for new connections
# Once a new connection is received, it logs the connection and stores the client's address in address_list
def new_connection():
    # This sets up the handling for new clients trying to connect
    while True:
        client, client_address = SERVER.accept()
        print(client + " has connected")
        client.send(bytes("What it do, my dude (or dudett)" + "\n What be your name?", "enc5"))
        address_list[client] = client_address
        Thread(target=client_handling, args=(client,)).start()


# Takes the client name (socket) as an argument
# The client picks their username
def client_handling(client):
    # This hanldes the single client we pass it
    name = client.recv(BUFSIZE).decode("enc5")
    # Give the client some basic instructions
    message = "Hello " + client + "! \n" + "To enter a message, simply type a message and hit enter. \n" \
              + "Or, to quit, simply type {goodbye}."
    client.send(bytes(message, "enc5"))
    client_msg = client + " has joined the server!"
    msg_broadcast(bytes(client_msg, "enc5"))
    # Save the client's name, and append a random number to the end, so as to give the client a unique name
    # This is a simple way to ensure there's no duplicate names
    while True:
        name_addon = random.randint(1, 1000)
        # Append the unique number identifier to the user's name
        name = name + str(name_addon)
        if name in client_list:
            print("Name taken, assigning new name addon")
        else:
            client_list[client] = name
            break

    # Continuously take messages from the client, until they wish to quit
    while True:
        client_msg = client.recv(BUFSIZE)
        if client_msg != bytes("{goodbye}", "enc5"):
            msg_broadcast(client_msg, name + ": ")
        else:
            # Close the connection socket for the client
            client.send(bytes("{goodbye}", "enc5"))
            client.close()
            # Remove the client's name from the list of clients
            del client_list[client]
            msg_broadcast(bytes(client + " has left the chat, thankfully. No one liked them. ", "enc5"))
            break


# Sends the msg to all connected clients
# Prefix is used for the name
def msg_broadcast(msg, prefix=""):
    # This displays the message from one client to all clients
    for sock in client_list:
        sock.send(bytes(prefix, "enc5") + msg)

# Starting the server
if __name__ == "__main__":
    SERVER.listen(3)  # 3 max connections
    print("Awaiting connection...")
    ACCEPT_THREAD = Thread(target=new_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()  # Used so the code doesn't jump to the next line
    SERVER.close()


# Client Code #
def msg_receive():
    # An infinite loop for taking in messages from clients
    while True:
        # A try/except statement for if the client has left the server
        try:
            # recv() stops execution until a message is received
            msg = client_socket.recv(BUFSIZE).decode("enc5")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


# Event is implicitly passed by tkinter when the send button is pressed
def msg_send(event=None):
    msg = my_msg.get()  # my_msg is the input field on the GUI, this line extracts the contents of the field
    my_msg.set("")  # Clear the input field
    client_socket.send(bytes(msg, "enc5"))  # Send the previously taken input
    if msg == "{goodbye}":  # If the input field is the exit message, then we disconnect the user
        client_socket.close()
        top.quit()


# This is called when the GUI window is closed
def gui_closing(event=None):
    my_msg.set("{goodbye}")
    msg_send()


# GUI Code #
# Top level widgets for the GUI and the frame name
top = tkinter.Tk()
top.title("CPSC 4550 Group 1 Chat Room")

# Frame for holding the messages
message_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # This holds the message that will be sent taken from the input field
my_msg.set("Type here...")
scrollbar = tkinter.Scrollbar(message_frame)
# Create the message list and place the certain frame components (widgets) where we want them
msg_list = tkinter.Listbox(message_frame, height=10, width=35, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

message_frame.pack()

user_text = tkinter.Entry(top, textvariable=my_msg)  # Input field for user, bound to my_msg string variable
user_text.bind("<Return>", msg_send)  # Bind the return (enter) button to send the user's message when pressed
user_text.pack()
send_button = tkinter.Button(top, text="Send", command=msg_send)  # Send button so user can click it to send message
send_button.pack()

top.protocol("WM_DELETE_WINDOW", gui_closing)

# Connecting to the server code #
# Get the server's address from the user
# We can add a GUI for this for convenience sake
HOST = input("Please enter the host address: ")
PORT = input("Please enter the port number: ")
if not PORT:
    PORT = 33000  # A default value
else:
    PORT = int(PORT)

BUFSIZE = 1024
ADDRESS = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDRESS)

# After receiving the address and we make a socket, we start the thread for receiving messages and start up the GUI
receive_thread = Thread(target=msg_receive)
receive_thread.start()
tkinter.mainloop()  # starts the GUI