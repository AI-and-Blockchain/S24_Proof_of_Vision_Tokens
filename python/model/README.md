# Deep Learning Client-Server Model for Image Classification
This repository contains a Python application designed for machine learning model training and evaluation using TensorFlow, focused on image classification tasks. It integrates client-server interaction for handling batches of images and processing their labels.

# Overview
The system comprises two primary components:

client: Handles requests for batches of images and the submission of predicted labels to a server.
user: Manages the downloading and processing of image datasets and machine learning models, and performs image classification.
Installation
To get started with this project, clone the repository and install the required dependencies.


git clone https://github.com/your-username/your-repo.git
cd your-repo
pip install -r requirements.txt
Configuration
Set the model and dataset URLs in the client initialization. These URLs are used to download the necessary machine learning model and image dataset.

Usage
Initialize the Client and User: The client is initialized with URLs to the model and dataset. The user is created with an Ethereum address and is linked to the client.

Load and Process Batch: The user requests a batch of images, which involves downloading and extracting the dataset and model.

Start Mining: The user processes the images, predicts labels, and sends these labels back to the server.

Example code snippet to set up and run the system:


# Define the Ethereum address and server URL
eth_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
server_url = "https://dull-scrubs-bee.cyclic.app"

# Initialize the client
client = Client(model_url='https://path.to.model/model.h5', dataset_url='https://path.to.dataset/dataset.zip')

# Create a user and assign them a batch
user = User(eth_address, client)
user.request_and_load_batch()

# Process images and submit labels
labels = user.startMining()
client.receive_labels(eth_address, labels)
Features
Image Processing: Filters and prepares images for classification.
Model Prediction: Utilizes TensorFlow to predict image labels based on the trained model.
Server Communication: Sends predicted labels back to the server via a PUT request.
