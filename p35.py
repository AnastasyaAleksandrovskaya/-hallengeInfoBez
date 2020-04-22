# Imports
import os
import hashlib
from Crypto.Cipher import AES


def malicious_g_attack():
    p = DiffieHellman.DEFAULT_P
    return_vals = []
    for g in [1, p, p - 1]:
        alice = DiffieHellman()
        bob = DiffieHellman(g=g)
        A = alice.gen_public_key()
        B = bob.gen_public_key()
        _msg = b"Hello, how are you?"
        _a_key = hashlib.sha1(str(alice.gen_shared_secret_key(B)).encode()).digest()[:16]
        _a_iv = os.urandom(AES.block_size)
        a_question = AES_CBC_encrypt(_msg, _a_iv, _a_key) + _a_iv
        mitm_a_iv = a_question[-AES.block_size:]
        if g == 1:
            mitm_hacked_key = hashlib.sha1(b'1').digest()[:16]
            mitm_hacked_message = AES_CBC_decrypt(a_question[:-AES.block_size], mitm_a_iv, mitm_hacked_key)

        elif g == p:
            mitm_hacked_key = hashlib.sha1(b'0').digest()[:16]
            mitm_hacked_message = AES_CBC_decrypt(a_question[:-AES.block_size], mitm_a_iv, mitm_hacked_key)

        else:

            for candidate in [str(1).encode(), str(p - 1).encode()]:
                mitm_hacked_key = hashlib.sha1(candidate).digest()[:16]
                mitm_hacked_message = AES_CBC_decrypt(a_question[:-AES.block_size], mitm_a_iv, mitm_hacked_key)
                if PKCS7_padded(mitm_hacked_message):
                    mitm_hacked_message = PKCS7_unpad(mitm_hacked_message)
                    break
        print(mitm_hacked_message)

malicious_g_attack()