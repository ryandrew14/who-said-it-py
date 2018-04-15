from flask import Flask
import json
import utils
import celebs

app = Flask(__name__)

@app.route('/')
def index():
    return 'Identity Crisis python scraping server. Made for HackDartmouth IV.'

@app.route('/tweet')
def api_tweet():
    return utils.find_four()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
