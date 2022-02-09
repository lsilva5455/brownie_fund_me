from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

# se debe separa el develpoment con fork ya que le primero trabajo con mocks y el segundo no
FORKED_LOCAL_ENVIOREMENTS = ["mainnet-fork", "mainnet-fork-dev"]
# LOCAL_BLOCKCHAIN_DEVEPLOMENT son los network de development
LOCAL_BLOCKCHAIN_DEVEPLOMENT = ["development", "ganache-local"]
# para fund_me (porque tiene una funcion que lo multiplica por 10)en get_price
DECIMALS = 8
STARTING_PRICE = 200000000000

# para deploy.py
# DECIMALS = 18
# STARTING_PRICE = 2000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_DEVEPLOMENT
        or network.show_active() in FORKED_LOCAL_ENVIOREMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("deploy mocks ...")

    # solo va a deployear una vez el contrato
    # para fundme
    if len(MockV3Aggregator) <= 0:
        mock_aggreggator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {"from": get_account()}
        )
    # para deploy.py
    # if len(MockV3Aggregator) <= 0:
    #     mock_aggreggator = MockV3Aggregator.deploy(
    #         DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
    #     )
    price_feed_address = MockV3Aggregator[-1].address
    print("mocks deployed")
