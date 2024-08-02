import os
import autogen

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

llm_config = {
    "config_list": [
        {
            'model': 'meta-llama-3-70b-instruct',
            'api_key': API_TOKEN,
            'base_url': 'https://inference.friendli.ai/v1',
        }
    ],
    "timeout": 600,
    "cache_seed": 42,
    "temperature": 0
}

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },
    human_input_mode="TERMINATE"
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config
)

pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config
)

group_chat = autogen.GroupChat(
    agents=[user_proxy, coder, pm],
    messages=[],
    max_round=12
)

manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software."
)