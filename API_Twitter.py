import os
from dotenv import load_dotenv
import tweepy  # type: ignore
import openai  # type: ignore

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Récupération des configurations à partir des variables d'environnement
api_key = os.getenv('API_KEY')
api_secret_key = os.getenv('API_SECRET_KEY')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Authentification Twitter avec OAuth 1.0a
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret_key,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Fonction pour obtenir une réponse de GPT-4 via OpenAI
def obtenir_message_chatgpt(prompt):
    print("Appel à GPT-4 avec le prompt :", prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print("Réponse reçue.")
    return response['choices'][0]['message']['content'].strip()

# Prompt pour GPT-4
prompt_text = "Donne-moi une information intéressante en commençant par #LeSaviezVous. L'information doit être vraie et contenir au maximum 150 caractères. Tu peux ajouter un emoji en rapport avec le message. Exemple : #LeSaviezVous Le premier café en Europe a ouvert à Venise en 1645. ☕️"
attempts = 0
max_attempts = 5
success = False

while attempts < max_attempts and not success:
    message = obtenir_message_chatgpt(prompt_text)
    print("Message généré par GPT-4 :", message)
    
    # Publier le message sur le compte automatisé
    try:
        print("Tentative de publication d'un tweet...")
        response = client.create_tweet(text=message)
        print("Tweet posté :", message)
        success = True  # Arrêter la boucle si le tweet est posté avec succès
    except tweepy.errors.TweepyException as e:
        print(f"Erreur lors de la publication sur Twitter : {e}")
        attempts += 1
        if "403 Forbidden" in str(e):
            print(f"Tentative {attempts} échouée. Nouvel essai...")
        else:
            # Pour toute autre erreur, interrompre la boucle et afficher le message
            break

if not success:
    print(f"Échec après {max_attempts} tentatives.")
