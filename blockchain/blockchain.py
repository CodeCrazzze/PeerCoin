import datetime
import copy
import pickle

from blockchain.transaction import Transaction
from blockchain.block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(datetime.datetime.now(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner):
        if len(self.pending_transactions) == 0:
            return False  # Защита от майнинга пустых блоков

        block = Block(datetime.datetime.now(), copy.deepcopy(self.pending_transactions), self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        print("Block mined successfully!")
        self.chain.append(block)
        self.pending_transactions = []
        self.pending_transactions.append(Transaction(None, miner, self.mining_reward))
        return True

    def create_transaction(self, sender_wallet, receiver_address, amount):
        # Проверка наличия достаточного баланса у отправителя
        if self.get_balance(sender_wallet.get_address()) < amount:
            print("Insufficient balance. Transaction discarded.")
            return False
        transaction = Transaction(sender_wallet.get_address(), receiver_address, amount)
        transaction.sign_transaction(sender_wallet.private_key)
        if not transaction.verify_transaction():
            print("Invalid transaction signature. Transaction discarded.")
            return False
        self.pending_transactions.append(transaction)
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance


def save_blockchain(blockchain, filename):
    with open(filename, 'wb') as file:
        pickle.dump(blockchain, file)


def load_blockchain(filename):
    with open(filename, 'rb') as file:
        blockchain = pickle.load(file)
    return blockchain
