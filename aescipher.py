import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key, IV, bufferSize): 
        self.bs = AES.block_size
        self.key = key
        self.iv = IV
        self.bufferSize = bufferSize


    def encrypt(self, raw, mode):
         mode = 'ecb'

         if mode == 'ecb':
             self.encryptECB(raw)
    

    def encryptECB(self, rawData):
        
        blocks = [rawData[i:i+16] for i in range(0, len(rawData), 16)]

        # padd the last array item to match the constraints
        blocks[-1] += ' ' * (16-len(blocks[-1]))

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

    # def encrypt(self, raw):
    #     raw = self._pad(raw)
    #     iv = Random.new().read(AES.block_size)
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    # def decrypt(self, enc):
    #     enc = base64.b64decode(enc)
    #     iv = enc[:AES.block_size]
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    # def _pad(self, s):
    #     return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    # @staticmethod
    # def _unpad(s):
    #     return s[:-ord(s[len(s)-1:])]