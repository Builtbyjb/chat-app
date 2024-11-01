import socket
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from database import Database
from werkzeug.security import check_password_hash, generate_password_hash

# Connect to Database
db = Database("clients.db")

# Creates the user socket object.
user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creates login window object
login_window = tk.Tk()

FT = "utf-8"
WSIZE = "615x570"

# Coloscheme
BACKGROUND = "#4A4A4A"
BTN_BG = "#BFC2C6"
BTN_FG = "#BFC2C6"


def main():
    run_login_window()


# Creates login window
def run_login_window():
    login_window.title("Chat-room")
    login_window.geometry(WSIZE)
    login_window.resizable(False, False)
    login_window.config(background=BACKGROUND)

    # Create two tabs on the login Windows
    notebook = ttk.Notebook(login_window)
    login_tab = tk.Frame(notebook, bg=BACKGROUND)
    register_tab = tk.Frame(notebook, bg=BACKGROUND)
    notebook.add(login_tab, text="Login")
    notebook.add(register_tab, text="Don't have an account? Register")
    notebook.pack(expand=True, fill="both")

    # Create login form
    l_username = tk.Entry(login_tab)
    l_username.insert(0, "USERNAME")
    l_username.pack(pady=15)

    def clear_l_username(event):
        l_username.delete(0, "end")

    l_username.bind("<Button-1>", clear_l_username)

    l_password = tk.Entry(login_tab, show="*")
    l_password.insert(0, "PASSWORD")
    l_password.pack()

    def clear_l_password(event):
        l_password.delete(0, "end")

    l_password.bind("<Button-1>", clear_l_password)

    l_btn = tk.Button(login_tab,
                      bg=BTN_BG,
                      text="Login",
                      command=lambda: user_verification(l_username.get(),
                                                        l_password.get()))
    l_btn.pack(pady=15)

    # Create Register form
    r_username = tk.Entry(register_tab)
    r_username.insert(0, "USERNAME")
    r_username.pack(pady=15)

    def clear_r_username(event):
        r_username.delete(0, "end")

    r_username.bind("<Button-1>", clear_r_username)

    r_password = tk.Entry(register_tab, show="*")
    r_password.insert(0, "PASSWORD")
    r_password.pack()

    def clear_r_password(event):
        r_password.delete(0, "end")

    r_password.bind("<Button-1>", clear_r_password)

    r_password2 = tk.Entry(register_tab, show="*")
    r_password2.insert(0, "PASSWORD")
    r_password2.pack(pady=15)

    def clear_r_password2(event):
        r_password2.delete(0, "end")

    r_password2.bind("<Button-1>", clear_r_password2)

    r_btn = tk.Button(register_tab,
                      bg=BTN_BG,
                      text="Register",
                      command=lambda: register_user(r_password.get(),
                                                    r_password2.get(),
                                                    r_username.get()))
    r_btn.pack()

    login_window.mainloop()


# Handles registering of users
def register_user(password1, password2, username):
    # Returns a list of all the current users.
    users = [u[0]for u in db.get_users()]

    if (password1 == password2):
        pwhash = generate_password_hash(password1,
                                        method='pbkdf2:sha256', salt_length=8)
        if username.lower() not in users:
            db.add_user(username.lower(), pwhash)
            run_app_window(username)
            users.clear()
        else:
            messagebox.showwarning(title="WARNING",
                                   message="USERNAME ALREADY EXISTS")
    else:
        raise ValueError("PASSWORDS DO NOT MATCH")
        messagebox.showwarning(title="WARNING",
                               message="PASSWORDS DO NOT MATCH")


# Verifies the user login information
def user_verification(username, password):
    # Returns a list of all users using list comprehension
    users = [u[0]for u in db.get_users()]

    if username.lower() in users:
        pwhash = db.get_user_pwhash(username.lower())[0][1]

        if check_password_hash(pwhash, password):
            run_app_window(username)
            users.clear()
        else:
            messagebox.showwarning(title="WARNING",
                                   message="INCORRECT PASSWORD")
    else:
        raise ValueError("USERNAME DOES NOT EXIST")
        messagebox.showwarning(title="WARNING",
                               message="USERNAME DOES NOT EXIST")


