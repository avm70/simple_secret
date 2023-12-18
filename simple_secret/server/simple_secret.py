import socket
import threading
import sqlite3
import sys

def on_new_client(clientsocket, addr):
    clientsocket.send(b"Wellcome\n1.To register\n2.To login\n>")
    while True:
        try:
            msg = clientsocket.recv(1024)
            if msg == b"1\n":
                client_registration(clientsocket)
            elif msg == b"2\n":
                client_login(clientsocket)
            else:
                clientsocket.send(b"Wrong command.\n1.To register\n2.To login\n>")
        except OSError:
            break

def client_registration(clientsocket):
    conn = sqlite3.connect('users_db')
    c = conn.cursor()
    while True:
        clientsocket.send(b"Registration\nEnter login\n>")
        msg = clientsocket.recv(1024)
        name = msg.decode("utf-8")
        name = name[:-1]
        c.execute("SELECT name FROM users WHERE name = ?", (name,))
        if c.fetchone() is None:
            clientsocket.send(b"Enter password\n>")
            msg = clientsocket.recv(1024)
            password = password = msg.decode("utf-8")
            password = password[:-1]
            while len(password) == 0:
                msg = clientsocket.recv(1024)
                password = msg.decode("utf-8")
                password = password[:-1]
                if len(password) == 0:
                    clientsocket.send(b"Password is empty.\nEnter password\n>")        
            c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
            conn.commit()
            conn.close()
            on_login(clientsocket, name)
        else:
            clientsocket.send(b"Username alredy exists\n")

def client_login(clientsocket):
    conn = sqlite3.connect('users_db')
    c = conn.cursor()
    while True:
        try:
            clientsocket.send(b"Login\nEnter login\n>")
            msg = clientsocket.recv(1024)
            name = msg.decode("utf-8")
            name = name[:-1]
            clientsocket.send(b"Enter password\n>")
            msg = clientsocket.recv(1024)
            password = msg.decode("utf-8")
            password = password[:-1]
            print(name, password)
            c.execute("SELECT * FROM users WHERE name = '%s' AND password = '%s'" % (name, password))
            data = c.fetchone()
            print(data)
            if data is None:
                clientsocket.send(b"Wrond data.\n")
                conn.close()
                on_new_client(clientsocket, "")
            else:
                conn.close()
                on_login(clientsocket, data[1])
        except OSError:
            break
        except sqlite3.OperationalError:
            clientsocket.send(b"Error.\n")
            break

def on_login(clientsocket, name):
    print("Client name: " + name + " log in")
    conn = sqlite3.connect('users_db')
    c = conn.cursor()
    while True:
        clientsocket.send(b"Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>")
        msg = clientsocket.recv(1024)
        if msg == b"1\n":
            try:
                c.execute("SELECT secret FROM users WHERE name = '%s'" % (name))
                data = c.fetchall()
                print(data)
                if data is None:
                    clientsocket.send(b"No secret.\n")
                else:
                    for secret in data:
                        clientsocket.send((secret[0] + "\n").encode())
            except TypeError:
                clientsocket.send(b"No secret.\n")
                print("Error")
        elif msg == b"2\n":
            clientsocket.send(b"Insert secret\n>")
            msg = clientsocket.recv(1024)
            secret = msg.decode("utf-8")
            secret = secret[:-1]
            c.execute("UPDATE users SET secret = (?) WHERE name = (?)", (secret, name))
            conn.commit()
        elif msg == b"3\n":
            c.execute("SELECT name FROM users")
            data = c.fetchall()
            for name in data:
                clientsocket.send((name[0] + "\n").encode())
        elif msg == b"4\n":
            conn.close()
            clientsocket.close()
            break
        else:
            clientsocket.send(b"Wrong command.\n")

if __name__ == '__main__':
    conn = sqlite3.connect('users_db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users ([user_id] integer PRIMARY KEY, [name] TEXT, [password] TEXT, [secret] TEXT)")
    conn.commit()
    conn.close()
    server_object = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    port = 3000
    server_object.bind(('', port))
    server_object.listen()

    while True:
        c, addr = server_object.accept()
        threading.Thread(target=on_new_client, args=(c, addr)).start()
