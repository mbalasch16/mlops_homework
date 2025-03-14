from flask import Flask, request, jsonify, render_template
from analyze import get_sentiment, compute_embeddings, classify_email, write_file
app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    print("Home page")
    return render_template('index.html')


@app.route("/api/v1/sentiment-analysis/", methods=['POST'])
def analysis():
    if request.is_json:
        data = request.get_json()
        sentiment = get_sentiment(data['text'])
        return jsonify({"message": "Data received", "data": data, "sentiment": sentiment}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/valid-embeddings/", methods=['GET'])
def valid_embeddings():
    embeddings = compute_embeddings()
    formatted_embeddings = []
    for text, vector in embeddings:
        formatted_embeddings.append({
            "text": text,
            "vector": vector.tolist() if hasattr(vector, 'tolist') else vector
        })
    embeddings = formatted_embeddings
    return jsonify({"message": "Valid embeddings fetched", "embeddings": embeddings}), 200
    
@app.route("/api/v1/add_class/",methods=['POST'])
def add_class():
    print("in add_class",request.get_json())
    if request.is_json:
        data = request.get_json()
        text = data['text']
        write_file(text)
    
        return jsonify({"message": f"Added class {text}"}), 200
    return jsonify({"error": "Invalid Content-Type"}), 400

@app.route("/api/v1/classify/", methods=['POST'])
def classify():
    if request.is_json:
        data = request.get_json()
        text = data['text']
        classifications = classify_email(text)
        #res = jsonify({"message": "Email classified", "classifications": classifications}), 200
        #ms = write_file(request)
        #json_response,status_code = jsonify({"message": "Email classified", "classifications": classifications}),200
        #write_file(json_response)
        #return json_response
        return jsonify({"message": "Email classified", "classifications": classifications}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/classify-email/", methods=['GET'])
def classify_with_get():
    text = request.args.get('text')
    classifications = classify_email(text)
    return jsonify({"message": "Email classified", "classifications": classifications}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
    