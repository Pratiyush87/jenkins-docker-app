from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "My name is Pratiyush Raj and I Deployed a file using Jenkins + Docker + GitHub My friend is doing devops"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)