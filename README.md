# PixelMind - AI Image Generator 🎨

PixelMind is a full-stack AI Image Generation application. It uses a split architecture to take advantage of free GPU computing power. The heavy image generation workloads run on **Google Colab**, while the beautiful and responsive web interface runs locally on your computer.

## 🌟 Features

- **Multiple AI Models**: Support for Stable Diffusion v1.5, DreamShaper, and SDXL Base 1.0.
- **LoRA Support**: Enhance generations with LoRA weights (e.g., Realistic Vision, Fearii LoHA).
- **Advanced Seed Control**: Keep track of seeds for reproducible results (Fixed, Random, Increment, Decrement).
- **Generation History**: Keep track of all generated images in your current session.
- **One-Click Download**: View generated images in full resolution and download them directly.

## 🏗️ Architecture

- **Backend (`untitled0.py`)**: Designed to be run in a Google Colab notebook with GPU enabled. It runs a Flask server exposed to the public internet using an `ngrok` tunnel. It uses the `diffusers` library to generate images and returns them as raw PNG data.
- **Frontend (`app.py` & `templates/index.html`)**: A local Flask server providing a sleek web interface. It connects to the Colab backend via the `ngrok` URL to submit prompts and retrieve images seamlessly.

## 🚀 Setup Instructions

### 1. Start the Colab Backend
1. Open Google Colab and enable the GPU runtime (`Runtime > Change runtime type > T4 GPU`).
2. Upload the code from `untitled0.py` into a new Colab cell.
3. Replace the `NGROK_AUTH_TOKEN` string with your personal token from [ngrok.com](https://ngrok.com/).
4. Run the cell. The script will download the necessary AI models and start the server.
5. Once running, the output will display a **Public URL** (e.g., `https://xxxx-xxxx.ngrok-free.app`). Copy this URL.

### 2. Configure the Local Frontend
1. Make sure you have Python installed on your local machine.
2. Install the required Python packages for the frontend:
   ```bash
   pip install flask flask-cors requests
   ```
3. Open `app.py` in your code editor.
4. Locate the `COLAB_BACKEND_URL` variable (around line 14) and update it with the URL you copied from Colab:
   ```python
   COLAB_BACKEND_URL='https://xxxx-xxxx.ngrok-free.app'
   ```

### 3. Run the App
1. Open your terminal in the project directory and run:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   **http://localhost:5000**
3. Enter your prompt, select your model, and click "Generate Image"!

## 📦 Dependencies

**Local Frontend:**
- `Flask`
- `flask-cors`
- `requests`

**Colab Backend:**
- `diffusers`
- `transformers`
- `accelerate`
- `torch` & `torchvision`
- `pyngrok`
- `flask` & `flask-cors`
- `Pillow`
