from Crypto.Cipher import AES
import time
import os

class Messager(object):
    def __init__(self, name, file_name, key):
        self.name = name
        self.file_name = file_name
        self.key = key

        
    def enc(self, plaintext):        
        nonce = os.urandom(8)  
        self.aes = AES.new(self.key, AES.MODE_CTR, nonce=nonce) 
        plaintext = plaintext.encode('utf-8')
        return self.aes.encrypt(plaintext), nonce
    
    def dec(self, ciphertext, nonce):
        decrypt_cipher = AES.new(self.key, AES.MODE_CTR, nonce=nonce)
        return decrypt_cipher.decrypt(ciphertext).decode('utf-8')
    
    def send_message(self, message):
        ciphertext, nonce = self.enc(message)
        with open(self.file_name, "a") as file:
            file.write(f"{self.name}|{nonce.hex()}|{ciphertext.hex()}\n")
            
    async def read_message(self):
        iteration = 0
        while True:
            try:
                with open(self.file_name, "r") as file:
                    lines = file.readlines()
                    
                formattedLine = lines[-1].replace("\n", "")
                if self.name not in formattedLine and "-key:" not in formattedLine:
                    name, nonce_str, ciphertext_str = formattedLine.split("|")
                    nonce = bytes.fromhex(nonce_str)
                    ciphertext = bytes.fromhex(ciphertext_str)
                    dec = self.dec(ciphertext, nonce) 
                    return name + ":" + dec       
            except:
                pass
            time.sleep(10)
            iteration+=1