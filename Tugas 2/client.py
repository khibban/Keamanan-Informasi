import socket
import threading
from DES import encrypt_message, decrypt_message

SHARED_KEY = "AABB09182736CCDD"
def receive_messages(sock: socket.socket):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Disconnected from server.")
                break
            encrypted_hex = data.decode()
            decrypted_text = decrypt_message(encrypted_hex, SHARED_KEY)
            print(f"\n📩 Pesan diterima (terenkripsi): {encrypted_hex}")
            print(f"🔓 Didekripsi: {decrypted_text}\n> ", end="")
        except Exception as e:
            print("Connection error :" ,e)
            break

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)
    client_socket.connect(server_address)

    print(f"Connected to {server_address[0]}:{server_address[1]}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    try:
        while True:
            message = input()
            if message.lower() == '/quit':
                break
            encrypted = encrypt_message(message, SHARED_KEY)
            client_socket.sendall(encrypted.encode())
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    run_client()
