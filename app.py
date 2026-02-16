from flask import Flask, render_template, request, jsonify
import os
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

app = Flask(__name__)

# DynamoDB setup
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'housingai-roi-calculator')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-west-2')

def get_table():
    """Get DynamoDB table resource."""
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    return dynamodb.Table(TABLE_NAME)


@app.route('/')
def calculator():
    """Serve the ROI calculator page."""
    calc_id = request.args.get('id', '')
    org_name = request.args.get('org', '')
    embed = request.args.get('embed', 'false') == 'true'
    return render_template('calculator.html', calc_id=calc_id, org_name=org_name, embed=embed)


@app.route('/api/save', methods=['POST'])
def save_data():
    """Save calculator inputs to DynamoDB."""
    data = request.get_json()
    calc_id = data.get('id')

    if not calc_id:
        return jsonify({"error": "Missing id parameter"}), 400

    try:
        table = get_table()
        table.put_item(Item={
            'calc_id': calc_id,
            'inputs': json.dumps(data.get('inputs', {})),
            'org_name': data.get('org_name', ''),
            'updated_at': datetime.now(timezone.utc).isoformat()
        })
        return jsonify({"status": "saved"})
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/load/<calc_id>')
def load_data(calc_id):
    """Load calculator inputs from DynamoDB."""
    try:
        table = get_table()
        response = table.get_item(Key={'calc_id': calc_id})
        item = response.get('Item')

        if not item:
            return jsonify({"status": "not_found"})

        return jsonify({
            "status": "found",
            "inputs": json.loads(item.get('inputs', '{}')),
            "org_name": item.get('org_name', ''),
            "updated_at": item.get('updated_at', '')
        })
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint for AWS."""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
