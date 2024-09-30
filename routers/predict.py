import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from PIL import Image
import io
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
import wikipediaapi

router = APIRouter()

# Set the model path to the current directory
model_path = os.path.join(os.path.dirname(__file__), 'my_model.h5')

# Check if the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Load your trained model
model = tf.keras.models.load_model(model_path)

# Class names
classes = ['Aspergillus', 'Bacillus', 'Bacillus cereus', 'Candida', 'Penicillium rubens', 'Pseudomonas', 'Staphylococcus']

def load_and_predict(img):
    img = keras_image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    predicted_class_idx = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    predicted_class = classes[predicted_class_idx]
    return predicted_class, float(confidence)

def get_wikipedia_info(predicted_class):
    # Initialize the Wikipedia API with a proper user agent
    user_agent = "microbio/1.0 (sachinharshitha179@gmail.com)"
    wiki_wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI, user_agent=user_agent)
    
    page = wiki_wiki.page(predicted_class)
    
    if page.exists():
        # Get the main summary
        about = page.summary
        
        # Extract different sections
        articles = []
        
        # Fetch top related articles with their URLs
        for link_title, link_info in page.links.items():
            if link_info.ns == 0:  # Only consider main articles
                full_url = f"https://en.wikipedia.org/wiki/{link_title.replace(' ', '_')}"
                articles.append({"name": link_title, "url": full_url})
                
                if len(articles) >= 3:  # Limit to top 3 articles
                    break
        
        key_research_topics = []
        uses = ""
        illnesses_caused = ""
        
        # Iterate through sections to extract information
        for section in page.sections:
            if 'use' in section.title.lower():
                uses = section.text
            elif 'disease' in section.title.lower() or 'infection' in section.title.lower():
                illnesses_caused = section.text
            else:
                key_research_topics.append(section.title)
        
        # Limiting the about section to the first 250 words
        about_words = about.split()
        about = ' '.join(about_words[:250])
        
        return {
            "about": about,
            "articles": articles,
            "key_research_topics": key_research_topics,
            "uses": uses,
            "illnesses_caused": illnesses_caused
        }
    else:
        return {
            "about": "No detailed description found for this category.",
            "articles": [],
            "key_research_topics": [],
            "uses": "No information available.",
            "illnesses_caused": "No information available."
        }

@router.post("/predict/")
async def predict(
    file: UploadFile = File(...),
   
):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        img = img.resize((224, 224))

        predicted_class, confidence = load_and_predict(img)
        
        # Get a detailed description from Wikipedia structured as needed
        wikipedia_info = get_wikipedia_info(predicted_class)

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "about": wikipedia_info["about"],
            "articles": wikipedia_info["articles"],  # Now includes both name and URL
            "key_research_topics": wikipedia_info["key_research_topics"],
            "uses": wikipedia_info["uses"],
            "illnesses_caused": wikipedia_info["illnesses_caused"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))