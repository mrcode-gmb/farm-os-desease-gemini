import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from disease_info import format_disease_response

# Same class order used in training
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

def predict_image(image_path, model, device):
    """
    Basic prediction function (backward compatible)
    Returns only the class name
    """
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(image)
        _, pred = torch.max(outputs, 1)

    return CLASS_NAMES[pred.item()]


def predict_image_detailed(image_path, model, device):
    """
    Enhanced prediction function with confidence scores and detailed information
    
    Args:
        image_path: Path to the image file
        model: Trained PyTorch model
        device: Device to run inference on (cpu/cuda)
        
    Returns:
        Dictionary containing:
        - prediction: Disease class name
        - confidence: Confidence percentage
        - disease_name: Human-readable disease name
        - crop: Affected crop
        - severity: Disease severity level
        - description: Disease description
        - symptoms: List of symptoms
        - causes: List of causes
        - treatment: List of treatment recommendations
        - prevention: List of prevention measures
        - is_healthy: Boolean indicating if plant is healthy
        - top_predictions: Top 3 predictions with confidence scores
    """
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Get predictions
    model.eval()
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
        confidence, pred = torch.max(probabilities, 1)
        
        # Get top 3 predictions
        top_probs, top_indices = torch.topk(probabilities, 3, dim=1)
        
    # Convert to percentages
    confidence_pct = confidence.item() * 100
    
    # Get predicted class
    predicted_class = CLASS_NAMES[pred.item()]
    
    # Get top 3 predictions
    top_predictions = []
    for i in range(3):
        top_predictions.append({
            'class': CLASS_NAMES[top_indices[0][i].item()],
            'confidence': f"{top_probs[0][i].item() * 100:.2f}%"
        })
    
    # Get detailed disease information
    response = format_disease_response(predicted_class, confidence_pct)
    response['top_predictions'] = top_predictions
    
    return response
