from cryptography.fernet import Fernet

def write_key(key_name):
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open(key_name, "wb") as key_file:
        key_file.write(key)

def load_key(key_name):
    """
    Loads the key from the current directory named `key.key`
    """
    return open(key_name, "rb").read()

def encrypt_file(key_name, file_name):
    key = load_key(key_name)
    f = Fernet(key)
    with open(file_name, "rb") as file:
        # read all file data
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(key_name, file_name):
    key = load_key(key_name)
    f = Fernet(key)
    with open(file_name, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data
    # write the original file
    #with open(file_name, "wb") as file:
        #file.write(decrypted_data)

def set_pw(key_name, pw_klar):
    key = load_key(key_name)
    f = Fernet(key)
    encrypted = f.encrypt(pw_klar)
    return(encrypted)

def get_pw(key_name, pw_crypt):
    key = load_key(key_name)
    f = Fernet(key)
    decrypted_encrypted = f.decrypt(pw_crypt)
    return decrypted_encrypted