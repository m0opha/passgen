import requests
import string
import os
import json

__APP = "passgen"
__CONFIG_PATH = os.path.join(os.getenv("HOME"), ".config", __APP)
__CONFIG_FILE = os.path.join(__CONFIG_PATH,"config.json")

def createConfigDirectory():
    if os.path.exists(__CONFIG_PATH) == False:
        os.mkdir(__CONFIG_PATH)
        print("[+]Config directory has been created.")

        with open(__CONFIG_FILE, "w") as file:
            file.write('{\n"API_KEY":"",\n"MAX_VALUE":"100",\n"MIN_VALUE":"0",\n"PASS_LENGTH":"30"\n}')
            print("[+] Please setting up config.json")

def loadJson(path):
    with open(path , "r") as file:
        data = json.load(file)
    return data

def getRandomInteger(api_key, n=1, min_value=0, max_value=100):
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": n,
            "min": min_value,
            "max": max_value,
            "replacement": True
        },
        "id": 1
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["result"]["random"]["data"]
    except requests.RequestException as e:
        print(f"Error al conectarse a la API: {e}")
    except KeyError:
        print("Error al procesar la respuesta de la API.")
    return None


def main():
    createConfigDirectory()
    config = loadJson("/home/m0opha/.config/passgen/config.json")

    integer_password = getRandomInteger(api_key=config["API_KEY"],
                                        n=config["PASS_LENGTH"],
                                        min_value=config["MIN_VALUE"],
                                        max_value=config["MAX_VALUE"])
    all_characters = string.printable
    password = ""

    for _integer in integer_password:
        password += all_characters[_integer]
    
    print(password)

if __name__ == "__main__":
    main()
