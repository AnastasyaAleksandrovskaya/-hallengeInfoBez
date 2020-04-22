# Imports
import random
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# Given
p = 37
g = 5

a = random.randint(1, p-1) % p
A = pow(g, a, p)
b = random.randint(1, p-1) % p
B = pow(g, b, p)

def send(from_, to, send):
    print(from_ ," send ", send, " to ", to)

#A->M
send('A', 'M', [p, g, A])#Отправить "p", "g", "A"
#M->B
send('M', 'B', [p, g, p])#Отправить "p", "g", "p"
#B->M
send('B', 'M', B)#Отправить "B"
#M->A
send('M', 'A', p)#Отправить "p"
sA=pow(p, a, p) #B подменили p
#A->M
#Отправить AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
s_a = hashlib.sha1(str(sA).encode()).digest()[:16]
iv = Random.new().read(AES.block_size)
cipher = AES.new(s_a, AES.MODE_CBC, iv)
msg = iv + cipher.encrypt(b'Attack at dawn!!')
send('A', 'M', msg)
#M->B
#Перенаправить это сообщение B
msg_a = cipher.decrypt(msg)[-16:]
print("Расшифровка сообщения = ", msg_a)
send('M', 'B', msg)
sB=pow(p, b, p)
#B->M
#Отправить AES-CBC(SHA1(s)[0:16], iv=random(16), A’s msg) + iv
s_b = hashlib.sha1(str(sB).encode()).digest()[:16]
iv = Random.new().read(AES.block_size)
cipher = AES.new(s_b, AES.MODE_CBC, iv)
msg = iv + cipher.encrypt(msg_a)
send('B', 'M', msg)
#M->A
send('M', 'A', msg)#Перенаправить это сообщение
