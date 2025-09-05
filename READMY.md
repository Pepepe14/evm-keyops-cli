# evm-keyops-cli

[![Status](https://img.shields.io/badge/status-in--progress-orange)](#)
[![Practice](https://img.shields.io/badge/practice-TDD-blue)](#)
[![Security](https://img.shields.io/badge/focus-security-critical)](#)

**MVP/WIP** — Tiny Web3.py lab to practice EVM key operations: Keystore V3, signing/verification, and local transactions with `EthereumTester`. **TDD-first, safety-first.**

---

## Status

**In progress (MVP/WIP).**
This is a small educational mini-project. Scope is local & reproducible; no mainnet, no real funds. Expect breaking changes while tests and API stabilize.

---

## What is this?

A minimal, educational repo to learn the basics of:

* Creating & reading **Keystore V3** files
* **Signing** and **verifying** messages (ECDSA)
* Sending **local transactions** against `EthereumTesterProvider`

**Scope:** local and reproducible. **No mainnet**, no real funds, no secrets in the repo.

---

## Quickstart

```bash
# Clone
git clone <REPO_URL>
cd evm-keyops-cli

# Environment
uv venv
source .venv/bin/activate

# Dependencies
uv pip install -U pytest ruff black web3 eth-account eth-abi eth-utils eth-tester

# (Optional) Vyper CLI available?
uvx vyper --version || true

# Run tests (the project is TDD-driven)
pytest -q

# Lint/format (check only)
ruff check .
black --check .
```

---

## Public API expected by tests (do not change signatures)

* `create_keystore(path: str, password: str) -> str`
  Writes a **Keystore V3** JSON and returns the **checksum address**.
* `decrypt_keystore(path: str, password: str) -> bytes`
  Returns the **32-byte private key**; fails clearly on wrong password.
* `derived_address_from_privkey(privkey: bytes) -> str`
  Returns the **checksum address** derived from the private key.
* `sign_message(privkey: bytes, msg: bytes) -> bytes`
  Signs a message (document the prefix scheme you use).
* `verify_signature(address: str, msg: bytes, sig: bytes) -> bool`
  Verifies the signature against the address.
* `send_tx_eth_tester(privkey: bytes, to: str, value_wei: int) -> dict|str`
  Sends a tx on `EthereumTesterProvider` and **changes the recipient balance**.

---

## CLI (future work)

When implemented, a simple `cli.py` could expose:

```bash
python cli.py create --keystore acct.json --password '...'
python cli.py addr   --keystore acct.json --password '...'
python cli.py sign   --keystore acct.json --password '...' --msg 'hello'
python cli.py send   --keystore acct.json --password '...' --to 0x... --value-wei 1000000000
```

**Outputs should be:**

* Address in **checksum** format
* Signature in hex/base64 (document which)
* Tx hash or receipt with `status == 1`

---

## What it does / What it doesn’t

**Does**

* Keystore V3 (create/read)
* Sign & verify with a consistent prefix strategy
* Local txs mined on `eth-tester` with observable balance change

**Doesn’t**

* Connect to public networks (mainnet/testnets)
* Manage hardware wallets or advanced KDF setups
* Provide a UI or complex contracts (out of scope for the mini-project)

---

## Testing tips

* If you see `json.decoder.JSONDecodeError`, your keystore file is not valid JSON V3 or is empty.
  Check size (`stat -c%s acct.json`), first char (`head -c 1 acct.json`), and keys (`version,address,crypto`).
* Always compare addresses in **checksum** form (`Web3.to_checksum_address`).
* Be explicit with errors—don’t silence exceptions.

---

## Security notes

* Do **NOT** commit real keystores or passwords.
* Use local throwaway passwords and ephemeral accounts.
* Document your signing prefix (e.g., EIP-191 style) and keep it consistent.

---

## License

MIT. See `LICENSE`.
