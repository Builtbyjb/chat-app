# A TCP Chat-room
#### Video Demo: https://youtu.be/G_tWUui5zMk
#### Description: 

My CS50P final project is a chat-room that allows users  connected to the same server send message back and forth, It uses a TCP socket and an IPV4
address. The Graphical User Interface (GUI) was designed using a python module called tkinker. My project features two main windows, a window that 
handles the login and registration of new users, and a main window that displays the the chat box where all the out going and incoming messages are
displayed for the currently connected users to see, it also contains a text input wigdet that allows users to send messages.

My project has 7 files in total, they include:
    1) project.py
    2) test_project.py
    3) clients.db
    4) database.py
    5) server.py
    6) requirement.txt 
    7) README.md

##### Project Files.

1) **project.py**: This is the main file of the my project, it runs Graphical User Interface,and Interacts with the database, to register new users 
and verify user login. It contains 5 imports a main function, and 10 other functions that are within the main functon but not nested in the main 
function i.e they are on the same indentation level as the main function, with a few constants defined above the main function.

**Imports:**
+ socket: This is a built-in python module that helps create an instance of a socket object. It allows the user to send data to the server and recieve
 data from the server.

+ threading: A thread in programming is a separate flow of execution, threading allows different processes in your program to run simultaneously, 
it prevents tasks from waiting on each other before they execute. Threading is used in my project tovallow the user socket to keep listen for messages 
from the server while being able to send messages to the server.

+ tkinker: Tkinter helps to create Graphical User Inferfaces, it was used to create the login and register window and the main window, from tkinker 
i imported tk which is used to create the window objects; scrolledtext which is used to create a text box with a scroll feature; messagebox which 
is used to send alerts, warnings, information as pop up windows when a action is performed and ttk used to create separate tabs on the same window,
it was used in the creation of the login and register window.

+ database: Provides acess to a the Database class, the class has a list of methods that performs the database operations needed to store the user
information and provide the informations when needed.

+ werkzeug.security: Provides methods like check_password_hash to confirm the hashpassword stored in the database is the same as the password the user 
provided to login, it returns true if it is and false if not; and generate_passward_hash to hash the password the user provided during registration, 
so that the users plain password is not stored in the database. The link to their usage documentation is;
![url](https://werkzeug.palletsprojects.com/en/2.2.x/utils/).

**Constants**
+ user_socket: defines a socket object, using AF_INET (IPV4) and SOCK_STREAM (TCP).
    
+ login_window: creates a tk object which is used in the creation of the login window.
    
+ FT = defines the encoding and decoding format used when sending data to server and recieving data from the server; the encode format used is this 
project is "UTF-8".
    
+ WSIZE = defines the default window size used in the login window and the main window, the defualt size is"615x570".
    
**Functions**
+ main: calls the run_login_window function, which starts the entire app.
    
+ run_login_window: Creates and run the login window, the login window contains two tabs, one to login the user another to register user. The regsiter
tab contains a username entry wigdet and two password entry wigdet, one password wigdet confirms the password, the regsiter button gets the input and
sends them to a "regsiter_users" function. The login user tab contains two entry wigdets and a button, the button sends the input gotten from the entry
boxs to a "users_verification" function.

+ register_user: This function gets the user input from the register tab entry wigdets, and checks if the passwords match, and if the username 
the user provide already exist, if the registration condition are met the "register_user" function converts the user passord into a hash, stores 
the user information in a database and calls the "run_app_window" function, if the conditions are not met the "regsiter_user" function raises a
"ValueError" and displays a pop up window informing the user that their registration information was not accepted.

+ user_verification: This function handles the verification of the user login information, it accepts a username and password as arguments. 
It checks if the username the user provides exist in the database , and confirms the user password by getting the hash password stored in the 
database with the one the user provide using the "check_password_hash" function gotten from "werkzeug". If the login condition are met the
"run_app_window" function is called, if the login condition is not met, it raises a "ValueError" and displays a pop up window telling the user that
their login information is not correct.
    
+ run_app_window: This function creates and run the main app window. The main app window is divided into 4 sections; a menu bar that contains a 
settings drop down menu, that as the option to delete the user account, the delete account button removes the user registration information from 
the database and exits the app; a top frame that displays the username of the user, a "connect to" button, two entry wigdets and an "EXIT" button,
the two entry wigdets takes in a HOST IP address and PORT, the HOST IP address and PORT is the same HOST IP address and PORT the server is binded to,
the "connect to" button then makes the connection, the "EXIT" button closes the connection and the application; a middle frame which is largest of 
the 4,it displays  the messages sent to the server and the messages recieved from the server; a bottom frame that contains an entry wigdet and 
a "Send" button, the "Send button" gets the input in entry wigdet, sends it to the server, before it is than recieved from the server and displayed
in the chat area.

+ connect_now: This function handles the connection to the server, it recieves a username, host ip address, port, and a variable that stores the 
"Connect to" button reference. It connects to the server using the host ip address and port, sends the username to server, so server can identify 
who is sending the messages, and disables the "connect to" button if the connection is successful, else it raises a "ValueError" and displays a 
pop up nessage the tells the user there was a "Connection error".

+ exit_now: This function is called when the "EXIT" button in the main app window is clicked, it takes the main app window reference as agruments. 
It shutsdown and closes the user socket connection and exits the application.

+ seng_msg: This function handles the sending of messages to the server, it takes the text the user provided in the text input entry wigdet and 
the a reference to the text input entry wigdet as agruments. It encodes the user input, send it to the server, if there was an issue sending the 
message it displays a pop up message telling the user "Sending Failed". It also clears the text input entry wigdet if the send was successful or not.
    
+ recieve_msg: This function handles the recieving of messages from the server. It is runs on a different thread, the thread starts when the 
"run_app_window" function is called and it keeps listen for messages from the server, when a message is recieved it calls the "add_msg" function and 
pass in the message recieved as an argument, if there is no message it keeps running untill the application closes.

+ add_msg: This function handles the adding of messages recieved from the server to the chat area.

+ delete_account: This function is called when the user clicks on the settings menu and selects the delete account option. It takes the username 
and a reference to "app_window" object as agruments, it removes the user information from the database and exits the application.

2) **test_project.py**: This file tests the "user_verification", "regsiter_user", and "connect_now" functions. The test are done using pytest.
It contains 3 functions which include:

