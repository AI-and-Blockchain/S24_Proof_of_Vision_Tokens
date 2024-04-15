// pragma solidity ^0.8.0;

// import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
// import "@chainlink/contracts/src/v0.8/Chainlink.sol";

// contract APICaller is ChainlinkClient {
//     using Chainlink for Chainlink.Request;

//     uint256 public data;
//     address private oracle;
//     bytes32 private jobId;
//     uint256 private fee;

//     constructor() {
//         setPublicChainlinkToken();
//         //oracle = ; // This needs to be the Chainlink Oracle address
//         jobId = "b6602d14e4734c49a5e1ce19d45a4632"; // Job ID for a GET > Uint256 request
//         fee = 0.1 * 10 ** 18; // 0.1 LINK
//     }

//     function requestData() public returns (bytes32 requestId) {
//         Chainlink.Request memory request = buildChainlinkRequest(jobId, address(this), this.fulfill.selector);
//         request.add("get", "https://dull-scrubs-bee.cyclic.app/showlabels"); // Set the URL to the API endpoint
//         request.add("path", "data.path.to.value"); // Set the path to find the desired data in the API response JSON
//         return sendChainlinkRequestTo(oracle, request, fee);
//     }

//     function fulfill(bytes32 _requestId, uint256 _data) public recordChainlinkFulfillment(_requestId) {
//         data = _data;
//     }
// }