# Creates the main app windwow
def run_app_window(username):
    # Destroys the login Window
    login_window.destroy()

    # Creates app window object
    app_window = tk.Tk()
    app_window.title("Chat-room")
    app_window.geometry(WSIZE)
    app_window.config(bg=BACKGROUND)

    # Create Menu bar
    menubar = tk.Menu(app_window)
    app_window.config(menu=menubar)

    account_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Settings", menu=account_menu)
    account_menu.add_command(label="Delete Account",
                             command=lambda: delete_account(username.lower(),
                                                            app_window))

    # Create top bar
    top_bar = tk.Frame(app_window, bg=BACKGROUND, width=600, height=50)
    top_bar.pack()

    # Create user display
    user_display = tk.Label(top_bar,
                            text=username,
                            font=("bold", 15),
                            bg=BACKGROUND,
                            fg=BTN_FG)
    user_display.grid(row=0, column=0, padx=5)

    # Create Host IP address input
    host_ip_input = tk.Entry(top_bar)
    host_ip_input.grid(row=0, column=2)
    host_ip_input.insert(0, "HOST")

    def clear_host(event):
        host_ip_input.delete(0, "end")

    host_ip_input.bind("<Button-1>", clear_host)

    # Create port input
    port_input = tk.Entry(top_bar, width=10)
    port_input.grid(row=0, column=3, padx=10)
    port_input.insert(0, "PORT")

    def clear_port(event):
        port_input.delete(0, "end")

    port_input.bind("<Button-1>", clear_port)

    # Create Connect Button
    connect_btn = tk.Button(top_bar,
                            bg=BTN_BG,
                            text="Connect to: ",
                            command=lambda: connect_now(host_ip_input.get(),
                                                        port_input.get(),
                                                        connect_btn,
                                                        username))
    connect_btn.grid(row=0, column=1, pady=10, padx=10)

    # Create account settings
    disconnect_btn = tk.Button(top_bar,
                               bg=BTN_BG,
                               text="EXIT",
                               command=lambda: exit_now(app_window))
    disconnect_btn.grid(row=0, column=4, padx=3)

    # Create Chat area
    chat_area = tk.Frame(app_window, bg=BACKGROUND, width=600, height=450)
    chat_area.pack()

    # Create Chat Box
    chat_box = scrolledtext.ScrolledText(chat_area, height=26, width=71)
    chat_box.grid(row=0, column=1)
    chat_box.config(state="disabled")

    # Create input text area
    text_area = tk.Frame(app_window, bg=BACKGROUND, width=600, height=100)
    text_area.pack()

    text_input = scrolledtext.ScrolledText(text_area, width=40, height=1)
    text_input.grid(row=0, column=0, pady=10, padx=10)

    send_btn = tk.Button(text_area,
                         bg=BTN_BG,
                         text="Send",
                         command=lambda: send_msg(text_input.get("1.0", 'end-1c'),
                                                  text_input))
    send_btn.grid(row=0, column=1, padx=5)

    # Creates a daemon thread
    # that handles the recieving of data from the server
    threading.Thread(target=recieve_msg, daemon=True, args=(chat_box,)).start()

    app_window.mainloop()


def connect_now(host, port, connect_btn, username):
    # Connects to the server
    try:
        user_socket.connect((host, int(port)))
        user_socket.setblocking(False)
        user_socket.send(username.encode(FT))
        connect_btn.config(state="disabled")
    except Exception:
        raise ValueError("Connection Error!")
        messagebox.showerror(title="Error!",
                             message="Connection Error!")


def exit_now(app_window):
    user_socket.shutdown(socket.SHUT_RDWR)
    user_socket.close()
    app_window.destroy()


# Handles the sending of messages from the user
def send_msg(text, text_input):
    try:
        user_socket.send(text.encode(FT))
    except Exception:
        messagebox.showerror(title="Error!",
                             message="Sending Failed!")

    text_input.delete("1.0", "end")


# Handles recieving of data from the server
def recieve_msg(chat_box):
    while True:
        try:
            # Recieves message from the server
            message = user_socket.recv(1024).decode(FT)
            if message:
                add_msg(message, chat_box)
            else:
                pass
        except Exception:
            pass


# Handles adding of messages to the chat box
def add_msg(message, chat_box):
    chat_box.config(state="normal")
    chat_box.insert("end", message + "\n")
    chat_box.config(state="disabled")


def delete_account(username, app_window):
    db.delete_user(username)
    app_window.destroy()


if __name__ == "__main__":
    main()
