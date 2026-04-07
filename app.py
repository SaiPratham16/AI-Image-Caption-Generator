import os
import numpy as np
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pickle
import json
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load pre-trained ResNet50 model for feature extraction
# This model will extract features from images for caption generation
# print("Loading ResNet50 model for feature extraction...")
# feature_extractor = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Simple vocabulary for demonstration (in production, use a larger pre-trained vocabulary)
# This is a simplified approach - in real applications, you'd use a proper dataset
vocabulary = {
    '<start>': 1, '<end>': 2, '<unk>': 3,
    'a': 4, 'the': 5, 'is': 6, 'are': 7, 'and': 8, 'in': 9, 'on': 10,
    'man': 11, 'woman': 12, 'person': 13, 'people': 14, 'child': 15,
    'dog': 16, 'cat': 17, 'animal': 18, 'bird': 19,
    'car': 20, 'truck': 21, 'vehicle': 22, 'bus': 23,
    'house': 24, 'building': 25, 'tree': 26, 'flower': 27,
    'red': 28, 'blue': 29, 'green': 30, 'yellow': 31, 'black': 32, 'white': 33,
    'big': 34, 'small': 35, 'large': 36, 'little': 37,
    'sitting': 38, 'standing': 39, 'walking': 40, 'running': 41,
    'beautiful': 42, 'nice': 43, 'good': 44, 'pretty': 45,
    'with': 46, 'has': 47, 'have': 48, 'wearing': 49,
    'shirt': 50, 'dress': 51, 'hat': 52, 'glasses': 53
}

# Reverse vocabulary for decoding
reverse_vocabulary = {v: k for k, v in vocabulary.items()}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
def preprocess_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        return np.array(img)
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None
# def preprocess_image(image_path):
#     """
#     Preprocess image for feature extraction
#     - Resize to 224x224 (ResNet50 input size)
#     - Convert to array and preprocess for ResNet50
#     """
#     try:
#         # Load and resize image
#         img = Image.open(image_path)
#         img = img.convert('RGB')  # Ensure RGB format
#         img = img.resize((224, 224))
        
#         # Convert to array and preprocess
#         # img_array = img_to_array(img)
#         # img_array = np.expand_dims(img_array, axis=0)
#         # img_array = preprocess_input(img_array)
        
#         return img_array
#     except Exception as e:
#         print(f"Error preprocessing image: {e}")
#         return None
def extract_features(image_path):
    processed_image = preprocess_image(image_path)
    if processed_image is None:
        return None
    return processed_image.flatten()
# def extract_features(image_path):
#     """Extract features from image using ResNet50"""
#     try:
#         # Preprocess image
#         processed_image = preprocess_image(image_path)
#         if processed_image is None:
#             return None
            
#         # Extract features
#         # features = feature_extractor.predict(processed_image, verbose=0)
#         # return features.flatten()
#     except Exception as e:
#         print(f"Error extracting features: {e}")
#         return None

def generate_caption_simple(image_features):
    """
    Generate a simple caption based on image features
    This is a simplified approach for demonstration
    In production, you'd use a trained LSTM model
    """
    # Simple rule-based caption generation
    # This creates basic captions based on common patterns
    
    # Basic caption templates
    templates = [
        "A {color} {object} is {action} in the {location}.",
        "The {object} is {size} and {color}.",
        "A person is {action} with a {object}.",
        "This is a {size} {color} {object}.",
        "A beautiful {object} {action} in the scene."
    ]
    
    # Sample words (in real app, these would be predicted by the model)
    colors = ['red', 'blue', 'green', 'black', 'white']
    objects = ['car', 'house', 'tree', 'person', 'animal', 'building']
    actions = ['standing', 'sitting', 'moving', 'resting', 'visible']
    locations = ['background', 'foreground', 'scene', 'view']
    sizes = ['big', 'small', 'large', 'medium']
    
    # Generate a random but plausible caption
    import random
    
    # Use image features to influence the caption (simplified)
    if image_features is not None:
        # Use first few features to seed random generation for consistency
        seed = int(np.sum(image_features[:5]) * 1000) % 1000
        random.seed(seed)
    
    template = random.choice(templates)
    
    caption = template.format(
        color=random.choice(colors),
        object=random.choice(objects),
        action=random.choice(actions),
        location=random.choice(locations),
        size=random.choice(sizes)
    )
    
    return caption

