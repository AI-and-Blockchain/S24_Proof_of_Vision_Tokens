# Introduction
This document guides you through the installation of Brownie and how to run tests for the Solidity smart contracts that make up the blockchain component of the Proof Of Vision project, as well as the full integration test requiring the API to be active, and three instances of worker to achieve consensus. The results of the tests will be outputted to a log file for review.
# Prerequisites
- Conda installed on machine
- NPM installed on machine
# Installation Steps
`Conda create -n POV`

`Conda activate POV`

`Conda install pip`

`pip install eth-brownie tensorflow matplotlib numpy pillow`

Navigate to brownie root folder

`npm install @openzeppelin/contracts`

`brownie test --logging=INFO > test_results.log`

# Files
- contracts  
--> POVToken.sol [The token reward]  
--> TokenManager.sol [The main smart contract that processes requests]  
--> chain.sol [barebones test connectivitiy for chainlink]  
- tests  
--> test_TokenManager.py [Tests all smart contracts as they are all connected through TokenManager]  
