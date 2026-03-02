from deepagents import create_deep_agent

from src.deep_agent import sub_agent_tools, model, INSTRUCTIONS
from src.prompts import RESEARCHER_INSTRUCTIONS
from src.tools.delegate_task import SubAgent
from src.tools.research import get_today_str, tavily_search, think_tool
from src.utils import format_messages

# Create research sub-agent
research_sub_agent_2 = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": [tavily_search, think_tool],
}

agent = create_deep_agent(  # updated
    tools=sub_agent_tools,
    system_prompt=INSTRUCTIONS,
    subagents=[SubAgent(**research_sub_agent_2)],
    model=model,
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