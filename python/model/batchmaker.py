# batchmaker.py
import tensorflow as tf
from PIL import Image
import os
import requests
import math

class Batchmaker:
    def __init__(self, model_url, dataset_url, total_images, num_clients):
        self.default_model_url = model_url
        self.default_dataset_url = dataset_url
        self.total_images = total_images
        self.num_clients = num_clients
        self.batches = {}
        self.distribute_batches()

    def distribute_batches(self):
        images_per_client = math.ceil(self.total_images / self.num_clients)
        for i in range(self.num_clients):
            start_index = i * images_per_client
            end_index = min(start_index + images_per_client, self.total_images)
            self.batches[f'client_{i+1}'] = {
                'model_url': self.default_model_url,
                'dataset_url': self.default_dataset_url,
                'start_index': start_index,
                'end_index': end_index,
            }
            print(f"{f'client_{i+1}'} will process images from index {start_index} to {end_index - 1}.")


    def request_batch(self, eth_address):
        return self.batches.get(eth_address)

    def receive_labels(self, eth_address, labels):
        if eth_address in self.batches:
            print(f"Labels received for {eth_address}: {labels}")
        else:
            print(f"Batch not found for the provided ETH address: {eth_address}")

