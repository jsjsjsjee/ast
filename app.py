from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "793d0584ae5607188171fcf3b170c17023628745"  # Replace with your key

def get_ai_response(query):
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()

        # Get answer box or snippet
        if "answerBox" in data and "answer" in data["answerBox"]:
            response = data["answerBox"]["answer"]
        elif "organic" in data and data["organic"]:
            response = data["organic"][0]["snippet"]
        else:
            response = "Sorry, I couldn't find an answer."

        # Replace specific punctuation with newline for formatting (if needed)
        response = response.replace(".", ".\n")  # Add newline after every period, adjust as needed

        return response

    except Exception as e:
        return f"API Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    ai_reply = ""
    
    if request.method == "POST":
        user_input = request.form["question"]
        ai_reply = get_ai_response(user_input)
    
    return render_template("index.html", user_input=user_input, bot_response=ai_reply)

if __name__ == "__main__":
    app.run(debug=True)