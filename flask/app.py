from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# About
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run()

