import os
import autogen
import asyncio
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

financial_tasks = [
    """What are the current stock prices of NVDA and TESLA, and how is the performance over the past month in terms of percentage change?""",
    """Investigate possible reasons of the stock performance.""",
    """Plot a graph comparing the stock prices over the past month.""",
]

writing_tasks = ["""Develop an engaging blog post using any information provided."""]

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)
writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.
        Reply "TERMINATE" in the end when everything is done.
        """,
)

user = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": True,
    },
)

async def run_chats():
    chat_results = await user.a_initiate_chats(
        [
            {
                "chat_id": 1,
                "recipient": financial_assistant,
                "message": financial_tasks[0],
                "silent": False,
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 2,
                "prerequisites": [1],
                "recipient": research_assistant,
                "message": financial_tasks[1],
                "silent": False,
                "summary_method": "reflection_with_llm",
            },
            {
                "chat_id": 3,
                "prerequisites": [1],
                "recipient": financial_assistant,
                "message": financial_tasks[2],
                "silent": False,
                "summary_method": "reflection_with_llm",
            },
            {"chat_id": 4, "prerequisites": [1, 2, 3], "recipient": writer, "silent": False, "message": writing_tasks[0]},
        ]
    )
    return chat_results

if __name__ == "__main__":
    asyncio.run(run_chats())