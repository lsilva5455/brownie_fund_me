from scripts.helpful_script import get_account, LOCAL_BLOCKCHAIN_DEVEPLOMENT
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    # arrange
    account = get_account()
    # fund_me es el contrato FundMe.sol deployed por lo que pueden llamar a sus funciones, eventos y variable
    fund_me = deploy_fund_me()
    # entrance_fee es el valor en de 50dolare convertidos a wei, el fund es un valor fijo de 50 usd
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # el primer testeo es para ver vi entrance_fee (que son los 50usd convertidos a wei) quedo guardado
    # en el arreglo addressToAmountFunded de forma correcta para la account que llamo a la funcion fund
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    # este test verifica que addressToAmountFunded del account  se vaya a 0 cuando se realice el retiro
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVEPLOMENT:
        pytest.skip("Only for local testing")
    #  account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    # si aparece el error por revert dado porque un address distinto del owner esta tratando de scara los morlacos y existe
    # un require el el contract con un revert
    # se maneja la expecion
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
