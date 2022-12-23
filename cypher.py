import ctypes


def cypher(message: str, key: int) -> str:
    key_sec = [(key & (0xFF << i * 8)) >> i * 8 for i in range(3, -1, -1)]
    result = ""
    for i in range(len(message)):
        result += chr(ord(message[i]) ^ key_sec[i % len(key_sec)])
    return result


# Процесс генерации S-блока


s = [0x9fa12b, 0x39f8ee, 0x1d48fc, 0x6aa8bc, 0x4c2ff1, 0x309ff1, 0x9bcd3e, 0xe9ff37]
t = [0x000000] * 257
k = [0x5c4a56, 0x595857, 0x4e5558, 0x5f4e4e]
s[0] = k[0]
s[1] = k[1]
s[2] = k[2]
s[3] = k[3]

for n in range(4, 256):
    x = ctypes.c_uint32(t[n - 4] + t[n - 1]).value
    t[n] = x >> 3 ^ s[x & 7]

for n in range(0, 23):
    t[n] = ctypes.c_uint32(t[n] + t[n + 89]).value

x = t[33]
z = t[59] | 0x01000001
z &= 0xff7fffff
x = (x & 0xff7fffff) + z

for n in range(0, 256):
    x = ctypes.c_uint32((x & 0xff7fffff) + z).value
    t[n] = (t[n] & 0x00ffffff) ^ x

t[256] = t[0]
x &= 0xff

for n in range(0, 256):
    x = (t[n ^ x] ^ x) & 0xff
    t[n] = t[x]
    t[x] = t[n + 1]


# Процесс автогенерации ключа

r3 = [0, 0]
r4 = [0, 0]
r5 = [0, 0]
r6 = [0, 0]
r3[0] = k[0]
r4[0] = k[1]
r5[0] = k[2]
r6[0] = k[3]
r3[1] = ((r3[0] + r6[0]) >> 8) ^ (t[(r3[0] + r6[0]) & 0xff])
r4[1] = ((r4[0] + r3[1]) >> 8) ^ (t[(r4[0] + r3[1]) & 0xff])
r5[1] = ((r5[0] + r4[1]) >> 8) ^ (t[(r5[0] + r4[1]) & 0xff])
r6[1] = ((r6[0] + r5[1]) >> 8) ^ (t[(r6[0] + r5[1]) & 0xff])

key = r6[1]
