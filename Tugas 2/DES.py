

def hex2bin(s):
    """Konversi Hex ke Biner"""
    mp = {
        '0': "0000", '1': "0001", '2': "0010", '3': "0011",
        '4': "0100", '5': "0101", '6': "0110", '7': "0111",
        '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
        'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"
    }
    bin_str = ""
    for i in range(len(s)):
        bin_str += mp[s[i]]
    return bin_str


def bin2hex(s):
    """Konversi Biner ke Hex"""
    mp = {
        "0000": '0', "0001": '1', "0010": '2', "0011": '3',
        "0100": '4', "0101": '5', "0110": '6', "0111": '7',
        "1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
        "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'
    }
    hex_str = ""
    for i in range(0, len(s), 4):
        ch = s[i:i+4]
        hex_str += mp[ch]
    return hex_str


def bin2dec(binary):
    """Konversi Biner ke Desimal"""
    decimal, i = 0, 0
    while binary != 0:
        dec = binary % 10
        decimal += dec * pow(2, i)
        binary //= 10
        i += 1
    return decimal


def dec2bin(num):
    """Konversi Desimal ke Biner"""
    res = bin(num).replace("0b", "")
    while len(res) % 4 != 0:
        res = '0' + res
    return res


def permute(k, arr, n):
    """Permutasi bit sesuai tabel"""
    return "".join([k[i - 1] for i in arr[:n]])


def shift_left(k, nth_shifts):
    """Geser bit ke kiri sebanyak nth_shifts"""
    return k[nth_shifts:] + k[:nth_shifts]


def xor(a, b):
    """XOR dua string biner"""
    return "".join(['0' if a[i] == b[i] else '1' for i in range(len(a))])


initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]

per = [16, 7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2, 8, 24, 14,
       32, 27, 3, 9,
       19, 13, 30, 6,
       22, 11, 4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25]


#  Fungsi Enkripsi DES
def encrypt(pt, rkb, rk):
    pt = hex2bin(pt)

    # Initial Permutation
    pt = permute(pt, initial_perm, 64)
    print("🔸 Setelah Initial Permutation:", bin2hex(pt))

    left = pt[0:32]
    right = pt[32:64]

    # Proses 16 ronde Feistel
    for i in range(16):
        right_expanded = permute(right, exp_d, 48)
        xor_x = xor(right_expanded, rkb[i])

        #  Proses S-Box 
        sbox_str = ""
        for j in range(8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(int(xor_x[j * 6 + 1:j * 6 + 5]))
            val = sbox[j][row][col]
            sbox_str += dec2bin(val)

        # Permutasi P-box
        sbox_str = permute(sbox_str, per, 32)

        # XOR dengan sisi kiri
        result = xor(left, sbox_str)
        left = result

        # Tukar posisi kecuali di ronde terakhir
        if i != 15:
            left, right = right, left

        print(f"Round {i+1}: L={bin2hex(left)} | R={bin2hex(right)} | K={rk[i]}")

    # Gabungkan kiri dan kanan
    combine = left + right

    # Final Permutation
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text

# Tambahan fungsi untuk enkripsi dan dekripsi singkat (tanpa print proses)
def generate_keys(key_hex):
    """Generate 16 round keys dari key hex."""
    key = hex2bin(key_hex)
    keyp = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    key = permute(key, keyp, 56)
    shift_table = [1, 1, 2, 2, 2, 2, 2, 2,
                   1, 2, 2, 2, 2, 2, 2, 1]
    key_comp = [14, 17, 11, 24, 1, 5,
                3, 28, 15, 6, 21, 10,
                23, 19, 12, 4, 26, 8,
                16, 7, 27, 20, 13, 2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32]
    left, right = key[0:28], key[28:56]
    rkb = []
    rk = []
    for i in range(16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        combine_str = left + right
        round_key = permute(combine_str, key_comp, 48)
        rkb.append(round_key)
        rk.append(bin2hex(round_key))
    return rkb, rk


def encrypt_message(plaintext, key_hex):
    """Encrypt plaintext ASCII menjadi HEX ciphertext."""
    # Ubah plaintext jadi hex (maks 8 karakter = 64 bit)
    pt_hex = plaintext.encode().hex().upper().ljust(16, '0')[:16]
    rkb, rk = generate_keys(key_hex)
    cipher_bin = encrypt(pt_hex, rkb, rk)
    return bin2hex(cipher_bin)


def decrypt_message(ciphertext_hex, key_hex):
    """Decrypt ciphertext HEX jadi plaintext ASCII."""
    rkb, rk = generate_keys(key_hex)
    rkb = rkb[::-1]
    rk = rk[::-1]
    plain_bin = encrypt(ciphertext_hex, rkb, rk)
    plain_hex = bin2hex(plain_bin)
    try:
        return bytes.fromhex(plain_hex).decode().strip('\x00')
    except:
        return "[DECRYPT_ERROR]"


if __name__ == "__main__":
    pt = "123456DBCA132536"
    key = "AABB09182736CCDD"

    #  Key Generation 
    key = hex2bin(key)
    keyp = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    key = permute(key, keyp, 56)

    shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    key_comp = [14, 17, 11, 24, 1, 5,
                3, 28, 15, 6, 21, 10,
                23, 19, 12, 4, 26, 8,
                16, 7, 27, 20, 13, 2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32]

    left, right = key[0:28], key[28:56]
    rkb, rk = [], []

    for i in range(16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])
        combine_str = left + right
        round_key = permute(combine_str, key_comp, 48)
        rkb.append(round_key)
        rk.append(bin2hex(round_key))

    #  Enkripsi 
    print("\n ENKRIPSI")
    cipher_text = bin2hex(encrypt(pt, rkb, rk))
    print("\n Cipher Text:", cipher_text)

    #  Dekripsi 
    print("\n DEKRIPSI")
    rkb_rev = rkb[::-1]
    rk_rev = rk[::-1]
    text = bin2hex(encrypt(cipher_text, rkb_rev, rk_rev))
    print(" Plain Text :", text)
