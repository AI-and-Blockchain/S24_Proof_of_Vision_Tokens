# batchmaker.py
import tensorflow as tf
from PIL import Image
import os
import requests


class Batchmaker:
    def __init__(self, model_url, dataset_url):
        self.default_model_url = model_url
        self.default_dataset_url = dataset_url
        self.batches = {}

    def request_batch(self, eth_address):
        # Register the batch and return the model and dataset URLs
        if eth_address not in self.batches:
            self.batches[eth_address] = {
                'model_url': self.default_model_url,
                'dataset_url': self.default_dataset_url
            }
        return self.batches[eth_address]

    def receive_labels(self, eth_address, labels):
        # Store the labels for the ETH address
        if eth_address in self.batches:
            self.batches[eth_address]['labels'] = labels
            print(f"Labels received for {eth_address}.")
            print(f"Received labels for {eth_address}: {labels}")

        else:
            print("Batch not found for the provided ETH address.")