+ test_register_user: Tests that the "regsiter_use"r function raises a "ValueError" if the passwords the user provided during registration are not
the same. 

+ test_user_verification: Tests that "the user_verification" function raises a "ValueError" if the information the user provided during login is not
in the database. 

+ test_connect_now: Tests that the "connect_now" function raises a "ValueError" if the user provides an invalid HOST IP address and PORT.

3) **Clients.db**: This is an sqlite3 database with a clients table that stores the users username and a hash of the user password.

4) **database.py**: This contains a class called Database that holds a list of functions that performs sqlite3 operations. It imports sqlite3 The
functions in Database class include: 

+ __init__: Connects to the database, and creates a cursor object that executes sqlite3 commands, it also creates a table in the database,
if the table does not exist before.

+ get_users: This functions takes no agruments, it gets a list of all the users in the database and returns it.

+ add_users: This functions takes two agruments apart from self, a username and a hash password. It add the username and hashpassword to the database.

+ get_user_pwhash: This functions takes a username as an agrument. It gets the hashpassword from the database and returns it.

+ delete_user: This function takes a username as an agrument. It removes the user information from the database.

+ __del__: This closes the connection to the database.

5) **server.py**: This file handles the creation of a server, It contains a socket object using AF_INET (IPV4) and SOCK_STREAM (TCP). It contains 
a "main" function, a "start" function, a handle_recieve function and a broadcast function.

+ The main function checks if the command line agruments provided by the user mets the required condition and then pass the values to the "start" 
function and then calls the "start" function, the command line arguments gotten are 
    1) A HOST IP address.
    2) A PORT.

+ The start function, takes two arguments a HOST IP address and a PORT. It binds the values to the server and starts listening for connection. 
If a connection is requested it accepts the connection and start a thread that keeps listening for messages from the new connection.

+ The handle_recieve function, it takes the user socket as agrument, and handles the recieving of messages from the connection and sends them 
to the other connections on the server. It also alerts the connected users that a user as disconnected.

+ The broadcast function, takes the recieved messages a arguments, it handles the sending of messages to all the connected users, it is called 
by the handle_recieve function when it gets a message from a user.

6) **requirement.txt**: Stores a list of all imported modules used in the project.
