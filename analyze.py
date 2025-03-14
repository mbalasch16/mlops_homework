from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
import re
import utilities

sentiment_pipeline = pipeline("sentiment-analysis")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')






#EMAIL_CLASSES = [
   # "Work", "Sports", "Food"
#]


EMAIL_CLASSES = utilities.read_class_file("email.txt") 





def get_sentiment(text):
    response = sentiment_pipeline(text)
    return response

def compute_embeddings(embeddings = EMAIL_CLASSES):
    embeddings = model.encode(embeddings)
    return zip(EMAIL_CLASSES, embeddings)

def classify_email(text):
    # Encode the input text
    text_embedding = model.encode([text])[0]
    
    # Get embeddings for all classes
    class_embeddings = compute_embeddings()
    
    # Calculate distances and return results
    results = []
    for class_name, class_embedding in class_embeddings:
        # Compute cosine similarity between text and class embedding
        similarity = np.dot(text_embedding, class_embedding) / (np.linalg.norm(text_embedding) * np.linalg.norm(class_embedding))
        results.append({
            "class": class_name,
            "similarity": float(similarity)  # Convert tensor to float for JSON serialization
        })
    
    # Sort by similarity score descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results
    
def write_file(res):
    
    #response_body=res.get_data(as_text=True)
    
    #match = re.search(r'"message":\s*"([^"]+)"', response_body)
    #if match:
       # message = match.group(1)  # Extract the message content
        #print(message)
    #else:
       # message = "not found"
        #print("Message not found")
    
    # Extract the 'message' field from the JSON response
    #response_dict = json.load(response_body)
    #message = response_dict["message"]
      
        # Optionally, save the message to a file
    with open('email.txt', 'a') as file:
        file.write(res + '\n')  # Save message to file with a newline
        #print("content written to file")
    return res

   