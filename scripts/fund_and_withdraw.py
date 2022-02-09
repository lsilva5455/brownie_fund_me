###SE DEBE DESCOMENTAR VARIABLES Y FUNCIONES EN HELPFUL_SCRIPT.PY

from brownie import FundMe
from scripts.helpful_script import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = FundMe.getEntranceFee()
    # print(entrance_fee)
    print(f"The current entrance fee is {entrance_fee}")
    print("Funding...")
    # se utlizan 2 entradas, porque  la funcion requiere el adrs de quien lo envia y el valor
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
