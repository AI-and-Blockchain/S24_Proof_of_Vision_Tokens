from web3.exceptions import BadResponseFormat
import pytest
from brownie import TokenManager, POVToken, accounts, reverts


@pytest.fixture
def token_manager():
    # Deploy POVToken contract
    initial_owner = accounts[0]
    pov_token = POVToken.deploy(initial_owner, {'from': accounts[0]})

    # Deploy TokenManager contract
    token_manager = TokenManager.deploy(
        pov_token.address, {'from': accounts[0]})
    return token_manager


def test_create_request(token_manager):
    # Test createRequest function
    token_manager.createRequest("dataset_source", "model_source", 100, {
                                'from': accounts[1], 'value': "1 ether"})
    assert token_manager.nextRequestID() == 1


def test_send_all_requests(token_manager):
    # Test sendAllRequests function
    token_manager.createRequest("dataset_source", "model_source", 100, {
                                'from': accounts[1], 'value': "1 ether"})
    token_manager.sendAllRequests({'from': accounts[0]})
    assert len(token_manager.workingIDs()) == 1
    assert len(token_manager.waitingIDs()) == 0


def test_no_tokens(token_manager):

    # Test claimDividends function fails when caller has no tokens
    token_manager.createRequest("dataset_source", "model_source", 100, {
        'from': accounts[1], 'value': "1 ether"
    })

    try:
        # Assert that claimDividends reverts with the expected error message
        with reverts("No dividends to claim"):
            token_manager.claimDividends({'from': accounts[0]})
    except BadResponseFormat as e:
        print("BadResponseFormat exception occurred:")
        print(f"Error message: {str(e)}")
        print(f"Response: {e.response}")
        raise
