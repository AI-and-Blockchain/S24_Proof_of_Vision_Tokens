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

    mapping(address => int256) public dividends; // value is number of wei
    POVToken public token;
    address[] public workers;
    // Placeholder for the pipelineAPI oracle

    // Changed from array to mapping due to runtime restrictions on arrays
    mapping(uint256 => Request) public waitingRequests;
    mapping(uint256 => Request) public workingRequests; 

    uint256[] waitingIDs;
    uint256[] workingIDs;

    uint256 public nextRequestID = 0; // Simple counter to track the next request ID

    constructor(address _tokenAddress) {
        token = POVToken(_tokenAddress);
        // Pipeline Chainlink API initialization placeholder
    }

    function createRequest(string memory datasetSource, string memory modelSource, uint256 bid) public {
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
    }

    function sendAllRequests() public {
        for(uint256 i = 0; i < waitingIDs.length; i++) {
            // TokenManager processing
            uint256 requestID = waitingIDs[i];
            workingIDs.push(requestID);
            waitingRequests[requestID].requestID = requestID;
            waitingRequests[requestID].datasetSource = waitingRequests[waitingIDs[i]].datasetSource;
            waitingRequests[requestID].modelSource = waitingRequests[waitingIDs[i]].modelSource;
            waitingRequests[requestID].requestOwner = waitingRequests[waitingIDs[i]].requestOwner;
            waitingRequests[requestID].bid = waitingRequests[waitingIDs[i]].bid;
            waitingRequests[requestID].consensusType = waitingRequests[waitingIDs[i]].consensusType;
            waitingRequests[requestID].results = waitingRequests[waitingIDs[i]].results;
            
            // Placeholder to send request to Pipeline API oracle
        }
    }

    function payDividends() public {
        //Unsure how to pay to addresses of each 
    }

    function retrieveData(uint256 requestID) public returns (string memory) {
        // Placeholder to access data from Pipeline API oracle with api callback
        // Request struct may be modified to store callback
    }

}
