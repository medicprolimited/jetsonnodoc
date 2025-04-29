# Jetson Embedding Generator

A web application that generates text embeddings using sentence transformer models hosted on a Jetson Orin Nano. The application consists of a FastAPI backend running on the Jetson and a simple web interface deployed on Vercel.

## Architecture

### Backend (Jetson Orin Nano)
- FastAPI application serving two sentence transformer models:
  - all-MiniLM-L6-v2 (faster, smaller)
  - all-mpnet-base-v2 (more accurate, larger)
- Exposes API endpoints on port 8002
- Uses ngrok for public internet access
- Runs as a systemd service for persistence

### Frontend (Vercel)
- Simple HTML/CSS/JavaScript web interface
- Deployed at https://apps.medicpro.london/web-app1
- Connects to Jetson backend via ngrok URL

## Setup Instructions

### Backend Setup

1. Create and activate Python virtual environment:
```bash
python -m venv /home/mx/jetsonnodoc/fastapi-env
source /home/mx/jetsonnodoc/fastapi-env/bin/activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up systemd service:
```bash
sudo cp systemd/jetson-embedding.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jetson-embedding
sudo systemctl start jetson-embedding
```

4. Set up ngrok:
```bash
ngrok http 8002
```

### Frontend Setup

1. Update the ngrok URL in `frontend/scripts/app.js`
2. Deploy to Vercel:
   - Connect your GitHub repository to Vercel
   - Configure the build settings to deploy the frontend directory
   - Set up automatic deployments

## Usage

1. Access the web interface at https://apps.medicpro.london/web-app1
2. Select a model from the dropdown
3. Enter text in the input field
4. Click "Generate Embedding" to get the result

## Maintenance

- The ngrok URL will change each time the service restarts (free tier)
- Update the URL in the frontend code when it changes
- Monitor the systemd service logs:
```bash
sudo journalctl -u jetson-embedding -f
```

## Security Considerations

- CORS is configured to only allow requests from the Vercel domain
- The API is protected by ngrok's basic authentication
- Consider implementing additional security measures for production use

## Troubleshooting

1. Check if the FastAPI service is running:
```bash
sudo systemctl status jetson-embedding
```

2. Verify ngrok is running and accessible:
```bash
curl https://abc123.ngrok.io/models
```

3. Check the application logs:
```bash
sudo journalctl -u jetson-embedding -f
```

## License

MIT License 