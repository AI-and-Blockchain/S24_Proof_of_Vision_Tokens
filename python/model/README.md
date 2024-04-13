# Deep Learning Client-Server Model for Image Classification
This repository contains a Python application designed for machine learning model training and evaluation using TensorFlow, focused on image classification tasks. It integrates client-server interaction for handling batches of images and processing their labels.

---

### Table of Contents
You're sections headers will be used to reference location of destination.

- [Overview](#Overview)
- [How To Use](#how-to-use)
- [Features](#Features)

---

## Overview

Creating ReadMe's for your Github repository can be tedious.  I hope this template can save you time and effort as well as provide you with some consistency across your projects.
The system comprises two primary components:
- client: Handles requests for batches of images and the submission of predicted labels to a server.
- user: Manages the downloading and processing of image datasets and machine learning models, and performs image classification.

---

## How To Use
## Prerequisites
 * Before you begin, ensure you have Python installed on your system. The project is 
   built using Python 3.8+.
 * TensorFlow, NumPy, and other necessary Python libraries.


#### Installation
To get started with this project, clone the repository and install the required dependencies.

```html
git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
```
#### Configuration
Set the model and dataset URLs in the client initialization. These URLs are used to download the necessary machine learning model and image dataset.

#### Usage
Set the model and dataset URLs in the client initialization. These URLs are used to download the necessary machine learning model and image dataset.

1. Initialize the Client and User:
   * Set up the client with links to the model and dataset.
   * Create a user instance with a specific Ethereum address linked to the client.

2. Load and Process Batch
   * The user requests and loads a batch of images.
   * Processes the images and prepares them for classification.

3. Start Mining: 
   * Execute image classification.
   * Send classification results back to the server.

Example code snippet to set up and run the system:

```html
# Define user and server details
eth_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
server_url = "https://dull-scrubs-bee.cyclic.app"

# Initialize the client with model and dataset URLs
client = Client(model_url='https://path.to/model.h5', dataset_url='https://path.to/dataset.zip')

# Create a user and assign a batch
user = User(eth_address, client)
user.request_and_load_batch()

# Process images and submit labels
labels = user.startMining()
client.receive_labels(eth_address, labels)

```
## Features
* Image Processing: Filters and prepares images for classification.
* Model Prediction: Utilizes TensorFlow to predict image labels based on the trained model.
* Server Communication: Sends predicted labels back to the server via a PUT request.

## License
MIT


