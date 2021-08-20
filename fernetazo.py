import os
import base64
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from rich.prompt import Prompt
from rich.console import Console

parser = argparse.ArgumentParser()
parser.add_argument('--encrypt', '-e', help="Encrypt a messsage with your password.", action="store_true", default=False)
parser.add_argument('--decrypt', '-d', help="Decrpyt a message with your password.", action="store_true", default=False)
args = parser.parse_args()
no_arguments = 'You need to define one argument (encrypt/decrypt). For further information add -h'

# Check arguments
if args.encrypt == False and args.decrypt == False:
    raise Exception(no_arguments)

# User Password
user_pass = Prompt.ask('Password', password=True)
pass_b = user_pass.encode('utf-8')

#Salt could be randomly generated, but should be stored to use the same in the future.
#random_salt = os.urandom(16)

#Salt stored as ENV var as string (keep a backup!!)
salt_env = os.getenv('FERNETAZO_SALT')
salt = salt_env.encode('utf-8')

# Prepare Fernetazo
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend(),
)
key = base64.urlsafe_b64encode(kdf.derive(pass_b))
fernetazo = Fernet(key)


def encrypt_message(message: str):
    message_b = message.encode('utf-8')
    token = fernetazo.encrypt(message_b)
    return token.decode('utf-8')


def decrypt_token(token: str):
    try:
        token_b = token.encode('utf-8')
        message_b = fernetazo.decrypt(token_b)
        return message_b.decode('utf-8')
    except:
        print('Decryption failed. Double check your password and token!')
        raise


if __name__ == "__main__":

    ## ENCRYPTING
    if args.encrypt:
        with open('encrypt.txt', 'r') as file:
            data = file.read()
        token = encrypt_message(data)
        print("Token generated: "+str(token))
        
    ## DECRYPTING
    elif args.decrypt:
        token = Prompt.ask('Token')
        message = decrypt_token(token)
        with open('decrypt.txt', 'w') as file:
            file.write(message)