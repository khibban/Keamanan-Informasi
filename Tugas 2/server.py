import socket
import select

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(2)
    print("Server ready on port 9999")

    clients = []
    while True:
        readable, _, _ = select.select([server] + clients, [], [])
        for s in readable:
            if s is server:
                client, addr = server.accept()
                clients.append(client)
                print(f"Client connected: {addr}")
            else:
                try:
                    data = s.recv(1024)
                    if not data:
                        clients.remove(s)
                        s.close()
                        continue
                    # relay ke client lain
                    for c in clients:
                        if c != s:
                            c.sendall(data)
                except:
                    clients.remove(s)
                    s.close()

if __name__ == "__main__":
    run_server()
