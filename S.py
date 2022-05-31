import socket, os, traceback
class WebServer():
    def __init__(self, ip, port, max_clients=None):
        self.ip = ip
        self.port = port
        self.max_clients = max_clients
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.html = []
        if self.max_clients == None:
            self.server.listen()
        else:
            self.server.listen(max_clients)
    def listen(self):
        conn, addr = self.server.accept()
        data = conn.recv(1024).decode()
        print(addr, data)
        try: 
            for i, l in enumerate(data.split("\n")):
                if i == 0:
                    requestType = l.split(" ")[0]
                    #TODO multiple request types check
                    if requestType != "GET":
                        conn.send(b"HTTP/1.1 400 Bad Request\n")
                    else:   
                        requestPath = l.split(" ")[1]
                        if ".." in requestPath:
                            print("Hack attempt from",addr)
                            conn.send(b"HTTP/1.1 404 Not Found\n")
                        elif os.path.exists("."+requestPath):
                            for h in self.html:
                                if(h.path == "."+requestPath):
                                    f = open("."+requestPath, "r")
                                    toSend = f.read().encode("UTF-8")
                                    f.close()
                                    conn.send(b"HTTP/1.1 200 OK\n"
                                    +b'Content-Type: text/html\n'
                                    +b"\n"
                                    +bytes(toSend))
                        else:
                            conn.send(b"HTTP/1.1 404 Not Found\n")
            conn.close()
        except Exception as e: 
            conn.close()
            traceback.print_exc()
    def addHtml(self, path):
        self.html.append(Html(path))
    def start(self):
        while True:
            self.listen()
class Html():
    def __init__(self, path):
        self.path = path
        try:
            self.file = open(self.path, "r").read()
        except Exception as e:
            print(e)
web = WebServer("0.0.0.0", 8080, None)
web.addHtml("./Folder/index.html")
web.start()
