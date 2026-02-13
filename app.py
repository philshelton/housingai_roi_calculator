from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def calculator():
    """Serve the ROI calculator page."""
    # Optional: accept query params for pre-filling org name or customisation
    org_name = request.args.get('org', '')
    theme = request.args.get('theme', 'light')
    embed = request.args.get('embed', 'false') == 'true'
    return render_template('calculator.html', org_name=org_name, theme=theme, embed=embed)

@app.route('/health')
def health():
    """Health check endpoint for AWS."""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
