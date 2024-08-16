import csv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

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

        Perform the task by understanding the problem, the target client, and being smart
        and efficient. Write a detailed response and when confronted with choices, make a 
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