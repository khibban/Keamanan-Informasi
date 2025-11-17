# server.py
import socket
import select
import json

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Server ready on port 9999")

    clients = []
    client_public_keys = {} 
    
    while True:
        readable, _, _ = select.select([server] + clients, [], [])
        for s in readable:
            if s is server:
                client, addr = server.accept()
                clients.append(client)
                print(f"Client connected: {addr}")
                
                # Send existing public keys to the new client
                for existing_client, pub_key in client_public_keys.items():
                    if existing_client in clients:  
                        try:
                            pk_msg = json.dumps({
                                "type": "public_key",
                                "e": pub_key[0],
                                "n": pub_key[1]
                            })
                            client.sendall((pk_msg + "\n").encode())
                            print(f"Sent existing public key to new client {addr}")
                        except Exception as e:
                            print(f"Error sending existing key: {e}")
                
                # Notify other clients about new client
                for c in clients:
                    if c != client:
                        try:
                            notification = json.dumps({
                                "type": "new_client",
                                "addr": str(addr)
                            })
                            c.sendall((notification + "\n").encode())
                        except:
                            pass
            else:
                try:
                    data = s.recv(4096)
                    if not data:
                        # Client disconnected
                        addr = s.getpeername()
                        print(f"Client disconnected: {addr}")
                        clients.remove(s)
                        if s in client_public_keys:
                            del client_public_keys[s]
                        s.close()
                        continue
                    
                    # Check if this is public key exchange
                    try:
                        msg = json.loads(data.decode())
                        if msg.get("type") == "public_key":
                            # Store this client's public key
                            client_public_keys[s] = (msg["e"], msg["n"])
                            print(f"Stored public key from {s.getpeername()}")
                            
                            # Broadcast public key to all other clients
                            for c in clients:
                                if c != s:
                                    c.sendall(data)
                            continue
                    except json.JSONDecodeError:
                        pass
                    
                    # Relay encrypted messages to other clients
                    for c in clients:
                        if c != s:
                            c.sendall(data)
                            
                except Exception as e:
                    print(f"Error: {e}")
                    try:
                        clients.remove(s)
                        if s in client_public_keys:
                            del client_public_keys[s]
                        s.close()
                    except:
                        pass

if __name__ == "__main__":
    run_server()