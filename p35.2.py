# Imports
import random
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# Given
ACK = "I got a message"
p = 37
g = 5

def send(from_, to, send):
    print(from_ ," send ", send, " to ", to)


def attack(falseG):
    # A->B
    send('A', 'M', [p,g])# Отправить "p", "g"
    send('M','B',[p, falseG])

    # B->A
    send('B','M',ACK)# Отправить ACK
    send('M','A', ACK)

    # A->B
    a = random.randint(1, p - 1) % p
    A = pow(g, a, p)
    send('A', 'M', A)# Отправить "A"
    send('M', 'B', A)

    # B->A
    b = random.randint(1, p - 1) % p
    B = pow(falseG, b, p)
    send('B', 'M', B)# Отправить "B"
    send('M', 'A', B)

    # A->B
    # Отправить AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    sA = pow(B, a, p)
    s_a = hashlib.sha1(str(sA).encode()).digest()[:16]
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(s_a, AES.MODE_CBC, iv)
    msg = iv + cipher.encrypt(b'Attack at dawn!!')
    send('A', 'M', msg)
    msg_a = cipher.decrypt(msg)[-16:]
    print("decrypt msg (M know this) = ", msg_a)
    send('M', 'B', msg)

    # B->A
    # Отправить AES-CBC(SHA1(s)[0:16], iv=random(16), сообщение от A) + iv
    sB = pow(A, b, p)
    s_b = hashlib.sha1(str(sB).encode()).digest()[:16]
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(s_b, AES.MODE_CBC, iv)
    msg = iv + cipher.encrypt(msg_a)
    send('B', 'M', msg)
    send('M', 'A', msg)

print('g = 1  ')
attack(1)
print('g = p  ')
attack(p)
print('g = p-1  ')
attack(p-1)