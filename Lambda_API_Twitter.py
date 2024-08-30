import os
from dotenv import load_dotenv
import tweepy  # type: ignore
import openai  # type: ignore
import random
import logging

# Configurez le logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Charge les variables d'environnement du fichier .env
load_dotenv()

# Récupération des configurations à partir des variables d'environnement
api_key = os.getenv('API_KEY')  # Assurez-vous que la casse des noms correspond
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

# Liste des sujets
sujet = [
    "Intelligence", "Climat", "Espace", "Trou", "Médecine", "Robotique", "Énergie", "Réalité", 
    "Exoplanètes", "Biotechnologie", "Méditation", "Alimentation", "Sommeil", "Réseaux", "Stress", 
    "Régime", "Pleine", "Sédentarité", "Fitness", "Pollution", "Droits", "Diversité", "Mondialisation", 
    "Mouvements", "Immigration", "Médias", "Religion", "Éducation", "Famille", "Technologie", 
    "Guerre", "Révolution", "Superpuissance", "Conflits", "Colonisation", "Froid", "Décolonisation", 
    "Politique", "Démocratie", "Routes", "Numérique", "Littérature", "Culture", "Écrivains", 
    "Musique", "Photographie", "Bandes", "Art", "Création", "Start-up", "Collaborative", 
    "Crypto-monnaies", "Travail", "Crises", "Social", "Marchés", "Circulaire", "Biodiversité", 
    "Déforestation", "Renouvelables", "Recyclage", "Eau", "Solutions", "Espèces", "Agriculture", 
    "Urbanisation", "Parcs", "Technologie", "Intelligence Artificielle", "Blockchain", "Nanotechnologie", 
    "Cybersécurité", "Big Data", "Internet des Objets", "Réalité Virtuelle", "Réalité Augmentée", "5G", 
    "Quantum Computing", "Éthique", "Science des données", "Drones", "Automatisation", "Fintech", 
    "Edtech", "Biométrie", "Surveillance", "Médias Sociaux", "Cybercriminalité", "Réseautage", "Algorithmes", 
    "Conservation", "Océanographie", "Biologie", "Astronomie", "Chimie", "Physique", "Mathématiques", 
    "Génétique", "Microbiologie", "Écologie", "Zoologie", "Botanique", "Astrophysique", "Géologie", 
    "Climatologie", "Météorologie", "Vulcanologie", "Séismologie", "Hydrologie", "Astronautique", 
    "Planétologie", "Origines de la vie", "Espace-temps", "Évolution", "Écologie urbaine", "Géopolitique", 
    "Environnement", "Changement climatique", "Sociologie", "Anthropologie", "Psychologie", "Philosophie", 
    "Histoire", "Archéologie", "Linguistique", "Théologie", "Mythologie", "Folklore", "Gastronomie", 
    "Vin", "Café", "Chocolat", "Cuisine moléculaire", "Cuisine internationale", "Recettes", "Boulangerie", 
    "Pâtisserie", "Nutrition", "Végétarisme", "Véganisme", "Superaliments", "Santé mentale", "Thérapie", 
    "Yoga", "Pilates", "Crossfit", "Marathon", "Randonnée", "Cyclisme", "Natation", "Plongée", 
    "Surf", "Ski", "Snowboard", "Escalade", "Alpinisme", "Football", "Basketball", "Tennis", 
    "Golf", "Cricket", "Rugby", "Baseball", "Athlétisme", "Escrime", "Arts martiaux", "Boxe", 
    "Danse", "Théâtre", "Cinéma", "Animation", "Documentaires", "Séries télévisées", "Comédie", 
    "Drame", "Science-fiction", "Fantasy", "Horreur", "Thriller", "Mystère", "Romance", "Aventure", 
    "Musique classique", "Jazz", "Blues", "Rock", "Pop", "Hip-hop", "Électronique", "Reggae", 
    "Folk", "Country", "Méditation sonore", "Instruments de musique", "Orchestre", "Chant", 
    "Improvisation", "Composition", "Paroles", "Poésie", "Impression 3D", "Technologies spatiales", 
    "Technologies vertes", "Écosystèmes marins", "Bioacoustique", "Éthologie", "Paléontologie", 
    "Bioluminescence", "Immunologie", "Psychologie positive", "Neurosciences", "Médecines alternatives", 
    "Méditation en pleine conscience", "Études de genre", "Minorités culturelles", "Cyberpsychologie", 
    "Pop culture", "Calligraphie", "Art minimaliste", "Photographie de rue", "Art de la performance", 
    "Design interactif", "Civilisations anciennes", "Routes de la soie", "Exploration polaire", 
    "Monuments historiques", "Cartographie", "Économie circulaire", "Entrepreneuriat social", 
    "Marketing numérique", "Finance durable", "Innovation ouverte", "Eco-tourisme", "Exploration sous-marine", 
    "Cultures indigènes", "Aventures extrêmes", "Récupération et DIY", "Design intérieur", 
    "Astuces de jardinage", "Livres à succès", "Photographie amateur", "Apprentissage en ligne", 
    "Coaching de vie", "Langues rares", "Écriture créative", "Habitudes de productivité", 
    "Technospace et santé", "Réalité mixte", "Art numérique", "Art de rue", "Art contemporain", 
    "Galeries", "Musées", "Critique d'art", "Collections d'art", "Art urbain", "Art tribal", 
    "Art ancien", "Restauration d'art", "Plantes médicinales", "Insectes", "Cryptozoologie", 
    "Théories du complot", "Utopies et dystopies", "Space opera", "Cyberpunk", "Steampunk", 
    "Réalité alternative", "Voyage dans le temps", "Alchimie", "Symbolisme", "Hermétisme", 
    "Astrologie", "Tarot", "Numérologie", "Mythes modernes", "Ovnis", "Paranormal", "Fantômes", 
    "Psychokinésie", "Télépathie", "Hypnose", "Métaphysique", "Synchronicité", "Effet placebo", 
    "Miracles", "Légendes urbaines", "Science-fiction classique", "Bioingénierie", "Biomatériaux", 
    "Origami et mathématiques", "Automates et poupées", "Jouets et jeux anciens", "Kitesurf", 
    "Vol en wingsuit", "Moto-cross", "Spéléologie", "Arts du cirque", "Jonglage", "Acrobatie", 
    "Magie", "Hypnotisme de scène", "Parcs d'attractions", "Escape games", "Jeux de rôle grandeur nature", 
    "Cosplay", "Super-héros", "Dessins animés", "Webtoons", "Mèmes Internet", "Viral marketing", 
    "Vlog", "Streaming", "Podcasters célèbres", "Écriture de blog", "Marketing d'influence", 
    "Marques personnelles", "Branding et identité", "Packaging créatif", "Design de produits", 
    "Design de meubles", "Art mural", "Pictogrammes et iconographie", "Typography", 
    "Calligraphie arabe", "Manuscrits anciens", "Codex et rouleaux", "Musique médiévale", 
    "Musique baroque", "Opéra", "Ballet", "Comédie musicale", "Théâtre de marionnettes", 
    "Théâtre d'ombres", "Performance expérimentale", "Art sonore", "Synthétiseurs analogiques", 
    "Thérapie par la musique", "Thérapie par l'art", "Thérapie animale", "Danse-thérapie", 
    "Sophrologie", "Réflexologie", "Aromathérapie", "Lithothérapie", "Feng Shui", "Géométrie sacrée", 
    "Éveil spirituel", "Retraites spirituelles", "Journées mondiales", "Innovations scientifiques", 
    "Éducation inclusive", "Égalité des sexes", "Droit des animaux", "Anthropocène", 
    "Extinction des espèces", "Zones de guerre", "Accords internationaux", "Diplomatie numérique", 
    "Cyber-guerre", "Défense de l'environnement", "Justice climatique", "Droits des réfugiés", 
    "Déplacements climatiques", "Résilience communautaire", "Crise de l'eau", "Pollution plastique", 
    "Microplastiques", "Plastique biodégradable", "Nanoplastiques", "Cultures vivrières", 
    "Sécurité alimentaire", "Fermes verticales", "Agriculture biologique", "Micro-agriculture", 
    "Élevage durable", "Produits de la mer durables", "Régime alimentaire planétaire", 
    "Insectes comestibles", "Protéines alternatives", "Fermentation", "Chimie alimentaire", 
    "Nutrition fonctionnelle", "Biomarqueurs", "Alimentation de précision", "Apprentissage tout au long de la vie", 
    "Apprentissage adaptatif", "Micro-certifications", "Compétences transversales", 
    "Compétences du 21ème siècle", "Jeux vidéo éducatifs", "Robotique éducative", "Éducation STEM", 
    "Fab Labs", "Ateliers de créativité", "Design thinking", "Modèles mentaux", "Cartographie des idées", 
    "Note-taking", "Apprentissage accéléré", "Espace d'innovation", "Hackathons", 
    "Collaboration interdisciplinaire", "Culture d'innovation", "Leadership innovant", 
    "Écosystèmes d'innovation", "Recherche et développement", "Transfert de technologie", 
    "Intrapreneuriat", "Entrepreneuriat féminin", "Entrepreneuriat vert", "Entrepreneuriat numérique", 
    "Croissance exponentielle", "Marché des nouvelles technologies", "Intelligence économique", 
    "Politique industrielle", "Robotique collaborative", "Cobotique", "Exosquelettes", "IA explicable", 
    "Apprentissage automatique", "Reconnaissance de la parole", "Vision par ordinateur", "Biohacking", 
    "Cyborgs", "Nanorobots", "CRISPR et génétique", "Édition de gènes", "Thérapie génique", 
    "Bio-impression", "Organes artificiels", "Médecine personnalisée", "Pharmacogénomique", 
    "Médecine régénérative", "Immunothérapie", "Biopharmacie", "Biocapteurs", "Biomarqueurs liquides", 
    "Génétique de la population", "Épidémiologie génétique", "Microbiome humain", "Bioremédiation", 
    "Technologies de dépollution", "Captage et stockage du carbone", "Énergie nucléaire de nouvelle génération", 
    "Fusion nucléaire", "Batteries de nouvelle génération", "Piles à hydrogène", "Hydrogène vert", 
    "Captage de l'énergie des vagues", "Parcs éoliens offshore", "Solaire spatial", "Réseaux électriques intelligents", 
    "Internet de l'énergie", "Mobilité électrique", "Villes intelligentes", "Bâtiments autonomes", 
    "Infrastructures résilientes", "Gestion de l'eau urbaine", "Parcs urbains", "Agriculture urbaine", 
    "Toits verts", "Couloirs écologiques", "Biodiversité urbaine", "Espaces publics inclusifs", 
    "Design urbain durable", "Urbanisme participatif", "Architecture bio-inspirée", "Biomimétisme", 
    "Design régénératif", "Construction en bois", "Constructions légères", "Constructions en matériaux recyclés", 
    "Constructions autonomes", "Micro-habitats", "Espaces de coworking", "Espaces de coliving", 
    "Habitat partagé", "Communautés intentionnelles", "Écovillages", "Tourisme durable", 
    "Tourisme culturel", "Tourisme d'aventure", "Tourisme de bien-être", "Tourisme d'affaires", 
    "Hôtels éco-certifiés", "Hébergements insolites", "Locations de vacances", "Agritourisme", 
    "Glamping", "Slow travel", "Micro-voyages", "Microaventures", "Voyages de formation", 
    "Voyages solidaires", "Voyages humanitaires", "Volontourisme", "Croisières éco-responsables", 
    "Expéditions scientifiques", "Voyages interstellaires"
]

