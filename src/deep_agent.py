from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from src.prompts import RESEARCHER_INSTRUCTIONS, SUBAGENT_USAGE_INSTRUCTIONS, TODO_USAGE_INSTRUCTIONS, \
    FILE_USAGE_INSTRUCTIONS
from src.state import DeepAgentState
from src.tools.delegate_task import _create_delegation_tool, SubAgent
from src.tools.file_sys import ls, read_file, write_file
from src.tools.research import tavily_search, think_tool, get_today_str
from src.tools.todo import write_todos, read_todos
from src.utils import format_messages

# Create agent using create_agent directly
model = init_chat_model(model="openai:gpt-4o-mini", temperature=0.0)

# Limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Tools
sub_agent_tools = [tavily_search, think_tool]
built_in_tools = [ls, read_file, write_file, write_todos, read_todos, think_tool]

# Create research sub-agent
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": ["tavily_search", "think_tool"],
}

research_sub_agent = SubAgent(**research_sub_agent)

# Create task tool to delegate tasks to sub-agents
delegate_task_tool = _create_delegation_tool(
    sub_agent_tools, [research_sub_agent], model, DeepAgentState
)

delegation_tools = [delegate_task_tool]
all_tools = sub_agent_tools + built_in_tools + delegation_tools  # search available to main agent for trivial cases

# Build prompt
SUBAGENT_INSTRUCTIONS = SUBAGENT_USAGE_INSTRUCTIONS.format(
    max_concurrent_research_units=max_concurrent_research_units,
    max_researcher_iterations=max_researcher_iterations,
    date=datetime.now().strftime("%a %b %-d, %Y"),
)

INSTRUCTIONS = (
    "# TODO MANAGEMENT\n"
    + TODO_USAGE_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + "# FILE SYSTEM USAGE\n"
    + FILE_USAGE_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + "# SUB-AGENT DELEGATION\n"
    + SUBAGENT_INSTRUCTIONS
)

# Create agent
agent = create_agent(
    model, all_tools, system_prompt=INSTRUCTIONS, state_schema=DeepAgentState
)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run the deep agent with a question.")
    parser.add_argument("question", nargs="?", default="Give me an overview of Model Context Protocol (MCP).",
                        help="The question to ask the agent.")
    args = parser.parse_args()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": args.question,
                }
            ],
        }
    )

    format_messages(result["messages"])


if __name__ == "__main__":
    main()

