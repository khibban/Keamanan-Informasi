import socket
import threading
import json
import random
from DES import encrypt_message, decrypt_message
from RSA import generate_keypair, encrypt_des_key_with_rsa, decrypt_des_key_with_rsa

class SecureClient:
    def __init__(self):
        # Generate RSA keypair untuk client ini
        print(" Generating RSA keypair...")
        self.public_key, self.private_key = generate_keypair(bits=512)
        print(f" RSA keys generated\n")
        
        # Generate random DES key untuk sesi ini
        self.des_key = self.generate_des_key()
        print(f" Generated DES session key: {self.des_key}\n")
        
        # Simpan public key dan DES key dari peer
        self.peer_public_key = None
        self.peer_des_key = None  # DES key yang dikirim peer (untuk decrypt pesan dari peer)
        self.secure_channel_ready = False
        self.key_exchange_complete = False
        
    def generate_des_key(self):
        """Generate random 64-bit DES key dalam format hex"""
        key_int = random.getrandbits(64)
        return hex(key_int)[2:].upper().zfill(16)
    
    def receive_messages(self, sock):
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    print("\n Disconnected from server.")
                    break
                
                # Cek apakah ini public key dari peer
                try:
                    msg = json.loads(data.decode())
                    
                    if msg.get("type") == "public_key":
                        self.peer_public_key = (msg["e"], msg["n"])
                        print(" RECEIVED PEER'S RSA PUBLIC KEY")
                        print(f"   e (public exponent): {msg['e']}")
                        print(f"   n (modulus): {str(msg['n'])[:50]}...{str(msg['n'])[-20:]}")
                        print(f"   DES Key (plaintext): {self.des_key}")
                        
                        # Enkripsi DES key kita dengan public key peer
                        encrypted_des_key = encrypt_des_key_with_rsa(
                            self.des_key, 
                            self.peer_public_key
                        )
                        
                        print(f"   Encrypted (RSA): {str(encrypted_des_key)[:60]}...{str(encrypted_des_key)[-20:]}")
                        print(f"   RSA ENCRYPTION SUCCESSFUL!")
                        
                        # Kirim encrypted DES key
                        key_msg = json.dumps({
                            "type": "encrypted_des_key",
                            "key": str(encrypted_des_key)
                        })
                        sock.sendall((key_msg + "\n").encode())
                        print(f" Sent to peer\n")
                        
                        # Cek apakah key exchange sudah complete
                        if self.peer_des_key is not None:
                            self.secure_channel_ready = True
                            print(" Secure channel fully established!\n> ", end="", flush=True)
                        continue
                    
                    elif msg.get("type") == "encrypted_des_key":
                        # Terima encrypted DES key dari peer 
                        print(f"\n Received encrypted DES key from peer")
                        encrypted_key_int = int(msg["key"])
                        
                        # Decrypt dengan private key kita
                        peer_des_key = decrypt_des_key_with_rsa(
                            encrypted_key_int,
                            self.private_key
                        )
                        self.peer_des_key = peer_des_key
                        print(f" Decrypted peer's DES key: {peer_des_key}")
                        
                        # Cek apakah key exchange sudah complete
                        if self.peer_public_key is not None:
                            self.secure_channel_ready = True
                            print(" Secure channel fully established!\n> ", end="", flush=True)
                        continue
                    
                    elif msg.get("type") == "new_client":
                        print(f"\n👤 New client connected: {msg['addr']}")
                        print("> ", end="", flush=True)
                        continue
                        
                except json.JSONDecodeError:
                    pass
                
                # Pesan terenkripsi DES biasa
                encrypted_hex = data.decode().strip()
                
                if not self.peer_des_key:
                    print(f"\n  Received encrypted message but don't have peer's DES key yet")
                    print("> ", end="", flush=True)
                    continue
                
                # Decrypt dengan peer's DES key
                try:
                    decrypted_text = decrypt_message(encrypted_hex, self.peer_des_key)
                    print(f"\n Peer: {decrypted_text}")
                    print(f"   [Encrypted: {encrypted_hex[:32]}...]")
                    print("> ", end="", flush=True)
                except Exception as e:
                    print(f"\n  Decryption error: {e}")
                    print("> ", end="", flush=True)
                
            except Exception as e:
                print(f"\n  Connection error: {e}")
                break
    
    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 9999)
        
        print(f" Connecting to {server_address[0]}:{server_address[1]}...")
        client_socket.connect(server_address)
        print(f" Connected to server\n")
        
        # Kirim public key ke server
        print(" Broadcasting public key...")
        e, n = self.public_key
        public_key_msg = json.dumps({
            "type": "public_key",
            "e": e,
            "n": n
        })
        client_socket.sendall((public_key_msg + "\n").encode())
        print(" Public key sent\n")
        
        # Start thread untuk receive messages
        receive_thread = threading.Thread(
            target=self.receive_messages, 
            args=(client_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()
        
        print("   Waiting for key exchange to complete...")
        
        try:
            while True:
                message = input("> ")              
                if not message.strip():
                    continue
                
                if not self.secure_channel_ready:
                    print(" Secure channel not ready yet. Please wait for another client to connect.")
                    continue
                
                # Enkripsi dengan DES key kita sendiri
                encrypted = encrypt_message(message, self.des_key)
                client_socket.sendall((encrypted + "\n").encode())
                print(f"   [Sent encrypted: {encrypted[:32]}...]")
                
        except KeyboardInterrupt:
            print("\n Exiting...")
        finally:
            client_socket.close()
            print(" Connection closed.")

if __name__ == "__main__":
    print()
    client = SecureClient()
    client.run()