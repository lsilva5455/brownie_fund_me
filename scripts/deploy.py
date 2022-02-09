###SE DEBE DESCOMENTAR VARIABLES Y FUNCIONES EN HELPFUL_SCRIPT.PY

from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_script import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_DEVEPLOMENT,
)


def deploy_fund_me():
    account = get_account()

    # si estamos en una red persitente como rinkeby usar la direccion asociada
    # sino  deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVEPLOMENT:
        ##se parametriza valor sacado desde brownie-config y se usa networks.show_active() para ver que red se esta usando
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is {network.show_active()}")
        print("deploy mocks ...")

        # solo va a desplegar una vez el contrato
        if len(MockV3Aggregator) <= 0:
            deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        print("mocks deployed")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed to {fund_me.address}")
    # fund_me es el contrato deployed.
    return fund_me


def main():
    deploy_fund_me()