def lambda_handler(event, context):
    try:
        # Sélectionner un sujet aléatoire
        sujet_choisi = random.choice(sujet)
        logger.info(f"Sujet choisi : {sujet_choisi}")

        # Prompt pour GPT-4
        prompt_text = (f"Commence ta phrase par #LeSaviezVous. Donne moi une information insolite ou utile et vraie concernant le sujet : {sujet_choisi}, en 150 caractères maximum. "
                       "Si tu le souhaites, tu peux finir ta phrase par un émoji en rapport avec le sujet ou bien alors, finir par un hashtag toujours en rapport avec le sujet")
        
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
        tweet_response = client.create_tweet(text=message)
        logger.info(f"Tweet posté avec succès. ID du tweet : {tweet_response.data['id']}")
        
        return {
            'statusCode': 200,
            'body': 'Tweet posted successfully!'
        }
    except openai.error.OpenAIError as e:
        logger.error(f"Erreur OpenAI : {e}")
        return {
            'statusCode': 500,
            'body': f"Erreur OpenAI : {str(e)}"
        }
    except tweepy.TweepyException as e:
        logger.error(f"Erreur Tweepy : {e}")
        return {
            'statusCode': 500,
            'body': f"Erreur Tweepy : {str(e)}"
        }
    except Exception as e:
        logger.error(f"Erreur inconnue : {e}")
        return {
            'statusCode': 500,
            'body': f"Erreur : {str(e)}"
        }
