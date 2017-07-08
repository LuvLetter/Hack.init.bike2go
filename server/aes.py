'''
Created on Mar 20, 2014, uses PyCrypto/Python 3.3
@author: Chris Coe
'''
#cited from https://gist.github.com/chrcoe/9667052
import binascii
from Crypto.Cipher import AES

class AESCipher:
    '''
    PyCrypto AES using ECB mode implementation in Python 3.3.  
    This uses very basic 0x00 padding, I would recommend PKCS5/7.
    '''

    def __init__(self, key):
        '''
        The constructor takes in a PLAINTEXT string as the key and converts it
        to a byte string to work with throughout the class.
        '''
        # convert key to a plaintext byte string to work with it
        self.key = bytes(key, encoding='utf-8')
        self.BLOCK_SIZE = 16
        
    def __pad(self, raw):
        '''
        This right pads the raw text with 0x00 to force the text to be a
        multiple of 16.  This is how the CFX_ENCRYPT_AES tag does the padding.
        
        @param raw: String of clear text to pad
        @return: byte string of clear text with padding
        '''
        if (len(raw) % self.BLOCK_SIZE == 0):
            return raw
        padding_required = self.BLOCK_SIZE - (len(raw) % self.BLOCK_SIZE)
        padChar = b'\x00'
        data = raw.encode('utf-8') + padding_required * padChar
        return data
    
    def __unpad(self, s):
        '''
        This strips all of the 0x00 from the string passed in. 
        
        @param s: the byte string to unpad
        @return: unpadded byte string
        '''
        s = s.rstrip(b'\x00')
        return s
    
    def encrypt(self, raw):
        '''
        Takes in a string of clear text and encrypts it.
        
        @param raw: a string of clear text
        @return: a string of encrypted ciphertext
        '''
        if (raw is None) or (len(raw) == 0):
            raise ValueError('input text cannot be null or empty set')
        # padding put on before sent for encryption
        raw = self.__pad(raw)
        cipher = AES.AESCipher(self.key[:32], AES.MODE_ECB)
        ciphertext = cipher.encrypt(raw)
        return  binascii.hexlify(bytearray(ciphertext)).decode('utf-8')
    
    def decrypt(self, enc):
        '''
        Takes in a string of ciphertext and decrypts it.
        
        @param enc: encrypted string of ciphertext
        @return: decrypted string of clear text
        '''
        if (enc is None) or (len(enc) == 0):
            raise ValueError('input text cannot be null or empty set')
        enc = binascii.unhexlify(enc)
        cipher = AES.AESCipher(self.key[:32], AES.MODE_ECB)
        enc = self.__unpad(cipher.decrypt(enc))
        return enc.decode('utf-8')
s = ""
for item in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f]:
    s += chr(item)
# print(s)
cipher = AESCipher(s)
encrypted = cipher.encrypt('asdfasdfasdfasdf')
decrypted = cipher.decrypt(encrypted)
print(encrypted.lower())
print(decrypted)