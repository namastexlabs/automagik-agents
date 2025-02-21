import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.notion.agent import NotionAgent


def main():
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter command: ")
    agent = NotionAgent()
    result = agent.run_sync(prompt)
    print(result)


if __name__ == '__main__':
    main() 