from core.config import settings, BASE_DIR

print("BASE_DIR:", BASE_DIR)
print(".env 경로:", BASE_DIR / ".env")
print(".env 존재 여부:", (BASE_DIR / ".env").exists())
print("settings.OPENAI_API_KEY:", settings.OPENAI_API_KEY)
