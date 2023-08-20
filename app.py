from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    bearer_token = request.form['bearerToken']

    offer_data = {
        "name": request.form['name'],
        "type": request.form['type'],
        "metadata": {
            "value": int(request.form['value']),
            "minAmount": int(request.form['minAmount']),
            "maxAmount": int(request.form['maxAmount'])
        },
        "isActive": True,
        "jsonRules": {
            "all": []
        },
        "validTill": request.form['validTill'],
        "priority": int(request.form['priority'])
    }

    json_rules_count = int(request.form['jsonRulesCount'])
    for i in range(json_rules_count):
        fact = request.form[f'fact_{i}']
        operator = request.form[f'operator_{i}']
        value = int(request.form[f'value_{i}'])
        rule = {
            "fact": fact,
            "operator": operator,
            "value": value
        }
        offer_data["jsonRules"]["all"].append(rule)

    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    api_url = "https://api.beta.uat.refyne.co.in/refyne-admin/offer"

    response = requests.post(api_url, headers=headers, data=json.dumps(offer_data))

    if response.status_code == 200:
        return jsonify({"message": "Offer configuration successfully submitted"})
    else:
        return jsonify({"message": "Failed to submit offer configuration", "error": response.text})

if __name__ == '__main__':
    app.run(debug=True)
