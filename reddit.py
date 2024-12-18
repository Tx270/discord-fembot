import requests

# Endpoint do wygenerowania obelgi w formacie tekstowym
# url = "https://insult.mattbas.org/api/insult"

# params = {
#     'who': "Michał Femboy eeee"
# }


# response = requests.get(url, params={ 'who': "Michał Femboy eeee" })

# if response.status_code == 200:
#     insult = response.text
#     print("Obelga:", insult)
# else:
#     print("Błąd:", response.status_code)

print(requests.get("https://v2.jokeapi.dev/joke/Dark?type=single").json()["joke"])