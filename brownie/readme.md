# Introduction
This document guides you through the installation of Brownie and how to run tests for the Solidity smart contracts that make up the blockchain component of the Proof Of Vision project. The results of the tests will be outputted to a log file for review.
# Prerequisites
- Python 3.6+ installed on your machine
- pip for managing Python packages
# Installation Steps
`pip install eth-brownie`

Navigate to brownie root folder

`brownie test --logging=INFO > test_results.log`

# Files
- contracts  
--> POVToken.sol [The token reward]  
--> TokenManager.sol [The main smart contract that processes requests]  
--> chain.sol [barebones test connectivitiy for chainlink]  
- tests  
--> test_TokenManager.py [Tests all smart contracts as they are all connected through TokenManager]  

# Final Note
This week types and structure is in flux and diagrams are slightly behind. Once we integrate a dynamic array library and believe we can move away from this problem, the diagrams will be prompty updated.
