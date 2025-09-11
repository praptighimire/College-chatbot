# import pickle
# import json
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from app.db import get_connection
# from app.fallback import fallback_with_distilgpt2

# # from openai import OpenAI
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()
# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# # Load trained components
# with open("intent_model.pkl", "rb") as f:
#     intent_model = pickle.load(f)
# with open("vectorizer.pkl", "rb") as f:
#     vectorizer = pickle.load(f)
# with open("label_encoder.pkl", "rb") as f:
#     label_encoder = pickle.load(f)
# with open("intents.json", "r", encoding="utf-8") as f:
#     intents_data = json.load(f)



# def get_response(message, user_type="guest"):
#     intent = detect_intent(message)
#     if not is_allowed(intent, user_type):
#         return "Sorry, you are not authorized to access this information."

#     # Check intents.json for intent response
#     for intent_item in intents_data["intents"]:
#         if intent_item["tag"] == intent:
#             return intent_item["responses"][0]

#     # Fallback LLM if no match
#     return fallback_with_distilgpt2(message)

import pickle
import json
from app.fallback import fallback_with_phi



# Load ML model components
with open("intent_model.pkl", "rb") as f:
    intent_model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)
with open("intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f)

# Optional: Intent restriction logic
restricted_intents = {"finance"}

def is_allowed(intent, user_type):
    return not (intent in restricted_intents and user_type == "guest")

# def get_response(message, user_type="guest", department=None):
#     try:
#         # Vectorize input
#         X = vectorizer.transform([message])

#         # Get prediction probabilities
#         probas = intent_model.predict_proba(X)[0]
#         confidence = max(probas)

#         # Fallback to LLM if low confidence
#         if confidence < 0.5:
#             print("⚠️ Low confidence fallback")
#             return fallback_with_distilgpt2(message)

#         # Predict intent
#         prediction = intent_model.predict(X)[0]
#         intent = label_encoder.inverse_transform([prediction])[0]

#         print(f"🧠 Predicted intent: {intent} (confidence: {confidence:.2f})")

#         # Permission check
#         if not is_allowed(intent, user_type):
#             return "Sorry, you are not authorized to access this information."

#         # Look up intent in intents.json
#         for intent_item in intents_data["intents"]:
#             if intent_item["tag"] == intent:
#                 return intent_item["responses"][0]

#         # If not found in intents.json
#         return fallback_with_distilgpt2(message)

#     except Exception as e:
#         print("❌ Chatbot error:", e)
#         return "I'm sorry, something went wrong."
def get_response(message, user_type="guest"):
    try:
        # 1. Predict intent and confidence
        X = vectorizer.transform([message])
        probas = intent_model.predict_proba(X)[0]
        prediction = intent_model.predict(X)[0]
        confidence = max(probas)
        intent = label_encoder.inverse_transform([prediction])[0]

        print(f"Detected intent: {intent} (confidence: {confidence:.2f})")

        # 2. Authorization check
        if not is_allowed(intent, user_type):
            return "Sorry, you are not authorized to access this information."

        # 3. Return from intents.json if match is known
        if confidence > 0.3:  # Lower threshold a bit
            for i in intents_data["intents"]:
                if i["tag"] == intent:
                    return i["responses"][0]

        print("⚠️ Low confidence or no intent match, using fallback LLM")
        return fallback_with_phi(message)

    except Exception as e:
        print("❌ Chatbot error:", e)
        return "Something went wrong."
