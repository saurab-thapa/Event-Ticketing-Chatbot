import requests


def compress_prompt(api_key: str, context_text: str, user_text: str) -> tuple[str, dict]:
    url = "https://api.scaledown.xyz/compress/raw/"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "context": context_text,
        "prompt": user_text,
        "scaledown": {"rate": "auto"},
    }

    response = requests.post(url, headers=headers, json=body, timeout=45)
    response.raise_for_status()
    data = response.json()

    compressed_text = (
        data.get("compressed_prompt")
        or data.get("compressed")
        or data.get("prompt")
        or (data.get("data", {}) or {}).get("compressed_prompt")
        or (data.get("result", {}) or {}).get("compressed_prompt")
        or (data.get("output", {}) or {}).get("compressed_prompt")
    )

    if not compressed_text:
        compressed_text = user_text
        data["fallback_used"] = True

    return compressed_text, data
