// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./POVToken.sol";

contract TokenManager {
    struct Request {
        uint256 requestID;
        string datasetSource;
        string modelSource;
        address requestOwner;
        uint256 bid;
        uint256 numImages;
        string consensusType;
        int[] results;
        mapping(address => uint256) participation; // "Normalized" to 100,000 bc no floats
    }

    mapping(uint256 => uint256) public dividends; // key is token id, value is number of wei
    POVToken public token;
    address[] public workers;
    // Placeholder for the pipelineAPI oracle

    // Changed from array to mapping due to runtime restrictions on arrays
    mapping(uint256 => Request) public waitingRequests;
    mapping(uint256 => Request) public workingRequests; 

    uint256[] waitingIDs;
    uint256[] workingIDs;

    uint256 public nextRequestID = 0; // Simple counter to track the next request ID
    uint256 public nextTokenID = 0; // Simple counter to track the next token ID

    constructor(address _tokenAddress) {
        token = POVToken(_tokenAddress);
        // Pipeline Chainlink API initialization placeholder
    }

    function createRequest(string memory datasetSource, string memory modelSource, uint256 bid) public payable{
        // Increment to next ID
        uint256 requestID = nextRequestID++;
        // Creates request if it doesn't exist on access
        waitingRequests[requestID].requestID = requestID;
        waitingRequests[requestID].datasetSource = datasetSource;
        waitingRequests[requestID].modelSource = modelSource;
        waitingRequests[requestID].requestOwner = msg.sender;
        waitingRequests[requestID].bid = bid;
        waitingRequests[requestID].consensusType = "";
        waitingRequests[requestID].results = [int256(10000)];
        waitingIDs.push(requestID);

        distributeDividends(msg.value);
    }

    function sendAllRequests() internal {
        for(uint256 i = 0; i < waitingIDs.length; i++) {

            // Move request from waitingRequests to workingRequests
            uint256 requestID = waitingIDs[i];
            workingRequests[requestID].requestID = requestID;
            workingRequests[requestID].datasetSource = waitingRequests[requestID].datasetSource;
            workingRequests[requestID].modelSource = waitingRequests[requestID].modelSource;
            workingRequests[requestID].requestOwner = waitingRequests[requestID].requestOwner;
            workingRequests[requestID].bid = waitingRequests[requestID].bid;
            workingRequests[requestID].consensusType = waitingRequests[requestID].consensusType;
            workingRequests[requestID].results = waitingRequests[requestID].results;
            
            workingIDs.push(requestID);
            delete waitingRequests[requestID];

            // Placeholder to send requests to Pipeline API oracle
        }
        delete waitingIDs;    
    }

    function distributeDividends(uint256 val) private {
        for(uint256 id = 0; id < nextTokenID; id++){
            dividends[id] += val;
        }
    }

    bool private _entered;
    modifier nonReentrant {
        require(!_entered, "re-entrant call");
        _entered = true;
        _;
        _entered = false;
    }

    function claimDividends() public nonReentrant{
        uint256 totalDividends = 0;
        for (uint256 id = 0; id < nextTokenID; id++) {
            if (token.balanceOf(msg.sender, id) > 0) {
                totalDividends += dividends[id];
                dividends[id] = 0;
            }
        }
        require(totalDividends > 0, "No dividends to claim");
        payable(msg.sender).transfer(totalDividends);
    }

    function retrieveData(uint256 requestID) public returns (string memory) {
        // Placeholder to access data from Pipeline API oracle with api callback
        // Request struct may be modified to store callback
    }

}
