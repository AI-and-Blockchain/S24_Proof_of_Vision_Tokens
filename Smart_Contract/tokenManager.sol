pragma solidity ^0.8.7;

contact tokenManager {
    struct Request{
        uint id;
        string datasetSource;
        string modelSource;
        address requestOwner;
        uint bid;
        string consensusType;
        mapping(address => uint) participation; 
    }
    mapping(address => uint) dividends;
    address[] workers;
    Request[] waitingRequests;
    Request[] workingRequests;

    function sendRequest (
        Request request
    )
    public
    {

    }

    function sendAllRequests(
    )
    public{

    }

    function payDividends(
    )
    public
    {

    }

    function createRequest(
        string memory datasetSource,
        string memory modelSource,
        uint bid
    )
    public
    {

    }

    function retrieveData(
        uint requestID
    )
    public
    returns(
        
    )
    {

    }
}
