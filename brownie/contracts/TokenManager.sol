// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./POVToken.sol";
import "./node_modules/@openzeppelin/contracts/utils/structs/EnumerableSet.sol";
import "./node_modules/@openzeppelin/contracts/utils/Strings.sol";
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

    mapping(uint256 => uint256) public dividends; // key is token id, value is number of wei
    POVToken public token;
    address[] public workers;
    // Placeholder for the pipelineAPI oracle

    // Changed from array to mapping due to runtime restrictions on arrays
    mapping(uint256 => Request) internal requests;

    EnumerableSet.UintSet internal waitingIDs;
    EnumerableSet.UintSet internal workingIDs;

    uint256 public nextRequestID = 0; // Simple counter to track the next request ID
    uint256 public nextTokenID = 0; // Simple counter to track the next token ID

    constructor(address _tokenAddress) {
        token = POVToken(_tokenAddress);
        // Pipeline Chainlink API initialization placeholder
    }

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

    function testMint(address account, uint256 id, uint256 amount, bytes memory data) public {
        ++nextTokenID;
    }


    function createRequest(string memory datasetSource, string memory modelSource, uint256 numImages) public payable{
        // Increment to next ID
        uint256 requestID = nextRequestID++;
        Request storage request = requests[requestID];
        request.requestID = requestID;
        request.datasetSource = datasetSource;
        request.modelSource = modelSource;
        request.requestOwner = msg.sender;
        request.bid = msg.value;
        request.numImages = numImages;
        request.consensusType = "";

        EnumerableSet.add(waitingIDs, requestID);

        distributeDividends(msg.value);
    }

    function sendAllRequests() public {
        for (uint256 i = 0; i < EnumerableSet.length(waitingIDs); i++) {
            uint256 requestID = EnumerableSet.at(waitingIDs, i);
            EnumerableSet.add(workingIDs, requestID);

            // Placeholder to send to api

            EnumerableSet.remove(waitingIDs, requestID);
        }


    }

    function distributeDividends(uint256 val) public {
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

    function retrieveData(
        uint256 requestID,
        string memory _results,
        address[] memory _participants
    ) public {
        Request storage req = requests[requestID];

        req.results = _results;

        for (uint256 i = 0; i < _participants.length; i++) {
            req.participants.add(_participants[i]);
        }
    }

    function getResults(uint256 requestID) public view returns (string memory) {
        return requests[requestID].results;
    }

}
