# works with web3===6.14.0
# 你要用python自动交易，肯定要连接钱包，钱包是要能支付到polymarket上面USDC（条件代币），我们购买yes no，token，所以需要授权



from web3 import Web3
from web3.constants import MAX_INT
from web3.middleware import geth_poa_middleware

rpc_url = "https://polygon-rpc.com" # Polygon rpc url 
priv_key = "f14af2100840da79a81fd16a5e7577f25f425192a5cc0b009422853bc42658c4" # Polygon account private key (needs some MATIC)
pub_key = "0x220aB136bDf671D86B76E5A465A322a03A289274" # Polygon account public key corresponding to private key..The pub_key is the 42-character wallet address derived from the 130-character public key, not the public key itself.
chain_id = 137

erc20_approve = """[{"constant": false,"inputs": [{"name": "_spender","type": "address" },{ "name": "_value", "type": "uint256" }],"name": "approve","outputs": [{ "name": "", "type": "bool" }],"payable": false,"stateMutability": "nonpayable","type": "function"}]"""
erc1155_set_approval = """[{"inputs": [{ "internalType": "address", "name": "operator", "type": "address" },{ "internalType": "bool", "name": "approved", "type": "bool" }],"name": "setApprovalForAll","outputs": [],"stateMutability": "nonpayable","type": "function"}]"""

usdc_address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" # MATIC collateral
ctf_address = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045" # MATIC conditionalTokens

web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

nonce = web3.eth.get_transaction_count(pub_key)

usdc = web3.eth.contract(address=usdc_address, abi=erc20_approve)
ctf = web3.eth.contract(address=ctf_address, abi=erc1155_set_approval)


# CTF Exchange
raw_usdc_approve_txn = usdc.functions.approve("0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", int(MAX_INT, 0)
).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
signed_usdc_approve_tx = web3.eth.account.sign_transaction(raw_usdc_approve_txn, private_key=priv_key)


print(dir(signed_usdc_approve_tx))

send_usdc_approve_tx = web3.eth.send_raw_transaction(signed_usdc_approve_tx.raw_transaction)
usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(send_usdc_approve_tx, 600)
print(usdc_approve_tx_receipt)




# USDC代币的ABI,包含allowance函数
usdc_abi = """[{
    "constant": true,
    "inputs": [
        {"name": "_owner","type": "address"},
        {"name": "_spender","type": "address"}
    ],
    "name": "allowance",
    "outputs": [{"name": "","type": "uint256"}],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
}]"""

# 检查授权额度
usdc_contract = web3.eth.contract(address=usdc_address, abi=usdc_abi)
allowance = usdc_contract.functions.allowance(
    pub_key,    # 你的地址,使用已定义的pub_key
    "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"  # CTF Exchange合约地址
).call()
print(f"当前授权额度: {web3.from_wei(allowance, 'ether')} USDC")





USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# 检查 USDC 余额
def check_usdc_balance(wallet_address):
    web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    usdc_contract = web3.eth.contract(address=USDC_ADDRESS, abi=usdc_abi)
    balance = usdc_contract.functions.balanceOf(wallet_address).call()
    return web3.from_wei(balance, 'mwei')  # USDC 是 6 位小数

print(check_usdc_balance(pub_key))



















# USDC 合约地址（Polygon）
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

# USDC 合约的 ABI（只包含我们需要的函数）
USDC_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# 检查 USDC 余额
def check_usdc_balance(wallet_address):
    web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    usdc_contract = web3.eth.contract(address=USDC_ADDRESS, abi=USDC_ABI)
    balance = usdc_contract.functions.balanceOf(wallet_address).call()
    return web3.from_wei(balance, 'mwei')  # USDC 是 6 位小数

# 检查余额
print(f"USDC 余额: ${check_usdc_balance(pub_key)}")

# 检查授权额度
def check_usdc_allowance(wallet_address, spender_address):
    web3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    usdc_contract = web3.eth.contract(address=USDC_ADDRESS, abi=USDC_ABI)
    allowance = usdc_contract.functions.allowance(
        wallet_address,
        spender_address
    ).call()
    return web3.from_wei(allowance, 'mwei')

