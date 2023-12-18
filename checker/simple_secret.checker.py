import socket
import sys
import os.path

if __name__ == '__main__':
    regime = sys.argv[1]
    address = sys.argv[2]
    port = int(sys.argv[3])
    if regime == "check":
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        try:
            sock.connect((address, port))
        except socket.error as msg:
            print("Caught exception socket.error : %s" % msg)
            sys.exit(104) 
        if os.path.exists('log.txt'):
            data = sock.recv(1024)
            if data.decode("utf-8") != "Wellcome\n1.To register\n2.To login\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"2\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Login\nEnter login\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"checker\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Enter password\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"12345\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"1\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "flag\n":
                sock.close()
                sys.exit(102)
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"3\n")
            usersdata = ""
            data = ""
            while True:        
                data = sock.recv(1024)
                data = data.decode("utf-8")
                usersdata = usersdata + data
                if "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>" in data:
                    break
            fulldata = usersdata[:len(usersdata) - len("Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>")]
            users = fulldata.split("\n")
            while "" in users:
                users.remove("")
            if "checker" not in users:
                sock.close()
                sys.exit(103)
            sock.send(b"4\n")
            sock.close()
            sys.exit(101)
        else:
            open('log.txt', 'w').close()
            data = sock.recv(1024)
            if data.decode("utf-8") != "Wellcome\n1.To register\n2.To login\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"1\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Registration\nEnter login\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"checker\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Enter password\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"12345\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"1\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "No secret.\n":
                sock.close()
                sys.exit(103)
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"2\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Insert secret\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"flag\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"1\n")
            data = sock.recv(1024)
            if data.decode("utf-8") != "flag\n":
                sock.close()
                sys.exit(102)
            data = sock.recv(1024)
            if data.decode("utf-8") != "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>":
                sock.close()
                sys.exit(103)
            sock.send(b"3\n")
            usersdata = ""
            data = ""
            while True:        
                data = sock.recv(1024)
                data = data.decode("utf-8")
                usersdata = usersdata + data
                if "Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>" in data:
                    break
            fulldata = usersdata[:len(usersdata) - len("Commands.\n1.Show secret\n2.Store secret\n3.Show users\n4.Exit\n>")]
            users = fulldata.split("\n")
            while "" in users:
                users.remove("")
            if "checker" not in users:
                sock.close()
                sys.exit(103)
            sock.send(b"4\n")
            sock.close()
            sys.exit(101)
    else:
        sys.exit(110)
