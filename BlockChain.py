

from Block import Block, Proof0fWork
from Transaction import Transaction
from Wallet import Wallet, verify_sign



class BlockChain:
    """
        区块链结构体
            blocks：         包含区块的列表
    """

    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        """
        添加区块
        :param block:
        :return:
        """
        self.blocks.append(block)

    def print_list(self):
        print(f"区块链包含个数为：{len(self.blocks)}")
        for block in self.blocks:
            height=0
            print(f"区块链高度为：{height}")
            print(f"父区块为：{block.prev_hash}")
            print(f"区块内容为：{block.transactions}")
            print(f"区块哈希值为：{block.hash}")
            height += 1
            print()

# 传入用户和区块链，返回用户的“余额”
def get_balance(user,blockchain):
    balance=0
    for block in blockchain.blocks:
        for t in block.transactions:
            if t.sender == user.address.decode():
                balance -= t.amount
            elif t.recipient == user.address.decode():
                balance += t.amount
    return balance

# user生成创世区块（新建区块链），并添加到区块链中
def generate_genesis_block(user):
    blockchain=BlockChain()
    new_block=Block(transactions=[],prev_hash="")
    w=Proof0fWork(new_block,user)
    genesis_block=w.mine()
    blockchain.add_block(genesis_block)
    #返回创世区块
    return  blockchain


# 用户之间进行交易并记入交易列表
def add_transaction(sender,recipient,amount):
    # 新建交易
    new_transaction=Transaction(
        sender=sender.address,
        recipient=recipient.address,
        amount=amount
    )
    # 生成数字签名
    sig=sender.sign(str(new_transaction))
    # 传入付款方的公钥和签名
    new_transaction.set_sign(sig,sender.pubkey)
    return new_transaction


# 验证交易，若验证成功则加入交易列表
def verify_new_transaction(new_transaction,transactions):
    if verify_sign(new_transaction.pubkey,
                   str(new_transaction),
                   new_transaction.signature
                   ):
        # 验证交易签名没问题，加入交易列表
        print("交易验证成功")
        transactions.append(new_transaction)
    else:
        print("交易验证失败")


# 矿工将全部验证成功的交易列表打包出块
def generate_block(miner,transactions,blockchain):
    new_block = Block(transactions=transactions,
                      prev_hash=blockchain.blocks[len(blockchain.blocks) - 1].hash
    )
    print("生成新的区块...")
    w=Proof0fWork(new_block,miner)
    block=w.mine()
    print("将新区块添加到区块链中")
    blockchain.add_block(block)

# 新建交易列表
transactions=[]

# 创建3个用户
alice=Wallet()
tom=Wallet()
bob=Wallet()

print("alice创建创世区块...")
blockchain=generate_genesis_block(alice)
print()

print(f"alice 的余额为{get_balance(alice, blockchain)}个比特币")
print(f"tom 的余额为{get_balance(tom, blockchain)}个比特币")
print(f"bob 的余额为{get_balance(bob, blockchain)}个比特币")
print()

# 打印区块链信息
blockchain.print_list()

print("新增交易：alice 转账 2 比特币给 tom")
nt = add_transaction(alice, tom, 2)
print()
verify_new_transaction(nt, transactions)
print(f"矿工 bob 将全部验证成功的交易列表打包出块...")
generate_block(bob, transactions, blockchain)
print("添加完成\n")

# 打印区块链信息
blockchain.print_list()
