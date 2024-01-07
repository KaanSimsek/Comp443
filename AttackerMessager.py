from Crypto.Cipher import AES
import time
import os

class AttackerMessager(object):
    def __init__(self, alice_file, bob_file, alice_key, bob_key):
        self.alice_file = alice_file
        self.bob_file = bob_file
        self.alice_key = alice_key
        self.bob_key = bob_key

        
    def enc(self, plaintext, key):        
        nonce = os.urandom(8)  
        self.aes = AES.new(key, AES.MODE_CTR, nonce=nonce) 
        plaintext = plaintext.encode('utf-8')
        return self.aes.encrypt(plaintext), nonce
    
    def dec(self, ciphertext, nonce, key):
        decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        return decrypt_cipher.decrypt(ciphertext).decode('utf-8')
    
    def send_message_to_alice(self, message):
        ciphertext, nonce = self.enc(message, self.alice_key)
        with open(self.alice_file, "a") as file:
            file.write(f"Bob|{nonce.hex()}|{ciphertext.hex()}\n")
    
    def send_message_to_bob(self, message):
        ciphertext, nonce = self.enc(message, self.bob_key)
        with open(self.bob_file, "a") as file:
            file.write(f"Alice|{nonce.hex()}|{ciphertext.hex()}\n")
            
    async def read_alice_message(self):
        iteration = 0
        while True:
            try:
                with open(self.alice_file, "r") as file:
                    lines = file.readlines()
                    
                formattedLine = lines[-1].replace("\n", "")
                if "Alice" in formattedLine and "-key:" not in formattedLine:
                    name, nonce_str, ciphertext_str = formattedLine.split("|")
                    nonce = bytes.fromhex(nonce_str)
                    ciphertext = bytes.fromhex(ciphertext_str)
                    dec = self.dec(ciphertext, nonce, self.alice_key) 
                    return name + ":" + dec
            except Exception as e:
                print(f"An error occurred: {e}")
            time.sleep(10)
            iteration+=1
    
    async def read_bob_message(self):
        iteration = 0
        while True:
            try:
                with open(self.bob_file, "r") as file:
                    lines = file.readlines()
                    
                formattedLine = lines[-1].replace("\n", "")
                if "Alice" not in formattedLine and "-key:" not in formattedLine:
                    name, nonce_str, ciphertext_str = formattedLine.split("|")
                    nonce = bytes.fromhex(nonce_str)
                    ciphertext = bytes.fromhex(ciphertext_str)
                    dec = self.dec(ciphertext, nonce, self.bob_key) 
                    return name + ":" + dec       
            except:
                pass
            time.sleep(10)
            iteration+=1