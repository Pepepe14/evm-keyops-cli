ADDRESS_PREFIX = '0x'

def normalize_to_checksum(addr: str) -> str:
    data_add_v = ADDRESS_PREFIX + addr if not addr.startswith(ADDRESS_PREFIX) else addr
    return data_add_v
