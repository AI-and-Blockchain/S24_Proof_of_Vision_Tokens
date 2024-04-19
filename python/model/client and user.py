import os
import requests
import tensorflow as tf
from PIL import Image
import zipfile
import math
import matplotlib.pyplot as plt
import numpy as np

# Class to handle client operations, such as managing model and dataset URLs, and tracking labels
class client:
    def __init__(self, model_url, dataset_url):
        # Initialize client with default model and dataset URLs
        self.default_model_url = model_url
        self.default_dataset_url = dataset_url
        self.batches = {}  # Dictionary to track assigned batches
        self.received_labels = {}  # Store labels received from each user

    def request_batch(self, eth_address):
        # Assign a new batch to a user if not already assigned
        if eth_address not in self.batches:
            self.batches[eth_address] = {
                'model_url': self.default_model_url,
                'dataset_url': self.default_dataset_url,
            }
        # Initialize label storage for new users
        if eth_address not in self.received_labels:
            self.received_labels[eth_address] = []
        return self.batches[eth_address]

    def receive_labels(self, eth_address, labels, requestID):
        # Convert labels to a native Python list type if necessary
        labels = labels.tolist() if isinstance(labels, np.ndarray) else labels
        labels = [int(label) if isinstance(label, np.integer) else label for label in labels]
        requestID = int(requestID)  # Ensure requestID is an integer

        self.received_labels[eth_address].extend(labels)
        print(f"Labels received for {eth_address}: {labels}")

        # Prepare data for PUT request to server
        data = {
            "requestID": requestID,
            "userEthAddress": eth_address,
            "labels": labels
        }
        # Send labels to the server
        response = requests.put("https://dull-scrubs-bee.cyclic.app/labels", json=data)
        if response.status_code == 202:
            print("Labels successfully submitted to the server.")
        else:
            print("Failed to submit labels. Response:", response.text)

# Class to handle user operations, such as downloading models and datasets, and processing images
class user:
    def __init__(self, eth_address, client):
        self.eth_address = eth_address
        self.client = client
        self.model = None
        self.dataset = None

    def _download_file(self, url, destination_path):
        # Handle file downloads, with special handling for Google Drive links
        if "drive.google.com" in url:
            file_id = url.split('/d/')[1].split('/')[0]
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url, stream=True)
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)

    def _extract_zip(self, file_path, extract_path):
        # Unzip files to the specified path
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    def _filter_images(self, directory):
        # Remove non-image files from the directory
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    Image.open(file_path)
                except (IOError, SyntaxError):
                    os.remove(file_path)

    def getuserModel(self, model_url,model_path):
        # Download and load the TensorFlow model
        self._download_file(model_url, model_path)
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)

    def getDataset(self, dataset_url,dataset_path):
        self._download_file(dataset_url, dataset_path)
        dataset_extract_path = 'dataset_extracted'
        self._extract_zip(dataset_path, dataset_extract_path)
        self._filter_images(dataset_extract_path)
        self.dataset = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_extract_path,
            color_mode='grayscale',
            image_size=(28, 28),
            batch_size=128,  # Set batch size to 100
            shuffle=False  # Disable shuffling to maintain the order
        )

    def request_and_load_batch(self):
        # Request batch info and load model and dataset
        batch_info = self.client.request_batch(self.eth_address)
        model_path = os.path.join('models', 'downloaded_model.h5')
        dataset_path = os.path.join('datasets', 'downloaded_dataset.zip')
        self.getuserModel(batch_info['model_url'], model_path)
        self.getDataset(batch_info['dataset_url'], dataset_path)

    def startMining(self, requestID):
        # Verify if both model and dataset are loaded, raise an error if not
        if not self.model or not self.dataset:
            raise ValueError("Model or dataset not loaded")

        predictions = []  # Initialize a list to hold prediction results

        # Iterate through the dataset batches
        for images_batch, _ in self.dataset:
            for image in images_batch:
                # Make a prediction on each image individually
                pred = self.model.predict(tf.expand_dims(image, 0))  # Expand dims to create a batch of one
                prediction = tf.argmax(pred, axis=1).numpy()[0]  # Get the prediction result for the image
                predictions.append(prediction)  # Store the prediction

        # Print the total number of processed images and return the predictions
        print(f"Total number of processed images by {self.eth_address}: {len(predictions)}")
        return predictions

# Example usage of the system:
address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44f"  # Define an Ethereum address for the user

# Making a GET request to retrieve batch information for the specified address
response = requests.get("https://dull-scrubs-bee.cyclic.app/batch", params={"address": address})
batch_data = response.json()  # Parse the JSON response to get batch data

# Extract model and dataset URLs and the request ID from the batch data
model_url = batch_data["modelUrl"]
dataset_url = batch_data["datasetUrl"]
requestID = batch_data["requestID"]

# Initialize the client with the model and dataset URLs obtained from the server
client = client(model_url, dataset_url)

# Create a user instance and link it to the client
single_user = user(address, client)

# Load the batch assigned to the user which includes downloading and preparing the model and dataset
single_user.request_and_load_batch()

# Start the mining process which involves image processing and label prediction
labels = single_user.startMining(requestID)

# Once labels are predicted, submit them to the server using the client's functionality
client.receive_labels(address, labels, requestID)
