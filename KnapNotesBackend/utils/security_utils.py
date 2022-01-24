from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_512
from secrets import token_hex
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode

N_HASH = 300000
SALT_SIZE = 100
RSA_STRENGTH = 4096
KEY_FORMAT = "PEM"


# arg - string, string
# return - string
def get_hash(data, salt):
	salt = str.encode(salt)
	hasher = SHA3_512.new(str.encode(data) + salt, update_after_digest=True)
	for i in range(N_HASH):
		hasher.update(hasher.digest() + salt)
	return hasher.hexdigest()


# return - string
def create_salt():
	return token_hex(SALT_SIZE)


# string, string, string
def hash_and_validate_password(real_password, password, salt):
	password = get_hash(password, salt)
	return real_password == password


# returns str, str
def create_new_key_pair(passphrase):
	key_pair = RSA.generate(RSA_STRENGTH)
	private_key = key_pair.export_key(format=KEY_FORMAT, passphrase=passphrase).decode()
	public_key = key_pair.public_key().export_key(format=KEY_FORMAT).decode()
	return private_key, public_key


# params str, str
# returns str
def encrypt(public_key, message):
	message = message.encode()
	public_key = RSA.import_key(public_key.encode())
	cipher = PKCS1_OAEP.new(public_key)
	return b64encode(cipher.encrypt(message)).decode()


# all str
def decrypt(private_key, passphrase, message):
	message = b64decode(message.encode())
	private_key = RSA.import_key(private_key.encode(), passphrase=passphrase)
	cipher = PKCS1_OAEP.new(private_key)
	return cipher.decrypt(message).decode()
