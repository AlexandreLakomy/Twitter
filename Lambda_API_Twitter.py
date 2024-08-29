import os
from dotenv import load_dotenv
import tweepy  # type: ignore
import openai  # type: ignore

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Récupération des configurations à partir des variables d'environnement
api_key = os.getenv('api_key')
api_secret_key = os.getenv('api_secret_key')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
openai_api_key = os.getenv('openai_api_key')
openai.api_key = openai_api_key

# Authentification Twitter avec OAuth 1.0a
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret_key,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def lambda_handler(event, context):
    # Votre logique de traitement ici
    try:
        # Exemple : Générer un tweet
        prompt_text = "Le Saviez-vous ? ..."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )
        message = response['choices'][0]['message']['content'].strip()
        client.create_tweet(text=message)
        return {
            'statusCode': 200,
            'body': 'Tweet posted successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

