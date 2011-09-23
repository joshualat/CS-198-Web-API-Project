import uuid
import hashlib
import cPickle as pickle
from Crypto.Random import random

# SecTools (Security Tools) Class

class SecTools(object):

    """
    SecTools class 

    Usable functions:
        generate_salt
        generate_uuid
        generate_hash
        verify_hash
        random_int
        random_choice
        random_float
        serialize
        deserialize

    """

    @classmethod
    def generate_salt(cls,length=16):
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return ''.join(cls.random_choice(ALPHABET) for i in range(length))

    @classmethod
    def generate_uuid(cls):
        return str(uuid.uuid1())

    @classmethod
    def generate_hash(cls,obj,salt=None):
        obj = cls.serialize(obj)
        if salt != None:
            obj = obj + salt
        return hashlib.sha256(obj).digest()

    @classmethod
    def verify_hash(cls,sig,obj,salt=None):
        return sig == cls.generate_hash(obj,salt)

    @classmethod
    def random_int(cls,a,b):
        return random.randint(a,b)

    @classmethod
    def random_choice(cls,seq):
        return random.choice(seq)

    @classmethod
    def random_float(cls):
        rand_int = random.randint(0,9999999999)
        return float(rand_int)/float(10000000000)

    @classmethod
    def serialize(cls,obj):
        return pickle.dumps(obj)

    @classmethod
    def deserialize(cls,obj):
        return pickle.loads(obj)