def generate_caption_with_lstm(image_features, max_length=20):
    """
    Generate caption using a simplified LSTM approach
    This simulates what a real trained model would do
    """
    # For demonstration, we'll create a more sophisticated pattern
    # In production, this would use an actual trained LSTM model
    
    # Start with beginning token
    caption = ['a']
    
    # Generate caption word by word (simplified simulation)
    for i in range(max_length - 1):
        # In real LSTM, this would predict next word based on features and previous words
        # Here we use a simple pattern-based approach
        
        if i == 0:
            # First word - usually an adjective or noun
            first_words = ['beautiful', 'big', 'small', 'colorful', 'nice']
            caption.append(np.random.choice(first_words))
        elif i == 1:
            # Second word - usually a noun
            nouns = ['car', 'house', 'tree', 'person', 'dog', 'cat', 'building']
            caption.append(np.random.choice(nouns))
        elif i == 2:
            # Third word - usually a verb
            verbs = ['is', 'are', 'was', 'were']
            caption.append(np.random.choice(verbs))
        elif i == 3:
            # Fourth word - usually a verb or adjective
            actions = ['standing', 'sitting', 'moving', 'beautiful', 'colorful']
            caption.append(np.random.choice(actions))
        elif i == 4:
            # Fifth word - preposition
            prepositions = ['in', 'on', 'at', 'with']
            caption.append(np.random.choice(prepositions))
        elif i == 5:
            # Sixth word - location or context
            contexts = ['the', 'a', 'this', 'that']
            caption.append(np.random.choice(contexts))
        elif i == 6:
            # Seventh word - final context
            final_words = ['scene', 'background', 'view', 'picture']
            caption.append(np.random.choice(final_words))
        else:
            # End the caption
            break
    
    # Join and capitalize
    caption_text = ' '.join(caption).capitalize() + '.'
    
    # Clean up the caption
    caption_text = caption_text.replace('  ', ' ').strip()
    
    return caption_text

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PNG, JPG, or JPEG'}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract features from the image
        print(f"Extracting features from {filename}...")
        features = extract_features(filepath)
        
        if features is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Generate caption
        print("Generating caption...")
        caption = generate_caption_with_lstm(features)
        
        # Return success response
        return jsonify({
            'success': True,
            'filename': filename,
            'caption': caption,
            'message': 'Image uploaded and processed successfully'
        })
        
    except Exception as e:
        print(f"Error in upload_file: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/caption', methods=['GET', 'POST'])
def get_caption():
    """Generate caption for an uploaded image"""
    try:
        if request.method == 'GET':
            # Get filename from query parameter
            filename = request.args.get('filename')
            if not filename:
                return jsonify({'error': 'Filename required'}), 400
        else:
            # Get filename from JSON body
            data = request.get_json()
            if not data or 'filename' not in data:
                return jsonify({'error': 'Filename required'}), 400
            filename = data['filename']
        
        # Construct file path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Extract features and generate caption
        features = extract_features(filepath)
        if features is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        caption = generate_caption_with_lstm(features)
        
        return jsonify({
            'success': True,
            'caption': caption,
            'filename': filename
        })
        
    except Exception as e:
        print(f"Error in get_caption: {e}")
        return jsonify({'error': f'Caption generation failed: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': feature_extractor is not None,
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Clean up old uploads on startup
def cleanup_old_uploads():
    """Remove old uploaded files (older than 1 hour)"""
    try:
        import time
        current_time = time.time()
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > 3600:  # 1 hour
                    os.remove(filepath)
                    print(f"Removed old file: {filename}")
    except Exception as e:
        print(f"Error cleaning up old uploads: {e}")

if __name__ == '__main__':
    print("Starting AI Image Caption Generator...")
    print("Features:")
    print("- ResNet50 feature extraction")
    print("- Simplified LSTM-style caption generation")
    print("- File upload and validation")
    print("- RESTful API endpoints")
    print()
    
    # Clean up old files
    cleanup_old_uploads()
    
    # Run the application
    # app.run(debug=True, host='0.0.0.0', port=5000)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)