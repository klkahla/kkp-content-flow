class MultiAgentRepository:
    def __init__(self, model):
        self.model = model

    def get_content(self, prompt_message):
        response = self.model.invoke(execute_task_prompt.invoke(input=prompt_message))
        return response.content
