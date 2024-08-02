import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

config_list = [
    {
        'model': 'meta-llama-3-8b-instruct',
        'api_key': API_TOKEN,
        'base_url': 'https://inference.friendli.ai/v1',
    }
]

llm_config = {
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="Chief technical officer of a tech company"
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Write python code to output numbers 1 to 100, and then store the code in a file
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)

task2 = """
Change the code in the file you just created to instead output numbers 1 to 200
"""

user_proxy.initiate_chat(
    assistant,
    message=task2
)