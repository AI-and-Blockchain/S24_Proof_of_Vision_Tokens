import pytest
from brownie import TokenManager, POVToken, FetchFromArray, accounts, reverts, web3


def test_chain():
    fetcher = FetchFromArray.deploy({'from': accounts[0]})

# @pytest.fixture
# def setup_contracts():
#     pov_token = POVToken.deploy({'from': accounts[0]})
#     token_manager = TokenManager.deploy(
#         pov_token.address, {'from': accounts[0]})
#     pov_token.setOwner(token_manager.address, {'from': accounts[0]})

#     # token_manager.setToken(pov_token.address)

#     return pov_token, token_manager


# def test_create_request(setup_contracts):
#     _, token_manager = setup_contracts

#     # Creating a request
#     bid = 1000
#     numImages = 10
#     tx = token_manager.createRequest("data_source", "model_source", numImages, {
#         'from': accounts[1], 'value': bid})

#     assert tx.status == 1, "Transaction failed"

#     # Validate request creation
#     request_id = token_manager.nextRequestID() - 1
#     request = token_manager.viewRequest(request_id)
#     assert request[0] == "data_source"
#     assert request[1] == "model_source"
#     assert request[2] == accounts[1]
#     assert request[3] == numImages
#     assert request[4] == bid

#     assert (token_manager.debugInfo() ==
#             "Waiting Count: 1; Working Count: 0; Waiting IDs: 0, Working IDs: ")


# def test_request_transition(setup_contracts):
#     _, token_manager = setup_contracts

#     token_manager.createRequest("data_source", "model_source", 10, {
#                                 'from': accounts[1], 'value': 10000})

#     assert (token_manager.debugInfo() ==
#             "Waiting Count: 1; Working Count: 0; Waiting IDs: 0, Working IDs: ")

#     token_manager.sendAllRequests({'from': accounts[0]})

#     assert (token_manager.debugInfo() ==
#             "Waiting Count: 0; Working Count: 1; Waiting IDs: Working IDs: 0, ")


# def test_no_tokens(setup_contracts):
#     _, token_manager = setup_contracts
#     token_manager.createRequest("data_source", "model_source", 100, {
#                                 'from': accounts[1], 'value': 10000})

#     with pytest.raises(Exception):
#         token_manager.claimDividends({'from': accounts[0]})


# def test_retrieve_data(setup_contracts):
#     _, token_manager = setup_contracts

#     tx = token_manager.createRequest("data_source", "model_source", 10, {
#         'from': accounts[1], 'value': 10000})
#     id = tx.return_value
#     assert (token_manager.debugInfo() ==
#             "Waiting Count: 1; Working Count: 0; Waiting IDs: 0, Working IDs: ")

#     token_manager.sendAllRequests({'from': accounts[0]})
#     assert (token_manager.debugInfo() ==
#             "Waiting Count: 0; Working Count: 1; Waiting IDs: Working IDs: 0, ")

#     participants = [accounts[2], accounts[3], accounts[4]]
#     results = "0 1 2 3 4 5 6 7 8 9"
#     tx = token_manager.retrieveData(id, results, participants)
#     assert (token_manager.nextTokenID() == 3)

#     results2 = token_manager.getResults(id)
#     assert (results == results2)

#     # Distribute dividends to token holders
#     bid = 20000
#     token_manager.createRequest("data_source2", "model_source2", 20, {
#                                 'from': accounts[1], 'value': bid})

#     initial_balance = accounts[2].balance()
#     token_manager.claimDividends({'from': accounts[2]})

#     increase = bid // len(participants)
#     assert accounts[2].balance() == initial_balance + increase
