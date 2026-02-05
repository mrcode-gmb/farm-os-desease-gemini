# Plant Disease Detection System

## Overview
An AI-powered plant disease detection system that uses deep learning to identify plant diseases from images. The system provides detailed information about detected diseases, including symptoms, causes, treatment recommendations, and prevention measures to help farmers make informed decisions.

## Features

### 🔍 Disease Detection
- **38 Plant Conditions**: Detects 38 different plant diseases and healthy states
- **14 Crop Types**: Supports Apple, Corn, Grape, Tomato, Potato, Pepper, Cherry, Peach, Strawberry, Orange, Squash, Blueberry, Raspberry, and Soybean
- **High Accuracy**: Deep learning model with confidence scores
- **Real-time Analysis**: Fast prediction with detailed results

### 📊 Detailed Information
- **Disease Name**: Human-readable disease identification
- **Confidence Score**: Prediction confidence percentage
- **Severity Level**: Disease severity assessment
- **Symptoms**: Comprehensive list of disease symptoms
- **Causes**: Understanding what causes the disease
- **Treatment**: Step-by-step treatment recommendations
- **Prevention**: Preventive measures for future protection
- **Top 3 Predictions**: Alternative diagnoses with confidence scores

### 🌐 RESTful API
- **Flask-based API**: Easy integration with any backend
- **Laravel Ready**: Complete Laravel integration examples
- **CORS Enabled**: Cross-origin requests supported
- **Batch Processing**: Analyze multiple images at once
- **Comprehensive Documentation**: Detailed API docs included

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python api.py
```

### Test the API
```bash
# Health check
curl http://localhost:5000/api/health

# Analyze plant image
curl -X POST http://localhost:5000/api/predict \
  -F "image=@path/to/plant_image.jpg"
```

## Project Structure

```
Plant desease/
├── api.py                      # Flask API for Laravel integration
├── app.py                      # Original Flask web app
├── model.py                    # ResNet9 model architecture
├── utils.py                    # Prediction utilities
├── disease_info.py             # Disease information database
├── plant-disease-model.pth     # Trained model weights
├── requirements.txt            # Python dependencies
├── API_DOCUMENTATION.md        # Complete API documentation
├── QUICK_START.md             # Quick start guide
├── static/                     # Static files and uploads
└── templates/                  # HTML templates
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Analyze single image |
| `/api/predict-batch` | POST | Analyze multiple images |
| `/api/diseases` | GET | List all diseases |
| `/api/disease/<class>` | GET | Get disease details |
| `/api/crops` | GET | List supported crops |

## Supported Diseases

### Tomato (9 conditions)
- Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy

### Corn/Maize (4 conditions)
- Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy

### Potato (3 conditions)
- Early Blight, Late Blight, Healthy

### Apple (4 conditions)
- Apple Scab, Black Rot, Cedar Apple Rust, Healthy

### Grape (4 conditions)
- Black Rot, Esca (Black Measles), Leaf Blight, Healthy

### And 9 more crop types...

## Laravel Integration

### Controller Example
```php
use Illuminate\Support\Facades\Http;

$response = Http::attach(
    'image',
    file_get_contents($request->file('image')->path()),
    $request->file('image')->getClientOriginalName()
)->post('http://localhost:5000/api/predict');

$result = $response->json();
```

See [QUICK_START.md](./QUICK_START.md) for complete Laravel integration guide.

## Documentation

- **[API Documentation](./API_DOCUMENTATION.md)**: Complete API reference with examples
- **[Quick Start Guide](./QUICK_START.md)**: Step-by-step setup and integration guide

## Technology Stack

- **Deep Learning**: PyTorch
- **Model**: ResNet9 (Custom CNN architecture)
- **API Framework**: Flask
- **Image Processing**: PIL, torchvision
- **Backend Integration**: Laravel (PHP)

## Model Information

- **Architecture**: ResNet9 (9-layer Residual Network)
- **Input Size**: 256x256 RGB images
- **Output**: 38 classes (diseases + healthy states)
- **Training Dataset**: PlantVillage Dataset

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 api:app
```

### Using Systemd
See [QUICK_START.md](./QUICK_START.md) for systemd service configuration.

### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[Add your license here]

## Contact

For questions or support, contact your development team.

---

**Made with ❤️ for farmers worldwide**