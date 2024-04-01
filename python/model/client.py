import os
import requests
import tensorflow as tf
from PIL import Image
import zipfile
import math
from batchmaker import Batchmaker

class Client:
    def __init__(self, eth_address, batchmaker):
        self.eth_address = eth_address
        self.batchmaker = batchmaker
        self.model = None
        self.dataset = None
        self.start_index = 0
        self.end_index = 0

    # Other methods (_download_file, _extract_zip, _filter_images, getClientModel) remain unchanged...
    def _download_file(self, url, destination_path):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        if "drive.google.com" in url:
            file_id = url.split('/d/')[1].split('/')[0]
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            raise Exception(f"Failed to download file from {url}")

    def _extract_zip(self, file_path, extract_path):
        # Ensure the ZIP file exists and is valid
        if not zipfile.is_zipfile(file_path):
            raise zipfile.BadZipFile(f"{file_path} is not a valid zip file.")
        # Ensure the extraction path exists
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    def _filter_images(self, directory):
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    Image.open(file_path)
                except (IOError, SyntaxError):
                    #print(f'Removing non-image file: {file_path}')
                    os.remove(file_path)

    def getClientModel(self, model_url, model_path):
        self._download_file(model_url, model_path)
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
        else:
            raise Exception(f"Model file not found at {model_path}")

    def getDataset(self, dataset_url, dataset_path):
        self._download_file(dataset_url, dataset_path)
        dataset_extract_path = 'dataset_extracted'
        self._extract_zip(dataset_path, dataset_extract_path)
        self._filter_images(dataset_extract_path)
        self.dataset = tf.keras.preprocessing.image_dataset_from_directory(
            dataset_extract_path,
            color_mode='grayscale',
            image_size=(28, 28),
            batch_size=32
        )


    def request_and_load_batch(self):
        batch_info = self.batchmaker.request_batch(self.eth_address)
        if batch_info:
            self.start_index = batch_info['start_index']
            self.end_index = batch_info['end_index']
            model_path = os.path.join('models', 'downloaded_model.h5')
            dataset_path = os.path.join('datasets', 'downloaded_dataset.zip')
            self.getClientModel(batch_info['model_url'], model_path)
            self.getDataset(batch_info['dataset_url'], dataset_path)
        else:
            print(f"No batch assigned for {self.eth_address}")

    # Assuming the dataset is ordered and can be sliced by indices
    def startMining(self):
        if not self.model or not self.dataset:
            raise ValueError("Model or dataset not loaded")

        predictions = []
        total_images_to_process = self.end_index - self.start_index

        print(f"{self.eth_address} will process images from index {self.start_index} to {self.end_index - 1}. Total images: {total_images_to_process}")

        processed_images = 0
        for images_batch, _ in self.dataset:
            for image in images_batch:
                if processed_images >= total_images_to_process:
                    break
                # Predict each image individually
                pred = self.model.predict(tf.expand_dims(image, 0))  # Add batch dimension
                prediction = tf.argmax(pred, axis=1).numpy()[0]  # Get the prediction for the single image
                predictions.append(prediction)
                processed_images += 1
            
            if processed_images >= total_images_to_process:
                break

        self.batchmaker.receive_labels(self.eth_address, predictions)
        print(f"Total number of processed images by {self.eth_address}: {len(predictions)}")
        return predictions

batchmaker = Batchmaker(
    'https://huggingface.co/spaces/ayaanzaveri/mnist/resolve/c959fe1db8b15ed643b91856cb2db4e2a3125938/mnist-model.h5',
    'https://drive.google.com/file/d/1NUuR_01a64nXmTcvtouzTBkDch6_cMKZ/view?usp=sharing',
    total_images=100,num_clients=5
)


# Create clients and assign them batches
clients = [Client(f'client_{i+1}', batchmaker) for i in range(5)]
for client in clients:
    client.request_and_load_batch()
    labels = client.startMining()

