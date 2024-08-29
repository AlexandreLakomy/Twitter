import os
from dotenv import load_dotenv
import tweepy  # type: ignore
import openai  # type: ignore
import logging

# Configurez le logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Récupération des configurations à partir des variables d'environnement
api_key = os.getenv('API_KEY')  # Vérifiez que la casse des noms correspond
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

def lambda_handler(event, context):
    try:
        # Prompt pour GPT-4
        prompt_text = "Donne-moi une information intéressante en commençant par #LeSaviezVous. L'information doit être vraie et contenir au maximum 150 caractères. Tu peux ajouter un emoji en rapport avec le message. Exemple : #LeSaviezVous Le premier café en Europe a ouvert à Venise en 1645. ☕️"
        
        logger.info("Appel à GPT-4 avec le prompt.")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )
        
        message = response['choices'][0]['message']['content'].strip()
        logger.info(f"Message généré par GPT-4 : {message}")
        
        # Publier le message sur Twitter
        client.create_tweet(text=message)
        logger.info("Tweet posté avec succès.")
        
        return {
            'statusCode': 200,
            'body': 'Tweet posted successfully!'
        }
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {e}")
        return {
            'statusCode': 500,
            'body': f"Erreur : {str(e)}"
        }