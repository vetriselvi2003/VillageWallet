from web3 import Web3
from eth_account import Account
from config import Config
import json

class BlockchainInterface:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(Config.POLYGON_RPC_URL))
        self.account = Account.from_key(Config.PRIVATE_KEY)
        self.contract_address = Config.CONTRACT_ADDRESS
        
        # Simple contract ABI (you would have your actual contract ABI)
        self.contract_abi = [
            {
                "inputs": [
                    {"name": "user", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "name": "disburseLoan",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "user", "type": "address"},
                    {"name": "amount", "type": "uint256"}
                ],
                "name": "repayLoan",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        
        if self.contract_address:
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.contract_abi
            )
    
    def create_wallet(self):
        """Create a new wallet for user"""
        try:
            account = Account.create()
            return {
                'address': account.address,
                'private_key': account.key.hex(),
                'success': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_balance(self, address):
        """Get wallet balance"""
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            print(f"Balance check error: {e}")
            return 0.0
    
    def disburse_loan(self, user_address, amount):
        """Disburse loan via smart contract"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            # Convert amount to Wei
            amount_wei = self.w3.to_wei(amount / 1000, 'ether')  # Convert rupees to a reasonable token amount
            
            # Build transaction
            transaction = self.contract.functions.disburseLoan(
                user_address,
                amount_wei
            ).build_transaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, Config.PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'amount': amount
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def process_repayment(self, user_address, amount):
        """Process loan repayment"""
        try:
            if not self.contract:
                return {'success': False, 'error': 'Contract not initialized'}
            
            amount_wei = self.w3.to_wei(amount / 1000, 'ether')
            
            transaction = self.contract.functions.repayLoan(
                user_address,
                amount_wei
            ).build_transaction({
                'from': self.account.address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, Config.PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'amount': amount
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}