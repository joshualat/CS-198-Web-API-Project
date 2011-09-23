import hashlib
import hmac
import os
import cPickle as pickle
from Crypto.Cipher import AES

# SKA (Symmetric Key Algorithm) Classes

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
    KEY_SIZE = 192

    @classmethod
    def generate_key(cls):
        key = os.urandom(cls.KEY_SIZE / 8 + cls.SIG_SIZE)
        return key.encode("base64").replace("\n", "")

    @classmethod
    def extract_keys(cls, key_string):
        key = key_string.decode("base64")
        assert len(key) == cls.KEY_SIZE / 8 + cls.SIG_SIZE, "Invalid Key"
        return key[:-cls.SIG_SIZE], key[-cls.SIG_SIZE:]

    @classmethod
    def main_encrypt(cls, shared_key, data):
        """encrypt data with AES-CBC and sign it with HMAC-SHA256"""
        aes_key, hmac_key = cls.extract_keys(shared_key)
        pad = cls.AES_BLOCK_SIZE - len(data) % cls.AES_BLOCK_SIZE
        data = data + pad * chr(pad)
        iv_bytes = os.urandom(cls.AES_BLOCK_SIZE)
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = iv_bytes + cypher.encrypt(data)
        sig = hmac.new(hmac_key, data, hashlib.sha256).digest()
        return data + sig

    @classmethod
    def main_decrypt(cls, shared_key, data):
        """verify HMAC-SHA256 signature and decrypt data with AES-CBC"""
        aes_key, hmac_key = cls.extract_keys(shared_key)
        sig = data[-cls.SIG_SIZE:]
        data = data[:-cls.SIG_SIZE]
        if hmac.new(hmac_key, data, hashlib.sha256).digest() != sig:
            raise SKAError("Message Authentication Failed")
        iv_bytes = data[:cls.AES_BLOCK_SIZE]
        data = data[cls.AES_BLOCK_SIZE:]
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = cypher.decrypt(data)
        return data[:-ord(data[-1])]

    @classmethod
    def encrypt(cls, shared_key, obj, pickler=pickle):
        """pickle and encrypt a python object"""
        return cls.main_encrypt(shared_key,cls.PICKLE_PAD + pickler.dumps(obj))

    @classmethod
    def decrypt(cls, shared_key, data, pickler=pickle):
        """decrypt and unpickle a python object"""
        data = cls.main_decrypt(shared_key, data)
        # simple integrity check to verify that we got meaningful data
        assert data.startswith(cls.PICKLE_PAD), "Unexpected Header"
        return pickler.loads(data[len(cls.PICKLE_PAD):])

    @classmethod
    def decrypt_or_none(cls, shared_key, data):
        try:
            return cls.decrypt(shared_key,data)
        except SKAError:
            return None
        except Exception:
            return None


if __name__ == "__main__":
    # example usage
    shared_key = SKA.generate_key()
    data = {"key1":"value1","key2":[1,2,3]}
    encrypted_message = SKA.encrypt(shared_key,data)
    decrypted_message = SKA.decrypt(shared_key,encrypted_message)
    print "Shared Key:"
    print shared_key
    print "Encrypted Message:"
    print encrypted_message.encode("base64")
    print "Decrypted Data:"
    print decrypted_message