# Polymarket 合约地址
POLYMARKET_ADDRESS = "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E"

# 检查授权
allowance = check_usdc_allowance(pub_key, POLYMARKET_ADDRESS)
print(f"USDC 授权额度: ${allowance}")























# 下一步，设置CTF Exchange的授权额度

# 可以检查当前 gas 价格
current_gas_price = web3.eth.gas_price
print(f"当前 gas 价格: {web3.from_wei(current_gas_price, 'gwei')} gwei")

# 如果需要加快交易，可以提高 gas 价格
gas_price = int(current_gas_price * 1.3)  # 提高20%的gas价格
print(f"调整后 gas 价格: {web3.from_wei(gas_price, 'gwei')} gwei")


nonce = web3.eth.get_transaction_count(pub_key)

# 在 build_transaction 中添加 gasPrice 参数
raw_ctf_approval_txn = ctf.functions.setApprovalForAll(
    "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", 
    True
).build_transaction({
    "chainId": chain_id, 
    "from": pub_key, 
    "nonce": nonce,
    "gasPrice": gas_price  # 这里添加调整后的 gas 价格
})

signed_ctf_approval_tx = web3.eth.account.sign_transaction(raw_ctf_approval_txn, private_key=priv_key)


send_ctf_approval_tx = web3.eth.send_raw_transaction(signed_ctf_approval_tx.raw_transaction)
ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(send_ctf_approval_tx, 120)
print(ctf_approval_tx_receipt)







nonce = web3.eth.get_transaction_count(pub_key)





# Neg Risk CTF Exchange
raw_usdc_approve_txn = usdc.functions.approve("0xC5d563A36AE78145C45a50134d48A1215220f80a", int(MAX_INT, 0)
).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
signed_usdc_approve_tx = web3.eth.account.sign_transaction(raw_usdc_approve_txn, private_key=priv_key)
send_usdc_approve_tx = web3.eth.send_raw_transaction(signed_usdc_approve_tx.raw_transaction)
usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(send_usdc_approve_tx, 120)
print(usdc_approve_tx_receipt)

nonce = web3.eth.get_transaction_count(pub_key)

raw_ctf_approval_txn = ctf.functions.setApprovalForAll("0xC5d563A36AE78145C45a50134d48A1215220f80a", True).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
signed_ctf_approval_tx = web3.eth.account.sign_transaction(raw_ctf_approval_txn, private_key=priv_key)
send_ctf_approval_tx = web3.eth.send_raw_transaction(signed_ctf_approval_tx.raw_transaction)
ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(send_ctf_approval_tx, 120)
print(ctf_approval_tx_receipt)

nonce = web3.eth.get_transaction_count(pub_key)

# Neg Risk Adapter
raw_usdc_approve_txn = usdc.functions.approve("0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", int(MAX_INT, 0)
).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
signed_usdc_approve_tx = web3.eth.account.sign_transaction(raw_usdc_approve_txn, private_key=priv_key)
send_usdc_approve_tx = web3.eth.send_raw_transaction(signed_usdc_approve_tx.raw_transaction)
usdc_approve_tx_receipt = web3.eth.wait_for_transaction_receipt(send_usdc_approve_tx, 120)
print(usdc_approve_tx_receipt)

nonce = web3.eth.get_transaction_count(pub_key)

raw_ctf_approval_txn = ctf.functions.setApprovalForAll("0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296", True).build_transaction({"chainId": chain_id, "from": pub_key, "nonce": nonce})
signed_ctf_approval_tx = web3.eth.account.sign_transaction(raw_ctf_approval_txn, private_key=priv_key)
send_ctf_approval_tx = web3.eth.send_raw_transaction(signed_ctf_approval_tx.raw_transaction)
ctf_approval_tx_receipt = web3.eth.wait_for_transaction_receipt(send_ctf_approval_tx, 120)
print(ctf_approval_tx_receipt)









