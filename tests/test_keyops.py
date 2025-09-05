# tests/test_keyops.py
import os
import json
import binascii
import pytest
from web3 import Web3, EthereumTesterProvider


# Tú debes crear estas funciones en wallet_ops.py
# Diseñadas para TDD; NO cambies sus firmas.
from wallet_ops import (
    create_keystore,            # (path: str, password: str) -> str (checksum address)
    decrypt_keystore,           # (path: str, password: str) -> bytes (32 bytes privkey)
    derived_address_from_privkey, # (privkey: bytes) -> str (checksum address)
    sign_message,               # (privkey: bytes, msg: bytes) -> bytes (firma 65 bytes)
    verify_signature,           # (address: str, msg: bytes, sig: bytes) -> bool
    send_tx_eth_tester          # (privkey: bytes, to: str, value_wei: int) -> dict|str (recibo/tx_hash)
)

PASSWORD = "correct horse battery staple"
MSG = b"daniele: test message"

def test_keystore_roundtrip(tmp_path):
    ks_path = tmp_path / "acct.json"
    addr_file = create_keystore(str(ks_path), PASSWORD)
    assert addr_file.startswith("0x") and len(addr_file) == 42

    assert os.path.exists(ks_path)
    with open(ks_path, "r") as f:
        data = json.load(f)
    assert "crypto" in data and "address" in data  # formato V3

    priv = decrypt_keystore(str(ks_path), PASSWORD)
    assert isinstance(priv, (bytes, bytearray)) and len(priv) == 32

    addr_derived = derived_address_from_privkey(priv)
    # Las direcciones deben coincidir (case-insensitive); validamos en checksum.
    assert Web3.to_checksum_address(addr_derived) == Web3.to_checksum_address(addr_file)

def test_sign_and_verify():
    # Genera temporalmente un keystore en memoria si necesitas, o reutiliza create_keystore con tmp_path
    # Aquí validamos la pareja sign/verify como contrato social de tus funciones.
    priv = binascii.unhexlify("5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a")
    addr = derived_address_from_privkey(priv)
    sig = sign_message(priv, MSG)
    assert isinstance(sig, (bytes, bytearray)) and len(sig) in (65, 72)  # 65 clásico, 72 si DER (acepta ambas)
    assert verify_signature(addr, MSG, sig) is True

def test_send_tx_eth_tester_changes_balance():
    w3 = Web3(EthereumTesterProvider())
    # Cuenta destino (primera de eth-tester) para ver cambios de balance
    to = w3.eth.accounts[0]
    # Genera tu propia cuenta desde privkey fija para reproducibilidad (no dependas de pre-funded)
    priv = binascii.unhexlify("5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a")
    sender = Web3.to_checksum_address(derived_address_from_privkey(priv))

    # Asegúrate de que el sender tenga fondos (por ejemplo, transfiriendo desde accounts[0] antes,
    # o usando un faucet interno según eth-tester). Tu implementación debe resolverlo.

    bal_before = w3.eth.get_balance(to)
    receipt = send_tx_eth_tester(priv, to, 10**9)  # 1 gwei
    # Debe devolver recibo o hash; en ambos casos, la tx debe estar minada.
    if isinstance(receipt, dict):
        assert receipt.get("status", 1) == 1
    bal_after = w3.eth.get_balance(to)
    assert bal_after > bal_before
