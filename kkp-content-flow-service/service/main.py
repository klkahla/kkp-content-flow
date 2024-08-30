import csv
import os
import time
import threading
import queue
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .utils.utils import Utils
from .network.api_service import ApiService
from .repository.alt_text_repository import AltTextRepository


def create_app():
    app = FastAPI()

    # Define the origins that should be allowed to make requests to this API
    origins = [
        "http://localhost:3000",
        # Add other origins as needed
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()

@app.post("/content-workflow")
async def get_content_workflow(request: Request):
    data = await request.json()
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
        
    print(f"Concatenated alt text: {concatenated_alt_text}")

    if concatenated_alt_text:
        prompt_message += (
            "\n\n" 
            "I have provided you a timeline of images using alt-text. You may use this additional descriptive information as you see fit to improve the content.\n\n"
            "***** TIMELINE OF IMAGES USING ALT-TEXT *****\n\n" 
            f"{concatenated_alt_text}\n\n"
            "****************************************"
            "\n\n"
        )

    execute_task_prompt = PromptTemplate(
        template="""`{input}`.

        Perform the task by understanding the problem, the target client, and being innovative. Write a detailed response and when confronted with choices, make a 
        decision yourself with reasoning.

        You must do well or I won't be able to book any more weddings and my business will die. 
        I will tip you $34082 for better results.
        """,
        input_variables=["input"],
    )

    model = ChatOpenAI(model="gpt-4o-mini")
    response = model.invoke(execute_task_prompt.invoke(input=prompt_message))
    print(response.content)

    return response

@app.get("/alt-text")
async def get_alt_text(directory_path: str, keywords: Optional[str] = None):
    start_time = time.time()

    csv_file_name = "AltTextAI_SEO_Output.csv"
    csv_file_path = directory_path + "/" + csv_file_name

    api_key = os.getenv("ALTTEXTSEO_API_KEY")
    api_url = 'https://alttext.ai/api/v1/images'
    
    api_service = ApiService(api_key)
    alt_text_repository = AltTextRepository(api_service, api_url)

    Utils.create_csv_file(csv_file_path)

    output_data = []

    q = queue.Queue()
    num_threads = 4
    threads = []

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(q, alt_text_repository, output_data, keywords))
        t.start()
        threads.append(t)

    try:
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.jpg'):
                    file_path = os.path.join(root, file)
                    print(f"Processing {file_path}")
                    q.put(file_path)

        q.join()

        for i in range(num_threads):
            q.put(None)
        for t in threads:
            t.join()
            
        # Sort the output data based on the filenames
        output_data.sort(key=lambda x: Utils.natural_sort_key(x[0]))

        # Save the sorted data to the CSV file
        Utils.save_output_to_csv(csv_file_path, output_data)

    except Exception as e:
        print(f"An error occurred while iterating over the directory: {e}")
        return {"error": str(e)}

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Time taken to process get_alt_text: {elapsed_time:.2f} seconds")

    response = {
        "csv_file_path": csv_file_path
    }
    return response

def worker(q, alt_text_repository, output_data, keywords):
    while True:
        file_path = q.get()
        if file_path is None:
            break
        try:
            encoded_file_path = Utils.encode_image_to_base64(file_path)
            response = alt_text_repository.create_image(encoded_file_path, keywords)
            print(response)
            if response and 'alt_text' in response:
                output_data.append((os.path.basename(file_path), response['alt_text']))
            else:
                print(f"Failed to get alt_text for {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        q.task_done()