import requests

try:
    response = requests.post(
        'http://127.0.0.1:8000/v1/chat/completions',
        headers={'Content-Type': 'application/json'},
        json={
            'model': 'E2B/claude-opus-4-5-20251101',
            'messages': [{'role': 'user', 'content': 'Hello, just checking if you are back online!'}],
            'stream': False
        }
    )
    print(f"Status: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Connection Error: {e}")
