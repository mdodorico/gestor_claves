import random
import string
import hashlib
import secrets
from storage.db_manager import *

def generate_password():
    length = random.randint(13, 15)
    
    upper = random.choices(string.ascii_uppercase, k=random.randint(2, 4)) 
    digits = random.choices(string.digits, k=random.randint(2, 3))  
    special = random.choices(string.punctuation, k=random.randint(2, 3))  
    all_characters = upper + digits + special 
    
    while len(all_characters) < length:
        all_characters.append(random.choice(string.ascii_lowercase + string.digits + string.punctuation))
    
    random.shuffle(all_characters) 
    password = ''.join(all_characters)
    
    return password

def password_to_hash(password):
    salt = secrets.token_bytes(16) # Salt de 16 bytes
    salt_hex = salt.hex()  # Convierto la salt a una cadena hexadecimal para almacenarla o verla
    hashed_password = hashlib.sha256(salt + password.encode('utf-8')).hexdigest()
    return salt_hex, hashed_password
  
def verify_password(stored_salt_hex, stored_hash_with_salt, input_password):
    stored_salt = bytes.fromhex(stored_salt_hex) # Convertir la salt almacenada (en hexadecimal) de nuevo a bytes
    input_password_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
    input_hash_with_salt = hashlib.sha256(stored_salt + input_password_hash.encode('utf-8')).hexdigest()
    if input_hash_with_salt == stored_hash_with_salt:
        return True  
    else:
        return False  