# scripts/export_config_docs.py
"""
YAML 설정을 읽어 간단한 문서/리스트를 콘솔에 출력하는 예시.
"""
from app.core.config.loader import load_yaml


def main():
    models = load_yaml("models")
    prompts = load_yaml("prompts")
    tools = load_yaml("tools")

    print("# Models")
    print(models)
    print("\n# Prompts")
    print(prompts)
    print("\n# Tools")
    print(tools)


if __name__ == "__main__":
    main()
