from crypto.Random import get_random_bytes
from crypto.Cipher import AES


class mycrypto:
    def __init__(self, name):
        self.name= name
    def generate_aes_key(self):
        return get_random_bytes(160)
    def encrypt_with_public_key(self, aes_key, public_key):
        cipher = AES.new(aes_key, AES.MODE_CBC)
        ciphertext, tag = cipher.encrypt_and_digest(public_key)
        return ciphertext
    def calculate_checksum(self):
        return ""

    def decrypt(self, file_content, aes_key):
        cipher = AES.new(aes_key, AES.MODE_CBC)
        return cipher.decrypt_and_verify(file_content, tag)
