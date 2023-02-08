import openai
import requests
import logging
from settings import open_AI_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

key = open_AI_settings.key

openai.organization = "org-PBv1I8A5NaoSiPDTloTOKS9J"
openai.api_key = key

openai.Model.list()

logger.info("OpenAI connected")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {}".format(key)
}


def get_response(prompt):
    data = {"model": "text-davinci-003",
            "prompt": f"how old is a?",
            "temperature": 0,
            "max_tokens": 7
            }
    a = requests.post('https://api.openai.com/v1/completions', headers=headers,
                      json={"model": "text-davinci-003", "prompt": f"how old is {prompt}?", "temperature": 0,
                            "max_tokens": 10}).json()
    logger.info(f"Response from openAI: {a}")
    try:
        age = [i for i in a["choices"][0]["text"].split(" ") if i.isdigit()][0]
        name = [i for i in a["choices"][0]["text"].split("is")][0]
        res1 = f"{name}is {age} years old"
        return res1
    except (IndexError, KeyError):
        try:
            b = requests.post('https://api.openai.com/v1/completions', headers=headers,
                              json={"model": "text-davinci-003",
                                    "prompt": f"I'm trying to figure out how old is {prompt}, he is a famous person, "
                                              f"but I might have got the name wrong. Who else can it be - can you give "
                                              f"me three names? Just the names, no explanation",
                                    "temperature": 0,
                                    "max_tokens": 30}).json()
            res2 = [i[3:] for i in (b["choices"][0]["text"].split("\n")[2:]) ]
            return res2
        except IndexError:
            return None


# print(get_response("devid"))
