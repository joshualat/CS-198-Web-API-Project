import hmac
import hashlib
import cPickle as pickle
from Crypto.PublicKey import RSA
from Crypto import Random

# PKA (Public-Key Algorithm) Classes

class PKAError(Exception):
    pass

class PKA(object):
    """
    Public-Key Algorithm class

    Algorithms used:
    RSA (encryption)
    HMAC-SHA256 (signing)

    """

    PICKLE_PAD = "pickle::"
    SIG_SIZE = hashlib.sha256().digest_size

    @classmethod
    def encrypt(cls,public_key,message,pickler=pickle):
        """pickle and encrypt a python object"""
        message = cls.PICKLE_PAD + pickler.dumps(message)
        rsa = RSA.importKey(public_key)
        encrypted_message = rsa.publickey().encrypt(message,'')
        sig = hmac.new(public_key, encrypted_message[0], hashlib.sha256).digest()
        output = (encrypted_message[0],sig)
        output = cls.PICKLE_PAD + pickler.dumps(output)
        return output

    @classmethod
    def decrypt(cls,private_key,message,pickler=pickle):
        """decrypt and unpickle a python object"""
        message = pickler.loads(str(message[len(cls.PICKLE_PAD):]))
        sig = message[1]
        hmac_message = message[0]
        message = (message[0],)
        rsa = RSA.importKey(private_key)
        public_key = rsa.publickey().exportKey()
        if hmac.new(public_key, hmac_message, hashlib.sha256).digest() != sig:
            raise PKAError("Message Authentication Failed")
        decrypted_message = rsa.decrypt(message)
        decrypted_message = pickler.loads(decrypted_message[len(cls.PICKLE_PAD):])
        return decrypted_message

    @classmethod
    def decrypt_or_none(cls,private_key,message):
        try:
            return cls.decrypt(private_key,message)
        except PKAError:
            return None
        except Exception:
            return None

    @classmethod
    def sign(cls,private_key,message,pickler=pickle):
        message = cls.PICKLE_PAD + pickler.dumps(message)
        rsa = RSA.importKey(private_key)
        hashed_message = hashlib.sha256(message).digest()
        signature = rsa.sign(hashed_message,'')
        return str(signature[0])

    @classmethod
    def verify(cls,public_key,message,signature,pickler=pickle):
        message = cls.PICKLE_PAD + pickler.dumps(message)        
        hashed_message = hashlib.sha256(message).digest()
        rsa = RSA.importKey(public_key)
        return rsa.verify(hashed_message,(long(signature),))

    @classmethod
    def generate_keys(cls,key_size=2048):
        """generate private and public keys"""
        random_generator = Random.new().read
        key = RSA.generate(key_size, random_generator)
        return (key.exportKey(),key.publickey().exportKey())

if __name__ == "__main__":
    # example usage
    priv_key, pub_key = PKA.generate_keys()
    data = {"key1":"value1","key2":[1,2,3]}
    encrypted_message = PKA.encrypt(pub_key,data)
    decrypted_message = PKA.decrypt(priv_key,encrypted_message)
    signature = PKA.sign(priv_key,encrypted_message)
    verified = PKA.verify(pub_key,encrypted_message,signature)
    print "\n"+"-"*50+"\n"

    print "Private Key:"
    print priv_key

    print "\n"+"-"*50+"\n"

    print "Public Key:"
    print pub_key

    print "\n"+"-"*50+"\n"

    print "Encrypted Message:"
    print encrypted_message

    print "\n"+"-"*50+"\n"

    print "Decrypted Data:"
    print decrypted_message

    print "\n"+"-"*50+"\n"

    print "Signature:"
    print signature

    print "Verified:"
    print verified
