// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./POVToken.sol";
import "../node_modules/@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
import "../node_modules/@openzeppelin/contracts/utils/Strings.sol";
using EnumerableSet for EnumerableSet.AddressSet;

contract TokenManager {
    struct Request {
        uint256 requestID;
        string datasetSource;
        string modelSource;
        address requestOwner;
        uint256 bid;
        uint256 numImages;
        string consensusType;
        string results;
        EnumerableSet.AddressSet participants;
    }

    // Events for chain documentation
    event tokenPaid(uint tokenID, address paidTo);
    event dividendsPaid(uint amountPerToken);
    event dividendsClaimed(uint amount, address paidto);

    mapping(uint256 => uint256) public dividends; // key is token id, value is number of wei
    POVToken public token; // Token smart contract
    // Placeholder for the pipelineAPI oracle

    
    mapping(uint256 => Request) internal requests; // Requests stored by id

    EnumerableSet.UintSet internal waitingIDs; // IDs of waiting requests
    EnumerableSet.UintSet internal workingIDs; // IDs of working requests

    uint256 public nextRequestID = 0; // Simple counter to track the next request ID
    uint256 public nextTokenID = 0; // Simple counter to track the next token ID

    // Constructor sets token to already created token address
    constructor(address _tokenAddress) {
        token = POVToken(_tokenAddress);
        // Pipeline Chainlink API initialization placeholder
    }

    // Function that returns stringified information of complex types that cannot be returned. Used for testing asserts.
    function debugInfo() public view returns (string memory) {
        uint256 waitingCount = EnumerableSet.length(waitingIDs);
        uint256 workingCount = EnumerableSet.length(workingIDs);
        
        // Start building the debug info string
        bytes memory debug = abi.encodePacked(
            "Waiting Count: ", Strings.toString(waitingCount), "; ",
            "Working Count: ", Strings.toString(workingCount), "; "
        );
        
        debug = abi.encodePacked(debug, "Waiting IDs: ");
        // Append each ID from waitingIDs
        for (uint256 i = 0; i < waitingCount; i++) {
            debug = abi.encodePacked(debug, Strings.toString(EnumerableSet.at(waitingIDs, i)), ", ");
        }

        debug = abi.encodePacked(debug, "Working IDs: ");
        // Append each ID from workingIDs
        for (uint256 i = 0; i < workingCount; i++) {
            debug = abi.encodePacked(debug, Strings.toString(EnumerableSet.at(workingIDs, i)), ", ");
        }
        
        return string(debug);
    }
    
    // Creates a new request. msg.sender is supplier stakeholder
    function createRequest(string memory datasetSource, string memory modelSource, uint256 numImages) public payable returns(uint256){
        // Increment to next ID
        uint256 requestID = nextRequestID++;
        // Set request information
        Request storage request = requests[requestID];
        request.requestID = requestID;
        request.datasetSource = datasetSource;
        request.modelSource = modelSource;
        request.requestOwner = msg.sender;
        request.bid = msg.value;
        request.numImages = numImages;
        request.consensusType = "";

        EnumerableSet.add(waitingIDs, requestID);
        // Pay dividends to all tokens created before this request
        distributeDividends(msg.value);
        return requestID;
    }

    // Debug function which returns complex type information for testing
    function viewRequest(uint256 id) public view returns(string memory, string memory, address, uint256, uint256){
        return (requests[id].datasetSource, requests[id].modelSource, requests[id].requestOwner, requests[id].numImages, requests[id].bid);
    }

    // Moves requests from waiting to working and sends them to the pipeline oracle
    function sendAllRequests() public {
        for (uint256 i = 0; i < EnumerableSet.length(waitingIDs); i++) {
            uint256 requestID = EnumerableSet.at(waitingIDs, i);
            EnumerableSet.add(workingIDs, requestID);
            EnumerableSet.remove(waitingIDs, requestID);

            // Placeholder to send to api
        }
    }

    // distributes val // n wei to each n tokens in existence
    function distributeDividends(uint256 val) internal {
        if (nextTokenID == 0){
            return; // Case is first request: no tokens exist
        }
        uint valPerToken = val / nextTokenID;
        for(uint256 id = 0; id < nextTokenID; id++){
            dividends[id] += valPerToken;
        }
        emit dividendsPaid(valPerToken);
    }

    // Protection against reentrancy attack
    bool private _entered;
    modifier nonReentrant {
        require(!_entered, "re-entrant call");
        _entered = true;
        _;
        _entered = false;
    }

    // Pays out all dividends owed to msg.sender
    // Reverts if no dividends are claimed
    function claimDividends() public nonReentrant{
        uint256 totalDividends = 0;
        // iterate through each token and check if owner is msg.sender
        for (uint256 id = 0; id < nextTokenID; id++) {
            if (token.balanceOf(msg.sender, id) > 0) {
                totalDividends += dividends[id];
                dividends[id] = 0;
            }
        }
        require(totalDividends > 0, "No dividends to claim");
        emit dividendsClaimed(totalDividends, msg.sender);
        payable(msg.sender).transfer(totalDividends);
    }

    // Nonfunctional placeholder function to demonstrate intended security
    modifier pipelineOnly {
        // require(msg.sender == pipelineAddress);
        _;
    }

    // Callback function for pipeline to return results
    // Responsible for minting tokens to workers
    function retrieveData(uint256 requestID, string memory _results, address[] memory _participants) public pipelineOnly returns(uint){
        Request storage req = requests[requestID];

        req.results = _results;
        for (uint256 i = 0; i < _participants.length; i++) {
            req.participants.add(_participants[i]);
            uint tokenID = nextTokenID;
            nextTokenID++;
            token.mint(_participants[i], tokenID, 1, "");
        }
    }

    function getResults(uint256 requestID) public view returns (string memory) {
        return requests[requestID].results;
    }

}
