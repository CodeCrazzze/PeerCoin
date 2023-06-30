import hashlib
import datetime


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.datetime.now()
        self.signature = None

    def calculate_hash(self):
        data = str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def sign_transaction(self, private_key):
        data = self.calculate_hash()
        signature = private_key.sign(data.encode('utf-8'))  # Подпись транзакции с использованием приватного ключа
        self.signature = signature

    def verify_transaction(self):
        data = self.calculate_hash()
        return self.sender.verify(data.encode('utf-8'), self.signature)  # Проверка подписи транзакции с использованием публичного ключа отправителя
