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
                "Berücksichtige dabei die Stimmung, die Präferenzen und eine Liste an vorhandenen Drinks mit Preis. "
                "Gebe die Getränke-Zutaten in ml an und den dazugehörigen Preis. Achte darauf, nur Getränke vorzuschlagen, "
                "die mit den gegebenen Zutaten zubereitet werden können. Mische bitte keinen Flaschen (330ml) außer wenn du der Überzeugung bist das es richtig gut passt"
                "Shots sind 25ml und LongDrinks bitte mit 50ml angeben (2 Einheiten), das heißt alle Mischgetränke haben mind. 50ml Alkohol wie 9 Mile o. ä. bei starken Getränken, können es auch mal 75ml, also 3 Einheiten sein."
                "Als Beispiel Coca Cola 200ml (0.50€) + Captain Morgan 50ml (4€) = Captain Cola 4.50€" "Als Beispiel Coca Cola 200ml (0.50€) + Captain Morgan 50ml (4€) = Captain Cola 4.50€"
                "Halte die Getränkemenge immer ungefähr bei 330ml, gehe nicht höher."
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


def validate_drink_inquiry(inquiry, drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_vk_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
    ])

    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Barkeeper-Experte und hilfst Nutzern, passende Getränke auszuwählen. "
                "Gebe die Getränke-Zutaten in ml an und den dazugehörigen Preis. Achte darauf, nur Getränke vorzuschlagen, "
                "die mit den gegebenen Zutaten zubereitet werden können.Mische bitte keinen Flaschen (330ml) außer wenn du der Überzeugung bist das es richtig gut passt"
                "Shots sind 25ml und LongDrinks bitte mit 50ml (2 Einheiten), das heißt alle Mischgetränke haben mind. 50ml Alkohol wie 9 Mile o. ä. angeben, bei starken Getränken, können es auch mal 75ml, also 3 Einheiten sein."
                "Als Beispiel Coca Cola 200ml (0.50€) + Captain Morgan 50ml (4€) = Captain Cola 4.50€"
            )
        },
        {
            "role": "user",
            "content": (
                f"Hier ist die Liste an verfügbaren Drinks der Bar:\n{drink_list}\n"
                f"Folgendes Getränk möchte ich zubereitet bekommen:\n{inquiry}\n"
                "Kannst du mir sagen, ob das möglich ist und welche Zutaten du dafür verwenden würdest? Gib mir ml und Preis an. "
                "Falls keine Zubereitung möglich ist, dann gib mir bitte eine Alternative anhand der gegebenen Liste."
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


def create_example_drinks(drinks):
    drink_list = "\n".join([
        f"- {d['name']} ({d['ml_pro_vk_einheit']}ml, {d['vk_preis']:.2f}€)" for d in drinks
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
                "Der Preis ist errechnet durch den Verkaufspreis in Euro, basierend auf den Zutaten. "
                "Wähle bitte nur Getränkemischungen, die du als schmackhaft bzw. sinnvoll erachtest. "
                "Achte immer darauf, dass deine Antwort ein optimal zu parsenden JSON-Block darstellt! Mische bitte keinen Flaschen (330ml) außer wenn du der Überzeugung bist das es richtig gut passt"
                "Shots sind 25ml und LongDrinks bitte mit 50ml (2 Einheiten) angeben, das heißt alle Mischgetränke haben mind. 50ml Alkohol wie 9 Mile o. ä. bei starken Getränken, können es auch mal 75ml, also 3 Einheiten sein."
                "Als Beispiel Coca Cola 200ml (0.50€) + Captain Morgan 50ml (4€) = Captain Cola 4.50€"
                "Halte die Getränkemenge immer ungefähr bei 330ml, gehe nicht höher."
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
        drinks_json = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Fehler beim Parsen des GPT-Outputs: {e}\nGPT-Antwort:\n{raw_text}")

    return drinks_json
