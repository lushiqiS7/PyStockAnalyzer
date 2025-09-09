from flask import Flask, render_template, request
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    try:
        ticker = request.form.get('ticker', 'AAPL').upper()
        
        return f"""
        <h2>anaylse {ticker}</h2>
        <p>this is {ticker} simple anaylse results</p>
        <p>full function is still developing...</p>
        <a href="/">return home</a>
        """
        
    except Exception as e:
        return f"error: {str(e)}"

if __name__ == '__main__':
    print("Start PyStock Analyzer Web...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)