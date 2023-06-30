import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class Wallet:
    def __init__(self):
        self.private_key, self.public_key = self.generate_key_pair()

    def generate_key_pair(self):
        # Генерация пары приватного и публичного ключей
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Сериализация ключей в PEM формат
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem.decode('utf-8'), public_pem.decode('utf-8')

    def get_address(self):
        # Получение адреса кошелька на основе публичного ключа
        return hashlib.sha256(self.public_key.encode('utf-8')).hexdigest()
