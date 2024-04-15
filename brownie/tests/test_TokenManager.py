import pytest
from brownie import TokenManager, POVToken, accounts, reverts, web3


@pytest.fixture
def setup_contracts():
    pov_token = POVToken.deploy(accounts[0], {'from': accounts[0]})
    token_manager = TokenManager.deploy(
        pov_token.address, {'from': accounts[0]})
    return pov_token, token_manager


def test_create_request(setup_contracts):
    _, token_manager = setup_contracts

    # Creating a request
    tx = token_manager.createRequest("data_source", "model_source", 10, {
        'from': accounts[1], 'value': 1000})

    assert tx.status == 1, "Transaction failed"

    # Validate request creation
    request_id = token_manager.nextRequestID() - 1
    request = token_manager.requests(request_id)
    assert request[1] == "data_source"
    assert request[2] == "model_source"
    assert request[3] == accounts[1]
    assert request[5] == 10

    assert (token_manager.waitingIDs(0) == 0,
            "waitingIDs should have the new request ID")


def test_request_transition(setup_contracts):
    _, token_manager = setup_contracts

    token_manager.createRequest("data_source", "model_source", 10, {
                                'from': accounts[1], 'value': 10000})

    waiting_ids_before = token_manager.waitingIDs()

    token_manager.sendAllRequests({'from': accounts[0]})

    working_ids = token_manager.workingIDs()
    waiting_ids_after = token_manager.waitingIDs()

    assert len(working_ids) == 1
    assert len(waiting_ids_after) == 0

    # Compare the waiting IDs before moving with the working IDs in reverse order
    assert working_ids[0] == waiting_ids_before[-1]


def test_claim_dividends(setup_contracts):
    pov_token, token_manager = setup_contracts
    token_manager.createRequest("data_source", "model_source", 10, {
                                'from': accounts[1], 'value': 10000})
    pov_token.mint(accounts[2], 0, 10, b'', {'from': accounts[0]})

    # Distribute dividends to token holders
    token_manager.distributeDividends(10000, {'from': accounts[0]})

    initial_balance = accounts[2].balance()
    token_manager.claimDividends({'from': accounts[2]})
    assert accounts[2].balance() > initial_balance


def test_no_tokens(setup_contracts):
    _, token_manager = setup_contracts
    token_manager.createRequest("data_source", "model_source", 100, {
                                'from': accounts[1], 'value': 10000})

    with pytest.raises(Exception):
        token_manager.claimDividends({'from': accounts[0]})
