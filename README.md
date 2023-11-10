# BulkBNB

## Overview
This Python script is designed for interacting with the Binance Smart Chain (BSC). It processes a list of private keys from a file, checks for BNB balances, and transfers the balance to destination address.

## Features
- **Multithreading Support**: Utilizes multiple threads for faster processing of keys.
- **Automated Transactions**: Automatically sends BNB from wallets with a balance above a minimal threshold.

## Configuration

- Must have Python3.6+
- Ensure private keys are listed one per line in a text file named `addr.txt`.
- Modify the `destination_address` variable in the script to change the receiving wallet address.

***Install The Required libraries***

   ```bash
   pip3 install web3 eth_account tqdm
   ```
## Usage

1. Place your private keys in a file named addr.txt, each key on a new line.
2. Run the script using Python:

   ```python
   python3 script_name.py --threads [NUMBER_OF_THREADS]
   ```
- Replace `[NUMBER_OF_THREADS]` with the desired number of threads (MAX 10)

## Disclaimer
***This script is for educational purposes only. Ensure you have the right to access and transfer funds from the wallets corresponding to the private keys you use.***

## Donations

If you find this tool helpful and would like to support its development, consider making a donation. Any contributions are greatly appreciated.

- **Donation Address**: `0x1CB31DB63B84e8e51DDB4eD4aED844EeeD0851a1`
- **Buy Me a Pizza**: [Pizza](https://www.buymeacoffee.com/web3dev.ma)
