import os
from py_crypto_hd_wallet import HdWalletFactory, HdWalletCoins, HdWalletSpecs, HdWalletWordsNum
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip32
from bip_utils.bip.bip_keys import BipPrivateKey, BipPublicKey, BipPrivateKey
from bip_utils.bip.bip32_utils import Bip32Utils
from hdwallet import HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import ETH
import json
import uuid
from typing import Any, Dict, List, Union, NoReturn, Optional, Tuple
import hashlib
import struct
import flaskweb.config as config

py_cryto_hd_wallet_fact = HdWalletFactory(HdWalletCoins.ETHEREUM)

#these are testing, never use in production
_EX_PRIV = 'xprv9zQLLKGwTqVEaQczh1reEnjzrE4xh5U9og2KtFwTLyGNBauV6jBxJhiu9ZKyVSikUV74wsqutdryHyUUmPmtvSTzi5fFpen9pwED6Tzf1Bb'
_EX_PUB = 'xpub6DPgjpoqJD3XnthTo3PebvgjQFuT6YC1AtwvgeM4uJoM4PEdeGWCrW3NzsyeQRsWD8FJvhZMNjyG5HFzAJ1ABkZogGvA4tCgBNLiXL1uaCC'
#must at account level
_EX_PATH = "m/44'/60'/0'"

def get_address(add_idx:int) -> str:
    return ""

def new_oas_address(user_id:str, use_ex_priv:Optional[bool] = False) -> Tuple[str, str, str]:
    hash = hashlib.md5(user_id.encode('utf-8')).digest()
    #base i.e "m/44'/60'/0'" 
    bip32 = Bip32.FromExtendedKey(oas_config.get("EXTENDED_PUBKEY") if not use_ex_priv else oas_config.get("EXTENDED_PRIVKEY"))
    d_path = oas_config.get("EXTENDED_PATH")
    for i in range(2): 
        a = struct.unpack('<L',hash[i * 4:(i + 1) * 4])
        idx = a[0] % 1000000
        bip32 = bip32.ChildKey(idx)  
        d_path = d_path + "/" + str(idx)

    #now "m/44'/60'/0'/a1/a2", should be treated as geth like key(i.e. only private key use used, not true HD wallet at this level.
    a = BipPublicKey(bip32, Bip44Coins.ETHEREUM) if not use_ex_priv else BipPrivateKey(bip32, Bip44Coins.ETHEREUM)
    b = a.ToExtended()
    z = py_cryto_hd_wallet_fact.CreateFromExtendedKey("aa", b)
    z.Generate()
    c = z.ToDict()
    return c["addresses"]["address_1"]["address"], d_path, c["addresses"]["address_1"]["raw_priv"] if use_ex_priv else None

def new_wallet() -> dict:
    py_hd_wallet = py_cryto_hd_wallet_fact.CreateRandom("", HdWalletWordsNum.WORDS_NUM_24)
    py_hd_wallet.Generate()
    x = py_hd_wallet.ToDict()
    return dict(mnemonic = x["mnemonic"]
                ,path="m/44'/60'/0'/0/0"
                , ex_pub=x['change_key']['ex_pub']
                ,ex_priv=x['change_key']['ex_priv']
                , address=x["addresses"]["address_1"]["address"]
                , priv=x["addresses"]["address_1"]["raw_priv"]
                , pub=x["addresses"]["address_1"]["raw_uncompr_pub"])

def get_xprivkey(add_idx:Optional[int]) -> str:
    return str(uuid.uuid4())

def get_xpubkey(add_idx:Optional[int]) -> str:
    wallet = new_wallet()
    return str(uuid.uuid4())
