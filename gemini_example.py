import requests

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": "AIzaSyBiLiAIDlqzmZ6-9JA6cG9t46-EERksj3I"
}
data = {
    "contents": [
        {
            "parts": [
                {"text": "Explain how AI works in a few words"}
            ]
        }
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.json())