from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


##################
# Drink Advisory #
##################
# Drink example on vibe and preferences #
def get_drink_recommendation(vibe, preferences, drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Barkeeper-Experte und hilfst Nutzern, passende Getränke auszuwählen. "
                "Berücksichtige dabei die Stimmung, die Präferenzen und eine Liste an vorhandenen Drinks mit Preis. "
                "Gebe die Getränke-Zutaten in ml an und den dazugehörigen Preis. Achte darauf, nur Getränke vorzuschlagen, "
                "die mit den gegebenen Zutaten zubereitet werden können."
            )
        },
        {
            "role": "user",
            "content": (
                f"Meine Stimmung ist: {vibe}\n"
                f"Meine Präferenzen sind: {', '.join(preferences) or 'keine'}\n"
                f"Hier ist die Liste an verfügbaren Drinks:\n{drink_list}\n"
                "Welchen Drink empfiehlst du, gebe mir ein kurze Begründung warum?"
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content

# Freetext Drink prove #
def validate_drink_inquiry(inquiry, drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Barkeeper-Experte und hilfst Nutzern, passende Getränke auszuwählen."
                "Gebe die Getränke-Zutaten in ml an und den dazugehörigen Preis. Achte darauf, nur Getränke vorzuschlagen, "
                "die mit den gegebenen Zutaten zubereitet werden können."
            )
        },
        {
            "role": "user",
            "content": (
                f"Hier ist die Liste an verfügbaren Drinks der Bar:\n{drink_list}\n"
                f"Folgendes getränk möchte ich zubereitet bekommen:\n{inquiry}\n"
                "Kannst du mir sagen ob das möglich ist und welche zutaten du dafür verwenden würdest, gebe mir ml und Preis an."
                "Falls keine Zubereitung möglich ist dann gebe mir doch bitte eine Alternative anhand der gegebenen Liste."

            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content


# Tinder Swipe Drinks #
def create_example_drinks(drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein professioneller Barkeeper. "
                "Du erhältst eine Liste verfügbarer Zutaten und sollst daraus maximal 8 passende Drinks vorschlagen, "
                "die sich ausschließlich aus diesen Zutaten herstellen lassen.\n\n"
                "Deine Antwort besteht ausschließlich aus einem JSON-ähnlichen Array von Objekten im folgenden Format "
                "(keine Einleitung oder Erklärung davor oder danach!):\n\n"
                "[\n"
                "  { \"name\": \"Drinkname\", \"preis\": \"X€\", \"alk\": \"leicht|mittel|stark|alkoholfrei\", \"zutaten\": [\"Zutat A - 5ml\", \"Zutat B - 200ml\"] },"
                "  ...\n"
                "]\n\n"
                "Wähle realistische Namen und ordne jedem Drink ein ungefähres Alkohollevel zu. "
                "Der Preis ist errechnet durch den Verkaufspreis in Euro, basierend auf den Zutaten. welche dir gegeben werden"
                "Wähle bitte nur getränkemischung welche du als schmackhaft bzw. sinnvoll erachten würdest."
                "Achte immer darauf das deine antwort ein optimal zu parsendes JSON Objekt ist!"
            )
        },
        {
            "role": "user",
            "content": (
                f"Hier ist die Liste an verfügbaren Drinks der Bar:\n{drink_list}\n"
                "Welche Drinks kannst du mir daraus vorschlagen?"
            )
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=400
    )
    
    raw_text = response.choices[0].message.content.strip()

    try:
        # Parsen von GPT-Text zu Python-Objekt
        drinks_json = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Fehler beim Parsen des GPT-Outputs: {e}\nGPT-Antwort:\n{raw_text}")

    return drinks_json