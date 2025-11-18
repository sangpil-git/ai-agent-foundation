
# 🧱 OpenAI 기반 프로젝트 – 초기 구축 & 개발 환경 가이드 (pyproject.toml 버전)

**OpenAI + LangChain + LangGraph 기반 AI 서비스**를 구성
Python **pyproject.toml 기반 환경** 구축

---

## 1. 📦 필수 설치 요구사항
- Python 3.11+
- Git
- (선택) Docker & Docker Compose

---

## 2. 📁 저장소 클론
```bash
git clone <repository-url>
cd project-root
```

---

## 3. 🧬 Python 가상환경 생성
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# 또는
source .venv/bin/activate        # macOS / Linux
```

---

## 4. 📥 패키지 설치 (pyproject.toml 사용)

### 🔧 프로젝트 패키지 설치
```bash
pip install .
```

또는 개발모드로 설치:
```bash
pip install -e .
```

---

## 5. 🔐 환경 변수(.env) 설정

프로젝트 루트에 `.env` 작성:

```env
OPENAI_API_KEY=your-openai-key
OPENAI_API_BASE=
OPENAI_MODEL=gpt-4.1-mini

LANGSMITH_API_KEY=
LANGSMITH_PROJECT=agent-foundation
LANGSMITH_ENDPOINT=
```

---

## 6. ⚙ OpenAI / LangChain / LangGraph 기본 초기화 코드

```python
from langchain_openai import ChatOpenAI
from core.config import settings

llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    temperature=0.2,
    openai_api_key=settings.OPENAI_API_KEY
)
```

---

## 7. ▶️ FastAPI 서버 실행

CLI 테스트 예시
```powershell
python -m app.core.llm.run_agent echo_chain "테스트"
```

서버 실행
루트에서:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
또는 pyproject.toml 에 script가 있다면:
```bash
uvicorn app.main:app --reload
```

브라우저에서 확인  
```text
http://localhost:8000/docs  (Swagger UI)  
http://localhost:8000/api/v1/health  (Health)  
http://localhost:8000/api/v1/.....
```

---

## 8. 추천 디렉터리 구조

```
project-root
├── app/
│   ├── api/
│   ├── core/
│   │    ├── config.py
│   │    ├── llm.py
│   │    ├── graph/
│   │    └── chains/
│   ├── services/
│   └── main.py
├── pyproject.toml
├── .env
└── README.md
```

현재 프로젝트 구조
``` 
project-root/
├── app/
│   ├── app.py                     # FastAPI 앱 생성(create_app) + lifespan(startup/shutdown)
│   ├── dependencies.py            # FastAPI Depends() 공통 의존성
│   │
│   ├── core/                      # 핵심 인프라 (설정, 로깅, LLM, 트레이싱 등)
│   │   ├── __init__.py
│   │   │
│   │   ├── config/                # 환경 설정, YAML 로더
│   │   │   ├── __init__.py
│   │   │   ├── settings.py        # .env 기반 환경변수 Settings
│   │   │   └── loader.py          # YAML 로딩 유틸 (models.yml / prompts.yml 등)
│   │   │
│   │   ├── logging/               # 글로벌 로깅 (structlog + 기본 logging)
│   │   │   ├── __init__.py
│   │   │   ├── logging_config.py  # LOG_LEVEL, JSON 로깅, 회전 로그
│   │   │   └── logger.py          # get_logger()
│   │   │
│   │   ├── llm/                   # 모델 제공자(Provider)별 팩토리 + 레지스트리
│   │   │   ├── __init__.py
│   │   │   ├── llm_factory.py     # OpenAI/Gemini/Claude/Azure/Ollama 자동 선택
│   │   │   ├── model_registry.py  # models.yml 기반 모델 설정
│   │   │   ├── prompt_registry.py # prompts.yml 불러오기
│   │   │   └── tool_registry.py   # tools.yml 기반 Tool 활성화/관리
│   │   │
│   │   ├── tracing/
│   │   │   ├── __init__.py
│   │   │   └── langsmith_config.py # LangSmith tracing 초기화
│   │   │
│   │   └── README.md (선택)
│   │
│   ├── graphs/                    # LangGraph 기반 Workflow (멀티 노드/워크플로우)
│   │   ├── __init__.py
│   │   ├── base_graph.py          # 공통 BaseGraph (input/output 규약)
│   │   ├── support_bot_graph.py   # 예: Q&A / RAG Bot
│   │   └── workflow_graph.py      # 예: 외부 API 기반 자동화 워크플로우
│   │
│   ├── chains/                    # LangChain Runnable 기반 단일 체인
│   │   ├── __init__.py
│   │   ├── base_chain.py          # 공통 BaseChain
│   │   ├── chain_registry.py      # 체인 자동 등록 레지스트리
│   │   ├── echo_chain.py          # 기본 Echo Chain
│   │   └── rag_qa_chain.py        # RAG Q&A Chain
│   │
│   ├── tools/                     # LLM Agent 가 호출하는 Tool 모음
│   │   ├── __init__.py            # auto-discovery (모든 툴 자동 등록)
│   │   ├── base.py                # @registered_tool 데코레이터 (LangChain tool + registry 연동)
│   │   ├── time_tools.py          # 예: 현재 시간 반환 tool
│   │   └── rag_tools.py           # RAG 검색 tool
│   │
│   ├── integrations/              # 외부 서비스 연동 (비즈니스 API)
│   │   ├── __init__.py
│   │   ├── slack_client.py        # Slack API 연동
│   │   ├── jira_client.py         # Jira API 연동
│   │   └── reservation_api.py     # 회의실 예약 시스템 연동
│   │
│   ├── rag/                       # RAG (데이터 로딩 + 벡터 스토어 + 검색)
│   │   ├── __init__.py
│   │   ├── loaders/
│   │   │   ├── api_loader.py      # REST/JSON → 문서 로더
│   │   │   ├── file_loader.py     # PDF/Word/Text 로더
│   │   │   └── image_loader.py    # OCR/이미지 캡션 로더
│   │   ├── vector_store.py        # chroma / pgvector / inmemory 추상화
│   │   └── retriever_factory.py   # RAG용 retriever 생성
│   │
│   ├── api/                       # REST API 라우터
│   │   ├── __init__.py
│   │   ├── router.py              # /api 공통 라우터
│   │   ├── v1/
│   │   │   ├── routes_graph.py    # 그래프 실행 API
│   │   │   ├── routes_chain.py    # 체인 실행 API
│   │   │   ├── routes_rag.py      # RAG 검색/인덱싱
│   │   │   ├── routes_tools.py    # 사용 가능 Tools 조회
│   │   │   └── routes_health.py   # 헬스체크
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_logging.py     # 자동 Request/Response Logging (structlog 기반)
│   │
│   ├── utils/                     # 공통 유틸
│   │   ├── __init__.py
│   │   ├── ids.py                 # uuid, short-id, request-id
│   │   ├── time.py                # now(), timestamp, duration
│   │   ├── json.py                # safe_json, pretty_json
│   │   ├── string.py              # masking, snake/camel 변환
│   │   ├── file.py                # file read/write
│   │   ├── http.py                # httpx 공통 wrapper
│   │   ├── security.py            # sha256/hmac
│   │   └── async_utils.py         # async helper (timeout 등)
│   │
│   └── __init__.py                # 패키지 초기화 (필수 로직 없음)
│
├── config/
│   ├── models.yml                 # multi-LLM 모델 설정 (OpenAI/Gemini/Claude/Azure/Ollama)
│   ├── prompts.yml                # 공통 프롬프트 템플릿
│   ├── tools.yml                  # 활성화할 tool 목록/설정
│   └── rag_sources.yml            # RAG 인덱싱 대상(파일/API)
│
├── scripts/
│   ├── ingest_rag_data.py         # RAG 인덱싱 스크립트
│   └── test_graph.py              # 개별 Graph 테스트
│
├── tests/
│   └── ...                        # 유닛/통합 테스트
│
├── .env                           # 환경 설정 (.env)
├── pyproject.toml                 # Poetry / 의존성
└── README.md
```

---

## 9. pyproject.toml 예시 (자동 포함됨)

```
[project]
name = "openai-agent-project"
version = "0.1.0"
description = "OpenAI + LangChain + LangGraph 기반 AI 서비스"
requires-python = ">=3.10"

dependencies = [
    "fastapi",
    "uvicorn",
    "python-dotenv",
    "openai>=1.0",
    "langchain",
    "langchain-openai",
    "langchain-community",
    "langgraph",
]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
```

---

## 10. 초기 점검 체크리스트
- [ ] `.env` 정상 로드 확인  
- [ ] OpenAI API 호출 테스트  
- [ ] Graph invoke 테스트  
- [ ] FastAPI `/docs` 정상 접근  

---

