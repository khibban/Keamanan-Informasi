# RSA.py
import random

def gcd(a, b):
    """Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """Extended Euclidean Algorithm untuk mencari modular inverse"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi

def is_prime(n, k=5):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=512):
    """Generate bilangan prima random dengan ukuran bits"""
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Set MSB dan LSB ke 1
        if is_prime(num):
            return num

def generate_keypair(bits=512):
    """Generate RSA keypair (public_key, private_key)"""
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    # Hitung n dan phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt_rsa(plaintext, public_key):
    """Encrypt plaintext menggunakan RSA public key"""
    e, n = public_key
    plaintext_int = int.from_bytes(plaintext.encode(), 'big')
    
    if plaintext_int >= n:
        raise ValueError("Plaintext terlalu panjang untuk key ini")
    
    ciphertext_int = pow(plaintext_int, e, n)
    return ciphertext_int

def decrypt_rsa(ciphertext_int, private_key):
    """Decrypt ciphertext menggunakan RSA private key"""
    d, n = private_key
    plaintext_int = pow(ciphertext_int, d, n)
    
    byte_length = (plaintext_int.bit_length() + 7) // 8
    plaintext = plaintext_int.to_bytes(byte_length, 'big').decode()
    return plaintext

def encrypt_des_key_with_rsa(des_key, public_key):
    """Encrypt DES key menggunakan RSA"""
    e, n = public_key
    key_int = int(des_key, 16)  
    encrypted = pow(key_int, e, n)
    return encrypted

def decrypt_des_key_with_rsa(encrypted_key_int, private_key):
    """Decrypt DES key menggunakan RSA"""
    d, n = private_key
    decrypted_int = pow(encrypted_key_int, d, n)
    des_key = hex(decrypted_int)[2:].upper().zfill(16)
    return des_key