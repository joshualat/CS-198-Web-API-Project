import hashlib
import hmac
import os
import cPickle as pickle
from Crypto.Cipher import AES

# SKA (Symmetric Key Algorithm) Classes
# source: http://code.activestate.com/recipes/576980-authenticated-encryption-with-pycrypto/
# note: code has been modified to fit project conventions and requirements

class SKAError(Exception): 
    pass

class SKA(object):
    """
    Symmetric Key Algorithm class 

    Algorithms used:
    AES-CBC (encryption)
    HMAC-SHA256 (signing)

    """

    PICKLE_PAD = "pickle::"
    AES_BLOCK_SIZE = 16
    SIG_SIZE = hashlib.sha256().digest_size

    def __init__(self, key_string, key_size=192):
        self.keys = self.extract_keys(key_string, key_size)
        self.key_size = key_size

    @classmethod
    def generate_key(cls, key_size=192):
        key = os.urandom(key_size / 8 + cls.SIG_SIZE)
        return key.encode("base64").replace("\n", "")

    @classmethod
    def extract_keys(cls, key_string, key_size):
        key = key_string.decode("base64")
        assert len(key) == key_size / 8 + cls.SIG_SIZE, "Invalid Key"
        return key[:-cls.SIG_SIZE], key[-cls.SIG_SIZE:]

    def main_encrypt(self, data):
        """encrypt data with AES-CBC and sign it with HMAC-SHA256"""
        aes_key, hmac_key = self.keys
        pad = self.AES_BLOCK_SIZE - len(data) % self.AES_BLOCK_SIZE
        data = data + pad * chr(pad)
        iv_bytes = os.urandom(self.AES_BLOCK_SIZE)
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = iv_bytes + cypher.encrypt(data)
        sig = hmac.new(hmac_key, data, hashlib.sha256).digest()
        return data + sig

    def main_decrypt(self, data):
        """verify HMAC-SHA256 signature and decrypt data with AES-CBC"""
        aes_key, hmac_key = self.keys
        sig = data[-self.SIG_SIZE:]
        data = data[:-self.SIG_SIZE]
        if hmac.new(hmac_key, data, hashlib.sha256).digest() != sig:
            raise SKAError("Message Authentication Failed")
        iv_bytes = data[:self.AES_BLOCK_SIZE]
        data = data[self.AES_BLOCK_SIZE:]
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = cypher.decrypt(data)
        return data[:-ord(data[-1])]

    def encrypt(self, obj, pickler=pickle):
        """pickle and encrypt a python object"""
        return self.main_encrypt(self.PICKLE_PAD + pickler.dumps(obj))

    def decrypt(self, data, pickler=pickle):
        """decrypt and unpickle a python object"""
        data = self.main_decrypt(data)
        # simple integrity check to verify that we got meaningful data
        assert data.startswith(self.PICKLE_PAD), "Unexpected Header"
        return pickler.loads(data[len(self.PICKLE_PAD):])

if __name__ == "__main__":
    # example usage
    shared_key = SKA.generate_key()
    data = {"key1":"value1","key2":[1,2,3]}
    ska = SKA(shared_key)
    encrypted_message = ska.encrypt(data)
    print "Encrypted Message:"
    print encrypted_message.encode("base64")
    print "Decrypted Data:"
    print ska.decrypt(encrypted_message)
