from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "My name is Pratiyush Raj and I Deployed a file using Jenkins + Docker + GitHub My friend is doing devops aman is doing devops and he is really a genius.And i am also a genius.We both are genius we are doing devops"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
