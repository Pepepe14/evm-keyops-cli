from web3 import Web3, EthereumTesterProvider
from eth_account import Account
from pathlib import Path
from helper import normalize_to_checksum

import secrets
import posix
import json
import os

def create_keystore(path: str, password: str) -> str: #(checksum address)
    ADDRESS_PREFIX = '0x'
    
    parent_dir = os.path.dirname(path) or "."
    secret_tkn = secrets.token_bytes(32)

    # Checks
    if os.path.isdir(path): 
        raise IsADirectoryError('The path is a dir path.')
    
    if not os.path.exists(parent_dir):
        raise FileNotFoundError('Not parent directory founded.')
    
    if os.path.exists(path): 
        raise FileExistsError("Overwrite prohibited - file already exists")
    
    if not os.path.isdir(parent_dir): 
        raise NotADirectoryError('Path exists but is not a directory. Please provide a valid directory path.')
    
    if not os.access(parent_dir, os.W_OK):
        raise PermissionError('Parent directory not writable.')
    
    #Encrypting data
    pk_account = Account.from_key(secret_tkn)
    acc_encrypted = pk_account.encrypt(password)
    
    with open(path, 'w') as ks_file: # Writting in Key Store file...   
        json.dump(acc_encrypted, ks_file)
       
    with open(path, 'r') as ks_file: # Checksumming address...
        data = json.load(ks_file)
    
    os.chmod(path, 0o600) # 0o600 permission in POSIX
    
    data_add = normalize_to_checksum(data['address'])
    file_addr = Web3.to_checksum_address(data_add)
    pk_address = Web3.to_checksum_address(pk_account.address)
    
    if pk_address == file_addr: 
        return pk_address  
    raise ValueError('Keystore address does not match PK')
    
def decrypt_keystore(path: str, password: str) -> bytes: #(32 bytes privkey)
    pass
    
def derived_address_from_privkey(privkey: bytes) -> str: #(checksum address)
    pass

def sign_message(privkey: bytes, msg: bytes) -> bytes: #(firma 65 bytes)
    pass

def verify_signature(address: str, msg: bytes, sig: bytes) -> bool:
    pass

def send_tx_eth_tester(privkey: bytes, to: str, value_wei: int) -> dict|str: #(recibo/tx_hash)
    pass

#if __name__ == '__main__':
#    create_keystore('', '')