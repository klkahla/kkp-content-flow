import base64
import csv
import re

class Utils:
    @staticmethod
    def extract_prompt_from_api(data):
        prompt_message = data.get("prompt_message", "")
        csv_file_path = data.get("csv_file_path", None)

        concatenated_alt_text = ""

        if csv_file_path:
            try:
                with open(csv_file_path, mode='r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    alt_texts = [row['alt_text'] for row in csv_reader]
                    concatenated_alt_text = " ".join(alt_texts)
            except Exception as e:
                return {"error": str(e)}

        if concatenated_alt_text:
            prompt_message += (
                "\n\n" 
                "I have provided you a pictorial timeline generated from the image's alt-text. You must use this descriptive timeline and details to improve the content.\n\n"
                "***** TIMELINE OF IMAGES USING ALT-TEXT *****\n\n" 
                f"{concatenated_alt_text}\n\n"
                "****************************************"
                "\n\n"
            )
        print("Final prompt message: ", prompt_message)
        return prompt_message
        

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

    @staticmethod
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]