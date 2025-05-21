from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


##################
# Drink Advisory #
##################
def get_drink_recommendation(vibe, preferences, drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_vk_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Barkeeper-Experte und hilfst Nutzern, passende Getränke auszuwählen. "
                "Berücksichtige Stimmung, Präferenzen und vorhandene Zutaten. Gib Zutaten in ml und Preis an. "
                "Verwende nur kombinierbare Zutaten. "
                "Shots = 25ml, LongDrinks = 50ml (2 Einheiten), stark = 75ml (3 Einheiten). "
                "Keine ganzen Flaschen (330ml), außer es passt wirklich gut. "
                "Format: JSON → {\"name\": \"...\", \"zutaten\": [\"...\"], \"preis\": \"...\", \"Empfehlungstext\": \"...\"}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Stimmung: {vibe}\n"
                f"Präferenzen: {', '.join(preferences) or 'keine'}\n"
                f"Zutaten:\n{drink_list}\n"
                "Welchen Drink empfiehlst du? Bitte mit Begründung und im genannten JSON-Format."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content


def validate_drink_inquiry(inquiry, drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_vk_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Gib die Antwort ausschließlich als JSON zurück. Beginne direkt mit { und gib keine Erklärung oder sonstigen Text. "
                "Wenn das angefragte Getränk nicht möglich ist, gib eine passende Alternative – aber immer rein als JSON im Format: "
                "{\"name\": \"...\", \"zutaten\": [\"...\"], \"preis\": \"...\", \"Empfehlungstext\": \"...\"}"
                "Format: {\"name\": \"...\", \"zutaten\": [\"...\"], \"preis\": \"...\", \"Empfehlungstext\": \"...\"} "
                "Falls nicht möglich, mache eine realistische Alternative mit diesem Format."
            )
        },
        {
            "role": "user",
            "content": (
                f"Verfügbare Zutaten:\n{drink_list}\n"
                f"Gewünschtes Getränk: {inquiry}\n"
                "Ist es möglich? Wenn ja, gib Zubereitung und Preis an. Wenn nein, nenne eine gute Alternative im JSON-Format."
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content


def create_example_drinks(drinks):
    import re

    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_vk_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Barkeeper. Gib ein **reines JSON-Array** zurück, das folgendermaßen aussieht – "
                "ohne Einleitung, Erklärung oder Markdown:\n"
                "[\n"
                "  { \"name\": \"Drinkname\", \"preis\": \"4.50€\", \"alk\": \"mittel\", \"zutaten\": [\"Zutat A - 50ml\", \"Zutat B - 200ml\"] },\n"
                "  ...\n"
                "]\n"
                "Antworte ausschließlich mit diesem Array. Kein Text davor oder danach!"
            )
        },
        {
            "role": "user",
            "content": (
                f"Hier ist die Liste an verfügbaren Drinks:\n{drink_list}\n"
                "Was kannst du daraus vorschlagen?"
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    raw_text = response.choices[0].message.content.strip()

    # Versuche JSON-Array aus der Antwort zu extrahieren
    match = re.search(r'\[\s*{.*}\s*\]', raw_text, re.DOTALL)
    if not match:
        raise ValueError(f"❌ Kein JSON-Array erkannt:\n{raw_text}")

    try:
        drinks_json = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON Parse Error: {e}\nAuszug:\n{match.group(0)}")

    return drinks_json
