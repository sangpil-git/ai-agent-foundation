# scripts/test_chain.py
"""
체인 로컬 테스트용 스크립트.
python -m scripts.test_chain 형태로 실행 가능.
"""
from app.chains.base.chain_registry import get_chain


def main():
    EchoChain = get_chain("echo")
    echo_chain = EchoChain()
    res1 = echo_chain.invoke({"text": "체인 테스트"})
    print("EchoChain result:", res1)

    RagQAChain = get_chain("rag_qa")
    rag_chain = RagQAChain()
    res2 = rag_chain.invoke({"question": "회의실 예약 시스템 상태는?"})
    print("RagQAChain result:", res2)


if __name__ == "__main__":
    main()
