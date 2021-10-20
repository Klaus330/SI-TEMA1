import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    MODE_ECB = 'ecb'
    MODE_CFB = 'cfb'

    def __init__(self, key, IV, bufferSize): 
        self.bs = AES.block_size
        self.key = key
        self.iv = IV
        self.bufferSize = bufferSize

    def encrypt(self, raw, mode):
        if mode == self.MODE_ECB:
            return self.encryptECB(raw)
        if mode == self.MODE_CFB:
            encrypted = self.encryptCFB(raw)
            return encrypted

    def decrypt(self, encrypted, mode):
        if mode == self.MODE_ECB:
            return self.decryptECB(encrypted)
        if mode == self.MODE_CFB:
            return self.decryptCFB(encrypted)

    
    def encryptECB(self, rawData):
        
        blocks = [rawData[i:i+16] for i in range(0, len(rawData), 16)]
        blocks[-1] += ' ' * (16-len(blocks[-1])) # padding

        crypted_blocks = []
        cipher = AES.new(self.key, AES.MODE_ECB)
        print(blocks)
        
        for block in blocks:
            blockEncoded = block.encode()
            crypted_blocks.append(
                cipher.encrypt(blockEncoded)
            )
        
        return crypted_blocks


    def decryptECB(self, encryptedData):
        decryptedBlocks = []
        cipher = AES.new(self.key, AES.MODE_ECB)

        for block in encryptedData:
            decryptedBlocks.append(
                cipher.decrypt(block).decode()
            )
        return "".join(decryptedBlocks).strip()

    
    def padding(self, raw):
        return b" " * (self.bufferSize - len(raw))

    def unpad(something, plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

    def xor(something, var, key):
        return bytes(a ^ b for a, b in zip(var, key))

    def encryptCFB(self, plainText):
        blocks = [plainText[i:i+16] for i in range(0, len(plainText), 16)]
        blocks[-1] += ' ' * (16-len(blocks[-1])) # padding

        blocks = [block.encode('utf-8') for block in blocks]
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        cryptedIV = cipher.encrypt(self.iv)
        crypted_blocks = []

        tmpCrypted = self.xor(cryptedIV, blocks[0])
        crypted_blocks.append(tmpCrypted)
        for block in blocks[1:]:
            tmpCrypted = cipher.encrypt(tmpCrypted)
            tmpCrypted = self.xor(tmpCrypted, block)
            crypted_blocks.append(tmpCrypted)

        return crypted_blocks

    def decryptCFB(self, cryptedText):
        decryptedBlocks = []
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        cryptedIV = cipher.encrypt(self.iv)

        #decrypt first block
        tmpDecrypted = self.xor(cryptedIV, cryptedText[0])
        decryptedBlocks.append(tmpDecrypted.decode())
        lastCrypted = cryptedText[0]
        for cryptedBlock in cryptedText[1:]:
            reEncrypted = cipher.encrypt(lastCrypted)
            tmpDecrypted = self.xor(reEncrypted, cryptedBlock)
            lastCrypted = cryptedBlock
            decryptedBlocks.append(tmpDecrypted.decode())
        
        return "".join(decryptedBlocks).strip()