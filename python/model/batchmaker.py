# batchmaker.py
import tensorflow as tf
from PIL import Image
import os
import requests
import math

class Batchmaker:
    def __init__(self, model_url, dataset_url):
        self.default_model_url = model_url
        self.default_dataset_url = dataset_url
        self.batches = {}
        self.received_labels = {}  # Dictionary to store labels from each client

    def request_batch(self, eth_address):
        if eth_address not in self.batches:
            self.batches[eth_address] = {
                'model_url': self.default_model_url,
                'dataset_url': self.default_dataset_url,
            }
        # Initialize the received labels list for this client
        if eth_address not in self.received_labels:
            self.received_labels[eth_address] = []
        return self.batches[eth_address]

    def receive_labels(self, eth_address, labels):
        if eth_address in self.batches:
            # Append the labels received from this client to its specific array
            self.received_labels[eth_address].extend(labels)
            print(f"Labels received for {eth_address}: {labels}")
        else:
            print(f"Batch not found for the provided ETH address: {eth_address}")



