import base64
import csv

class Utils:
    @staticmethod
    def encode_image_to_base64(image_path):
        """
        Reads a local image file and returns its Base64-encoded string.

        :param image_path: Path to the local image file
        :return: Base64-encoded string of the image
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def create_csv_file(csv_file_name):
        """
        Creates a CSV file with headers.

        :param csv_file_name: Name of the CSV file to create
        """
        fieldnames = ['file_name', 'alt_text']
        with open(csv_file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    @staticmethod
    def save_output_to_csv(file_path, data):
        """
        Saves data to a CSV file.

        :param file_path: Path to the CSV file
        :param data: Data to write to the CSV file
        """
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["file_name", "alt_text"])
            writer.writerows(data)