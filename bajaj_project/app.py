from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import math
import requests
import os
import re

app = FastAPI()

OFFICIAL_EMAIL = "gauri3822.beai23@chitkara.edu.in"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def fibonacci(n: int) -> List[int]:
    if n < 0 or n > 1000:
        raise ValueError("Invalid fibonacci range")
    a, b = 0, 1
    res = []
    for _ in range(n):
        res.append(a)
        a, b = b, a + b
    return res

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def lcm_list(arr: List[int]) -> int:
    if not arr:
        raise ValueError("Empty list")
    lcm_val = arr[0]
    for i in arr[1:]:
        lcm_val = abs(lcm_val * i) // math.gcd(lcm_val, i)
    return lcm_val

def hcf_list(arr: List[int]) -> int:
    if not arr:
        raise ValueError("Empty list")
    hcf = arr[0]
    for i in arr[1:]:
        hcf = math.gcd(hcf, i)
    return hcf

def ask_ai(question: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("AI key missing")

    if len(question.strip()) == 0 or len(question) > 500:
        raise ValueError("Invalid AI question")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-pro:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }

    r = requests.post(url, json=payload, timeout=10)
    if r.status_code != 200:
        raise RuntimeError("AI API failure")

    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]

    match = re.search(r"\b[A-Za-z]+\b", text)
    if not match:
        raise RuntimeError("Invalid AI response")

    return match.group(0)


@app.get("/health")
def health():
    return {
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }

@app.post("/bfhl")
def bfhl(payload: Dict[str, Any]):

    if not isinstance(payload, dict) or len(payload) != 1:
        raise HTTPException(status_code=400, detail="Payload must contain exactly one key")

    key = list(payload.keys())[0]
    value = payload[key]

    try:
        if key == "fibonacci":
            if not isinstance(value, int):
                raise ValueError
            data = fibonacci(value)

        elif key == "prime":
            if not isinstance(value, list):
                raise ValueError
            nums = [int(x) for x in value]
            if len(nums) > 1000:
                raise ValueError
            data = [x for x in nums if is_prime(x)]

        elif key == "lcm":
            if not isinstance(value, list):
                raise ValueError
            nums = [int(x) for x in value]
            data = lcm_list(nums)

        elif key == "hcf":
            if not isinstance(value, list):
                raise ValueError
            nums = [int(x) for x in value]
            data = hcf_list(nums)

        elif key == "AI":
            if not isinstance(value, str):
                raise ValueError
            data = ask_ai(value)

        else:
            raise HTTPException(status_code=400, detail="Invalid key")

        return {
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": data
        }

    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid input format")

    except RuntimeError:
        raise HTTPException(status_code=500, detail="Internal processing error")

    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")
