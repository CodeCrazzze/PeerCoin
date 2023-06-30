import datetime
import copy
from blockchain.blockchain import Blockchain, save_blockchain
from wallet.wallet import Wallet
from blockchain.block import Block
from blockchain.transaction import Transaction


def main():
    blockchain = Blockchain()
    wallet = Wallet()

    while True:
        print("\n===== Menu =====")
        print("1. Create Transaction")
        print("2. Mine Pending Transactions")
        print("3. Check Balance")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            receiver = input("Enter receiver's address: ")
            amount = float(input("Enter amount: "))
            if blockchain.create_transaction(wallet, receiver, amount):
                print("Transaction created successfully!")
            else:
                print("Failed to create transaction.")
        elif choice == '2':
            miner_address = input("Enter miner's address: ")
            if blockchain.mine_pending_transactions(miner_address):
                print("Pending transactions mined successfully!")
            else:
                print("No pending transactions to mine.")
        elif choice == '3':
            address = wallet.get_address()
            balance = blockchain.get_balance(address)
            print(f"Balance for address {address}: {balance}")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    save_blockchain(blockchain, 'blockchain.dat')


if __name__ == '__main__':
    main()
