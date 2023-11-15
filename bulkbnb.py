# BulkBNB (V1.1.0)
# Developed by Fahd El Haraka ©
# Email: fahd@web3dev.ma
# Telegram: @thisiswhosthis
# Website: https://web3dev.ma
# GitHub: https://github.com/ELHARAKA

import argparse
import threading
from queue import Queue
from web3 import Web3
from eth_account import Account
from tqdm import tqdm

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process private keys.')
parser.add_argument('--threads', type=int, default=1, help='Number of threads to use')
args = parser.parse_args()

# Number of threads
num_threads = args.threads

# Connect to Binance Smart Chain
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

if not web3.is_connected():
    raise Exception("Failed to connect to Binance Smart Chain")

destination_address = 'PASTE_YOUR_WALLET_ADDRESS_HERE'

def get_balance(private_key):
    account = Account.from_key(private_key)
    balance = web3.eth.get_balance(account.address)
    return web3.from_wei(balance, 'ether')

def send_bnb(private_key, amount):
    account = Account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)
    gas_limit = 21000
    gas_price = web3.to_wei('3', 'gwei')
    total_cost = (gas_limit * gas_price)

    balance_wei = web3.to_wei(amount, 'ether')
    amount_to_send = balance_wei - total_cost

    if balance_wei >= total_cost and amount_to_send > 0:
        tx = {
            'nonce': nonce,
            'to': destination_address,
            'value': amount_to_send,
            'gas': gas_limit,
            'gasPrice': gas_price
        }
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return f"Sent {web3.from_wei(amount_to_send, 'ether')} BNB. Transaction hash: {tx_hash.hex()}"

    return None

def process_key(queue, pbar):
    while True:
        key = queue.get()
        if key is None:
            break  # Sentinel value to end the thread
        balance = get_balance(key)
        if balance > 0.00001:
            response = send_bnb(key, balance)
            if response:
                print(response + f" Wallet with private key ending in ...{key[-5:]}")
        queue.task_done()
        pbar.update(1)  # Update the progress bar

# Load private keys from file
with open('addr.txt', 'r') as file:
    private_keys = file.read().splitlines()

# Create a queue and add your keys
queue = Queue()
[queue.put(key) for key in private_keys]

# Create a thread-safe tqdm progress bar
pbar = tqdm(total=len(private_keys), desc="Processing keys")

# Start threads
threads = [threading.Thread(target=process_key, args=(queue, pbar)) for _ in range(num_threads)]
[t.start() for t in threads]

# Wait for all keys to be processed
queue.join()

# Stop workers
[queue.put(None) for _ in range(num_threads)]
[t.join() for t in threads]

# Close the progress bar
pbar.close()
