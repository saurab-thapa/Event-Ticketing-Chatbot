import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("OPENROUTER_MODEL", "stepfun/step-3.5-flash:free")
scaledown_api_key = os.getenv("SCALEDOWN_API_KEY", "")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
