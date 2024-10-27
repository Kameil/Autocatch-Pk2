#bot.py url
boturl = "https://raw.githubusercontent.com/Kameil/Autocatch-Pk2/main/bot.py"


import requests, subprocess, os

bot_path = os.path.join(os.path.dirname(__file__), "bot.py")

# atualizar/baixar o bot.py
response = requests.get(boturl)
if response.status_code == 200:
    with open("bot.py", "w", encoding="utf-8") as file:
        file.write(response.text)
else:
    raise("deeu bom nao")


# iniciar o autocatch
if __name__ == "__main__":
    subprocess.run(["python", bot_path], check=True)
