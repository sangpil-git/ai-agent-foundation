import argparse
import asyncio

from agents import get_agent


async def _run(agent_name: str, text: str):
    agent = get_agent(agent_name)
    result = agent.invoke({"input": text})
    print(f"[{agent_name}]")
    print(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("agent_name", help="echo_chain / echo_graph / rag_chain ...")
    parser.add_argument("text", help="질문 또는 프롬프트 텍스트")
    args = parser.parse_args()

    asyncio.run(_run(args.agent_name, args.text))


if __name__ == "__main__":
    main()
