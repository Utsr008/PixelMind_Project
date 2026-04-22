"""
Main application file for the AI Image Generator backend.
"""
import os
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure your Colab backend URL here
# You'll get this from ngrok when you run the Colab notebook
COLAB_BACKEND_URL='https://a66e-34-16-244-247.ngrok-free.app'

@app.route('/')
def index():
    """Render the main index page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Endpoint to generate an image via the Colab backend."""
    try:
        data = request.json

        # Prepare the request for the Colab backend
        payload = {
            'model': data.get('model'),
            'lora': data.get('lora'),
            'prompt': data.get('prompt'),
            'seed': data.get('seed', 0)
        }

        # Send request to Colab backend
        response = requests.post(
            f'{COLAB_BACKEND_URL}/generate',
            json=payload,
            headers={'ngrok-skip-browser-warning': 'true'},
            timeout=120  # 2 minute timeout for image generation
        )

        if response.status_code == 200:
            import base64
            # Check if the backend returned raw image bytes
            if response.content.startswith(b'\x89PNG') or 'image' in response.headers.get('Content-Type', ''):
                img_str = base64.b64encode(response.content).decode('utf-8')
                return jsonify({
                    'success': True,
                    'image': f'data:image/png;base64,{img_str}',
                    'seed': data.get('seed')
                })
            
            # Otherwise, try parsing as JSON
            try:
                result = response.json()
                return jsonify({
                    'success': True,
                    'image': result['image'],  # Base64 encoded image
                    'seed': data.get('seed')
                })
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Expected JSON but got: {response.text[:200]}'
                }), 500
        else:
            return jsonify({
                'success': False,
                'error': f'Backend error: {response.status_code} - {response.text[:100]}'
            }), 500

    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timeout - generation took too long'
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'Cannot connect to Colab backend. Make sure it is running.'
        }), 503
    except requests.RequestException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Try to ping the Colab backend
        response = requests.get(
            f'{COLAB_BACKEND_URL}/health',
            headers={'ngrok-skip-browser-warning': 'true'},
            timeout=5
        )
        backend_status = response.status_code == 200
    except requests.RequestException:
        backend_status = False

    return jsonify({
        'status': 'healthy',
        'backend_connected': backend_status,
        'backend_url': COLAB_BACKEND_URL
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    print("\n" + "="*50)
    print("AI Image Generator Server")
    print("="*50)
    print("\nServer running on: http://localhost:5000")
    print(f"Colab backend URL: {COLAB_BACKEND_URL}")
    print("\nTo change this, update COLAB_BACKEND_URL in app.py")
    print("\n" + "="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
