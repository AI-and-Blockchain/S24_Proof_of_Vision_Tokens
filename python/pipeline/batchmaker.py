# batchmaker.py
import tensorflow as tf
from PIL import Image
import os
import requests
import math
from classes import PipelineRequest

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

    '''
    Russell Note:
    I'm not sure how this works. From my perspective, this needs two things:
    1. a way to generate a new batch from a PipelineRequest object
    2. a way to turn this into a format that the workers will receive
        It will return this object to be sent to the worker via the worker calling GET /batch
        This will also save the worker's address in the PipelineRequest object

    I don't know if you have this right now.
    '''