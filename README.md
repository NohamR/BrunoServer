# Bruno Self-Hosted License Server

A self-hosted license activation server for [Bruno](https://github.com/usebruno/bruno/) API client.

> **⚠️ DISCLAIMER**: This project is for **development and educational purposes only**. If you like Bruno and use it professionally, please [purchase a legitimate license](https://www.usebruno.com/pricing) to support the developers.

## Overview

This Flask-based server implements the license activation and verification endpoints required by Bruno, allowing you to run a local license server for testing and development purposes.

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/NohamR/BrunoServer.git && cd BrunoServer
pip install -r requirements.txt
```

## Usage
Run the server with default settings (localhost:5000):
```bash
python server.py
```

Configure the server using environment variables:
```bash
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
export FLASK_DEBUG=true
```

### Configure Bruno

To use this license server with Bruno:

#### Option 1: Use the Public Demo Server
- **URL**: `https://brunoserver-k4vf.onrender.com`
- ⚠️ **Note**: This server may be inactive due to Render's free tier spin-down after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.

#### Option 2: Run Your Own Server
1. Start the server locally
2. In Bruno, configure the license server URL to point to your local server:
   - Default: `http://127.0.0.1:5000`
3. Use any license key for activation and any otp for verification.

#### Option 3: Run Your Own over Docker
1. Create docker image:
```bash
docker build -t bruno-server .
```
2. Run docker image in container:
```bash
docker run -d --name bruno-server -p 5000:5000 bruno-server
```
3. Use the option 'License Server' from activation and enter `http://localhost:5000` as License Server URL
4. Enter any text in License Key and Email.
5. When prompted for OTP, enter any text. Bruno Ultimate will be activated.

## Legal Notice

This software is provided for educational and development purposes only. The authors do not condone piracy or license violations. 

**Please support the Bruno project** by purchasing a legitimate license if you:
- Use Bruno for professional/commercial work
- Want to support ongoing development
- Need official support

Visit [Bruno's official website](https://www.usebruno.com/) to learn more and purchase a license.

## Disclaimer

This project is not affiliated with, endorsed by, or connected to the Bruno project or its developers. All trademarks and copyrights belong to their respective owners.
