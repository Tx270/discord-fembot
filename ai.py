import requests

def chatbot(prompt, max_tokens):
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": "Bearer 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"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": max_tokens,
            "temperature": 0.8,
            "top_p": 0.9
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result:
            return result[0]['generated_text']
        else:
            return "Brak odpowiedzi w liście"
    else:
        return f"Błąd: {response.status_code} - {response.text}"

prompt = "Michał, the most feminen of the students at the SCI technical school, was walking one night looking for someone to fuck when in the rain he encounterd a "
# prompt = "Write a haiku in the first person. The narrator is Michał from Szczecin, reflecting on his life or experiences. Ensure the haiku follows the traditional 5-7-5 syllable structure. Here is the haiku: "
# prompt = """Here is an example of a haiku:
# Silent morning light,
# Reflections on calm waters—
# Peaceful solitude.

# Here is a completly diffrent haiku: """


with open("output.txt", 'w', encoding='utf-8') as f:
    f.write(chatbot(prompt, 50))
