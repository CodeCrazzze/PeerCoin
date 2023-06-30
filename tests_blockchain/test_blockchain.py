import unittest
from cryptography.hazmat.primitives.asymmetric import rsa


from blockchain.transaction import Transaction
from blockchain.blockchain import Blockchain
from wallet.wallet import Wallet


class TestTransaction(unittest.TestCase):
    def test_transaction_signature_verification(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        sender_wallet = Wallet()
        receiver_wallet = Wallet()

        amount = 10
        transaction = Transaction(sender_wallet.get_address(), receiver_wallet.get_address(), amount)
        transaction.sign_transaction(private_key)

        self.assertTrue(transaction.verify_transaction())
        self.assertFalse(transaction.verify_transaction(public_key))  # Wrong public key

    def test_wallet_address_generation(self):
        wallet = Wallet()
        address = wallet.get_address()

        self.assertIsInstance(address, str)
        self.assertEqual(len(address), 64)

    def test_create_transaction(self):
        blockchain = Blockchain()
        sender_wallet = Wallet()
        receiver_wallet = Wallet()

        amount = 10
        self.assertTrue(blockchain.create_transaction(sender_wallet.get_address(), receiver_wallet.get_address(), amount))
        self.assertFalse(blockchain.create_transaction(sender_wallet.get_address(), receiver_wallet.get_address(), -amount))
        self.assertFalse(blockchain.create_transaction(sender_wallet.get_address(), receiver_wallet.get_address(), 0))

    def test_mine_pending_transactions(self):
        blockchain = Blockchain()
        miner_wallet = Wallet()

        self.assertFalse(blockchain.mine_pending_transactions(miner_wallet.get_address()))  # No pending transactions

        sender_wallet = Wallet()
        receiver_wallet = Wallet()
        amount = 10
        blockchain.create_transaction(sender_wallet.get_address(), receiver_wallet.get_address(), amount)

        self.assertTrue(blockchain.mine_pending_transactions(miner_wallet.get_address()))  # Mine pending transactions

    def test_get_balance(self):
        blockchain = Blockchain()
        wallet = Wallet()

        initial_balance = blockchain.get_balance(wallet.get_address())

        sender_wallet = Wallet()
        receiver_wallet = Wallet()
        amount = 10
        blockchain.create_transaction(sender_wallet.get_address(), receiver_wallet.get_address(), amount)

        final_balance = blockchain.get_balance(wallet.get_address())

        self.assertEqual(final_balance, initial_balance - amount)


def start():
    unittest.main()

if __name__ == "__main__":
    start()