# AI Image Caption Generator

A full-stack web application that generates intelligent captions for images using deep learning. Built with Flask, TensorFlow, and modern web technologies.

## Features

- **Deep Learning Powered**: Uses ResNet50 for feature extraction and LSTM-style caption generation
- **Modern UI**: Clean, responsive interface with drag-and-drop file upload
- **Real-time Processing**: Generate captions in seconds
- **File Validation**: Supports PNG, JPG, JPEG formats (max 16MB)
- **Copy to Clipboard**: Easy sharing of generated captions
- **Error Handling**: Comprehensive error messages and loading states
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## Project Structure

```
project-1/
|
|--- app.py                 # Main Flask application with AI model
|--- requirements.txt       # Python dependencies
|--- README.md              # This file
|
|--- model/                 # Directory for model files (empty for demo)
|
|--- static/
|    |--- css/
|    |    |--- style.css    # Professional styling
|    |
|    |--- js/
|        |--- script.js     # Frontend JavaScript functionality
|
|--- templates/
|    |--- index.html        # Main HTML template
|
|--- uploads/               # Temporary storage for uploaded images
```

## Technology Stack

### Backend
- **Flask**: Web framework for Python
- **TensorFlow/Keras**: Deep learning framework
- **ResNet50**: Pre-trained CNN for feature extraction
- **Pillow**: Image processing
- **NumPy**: Numerical computations

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Typography

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 8GB+ RAM recommended (for TensorFlow models)

### Step 1: Clone/Download the Project
```bash
# If using git (not required for this demo)
git clone <repository-url>
cd project-1
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

## Usage Guide

### 1. Upload an Image
- **Method 1**: Click "Browse Files" and select an image
- **Method 2**: Drag and drop an image onto the upload area
- **Method 3**: Click anywhere in the upload area to browse

### 2. Generate Caption
- After upload, the AI will automatically process the image
- Wait for the loading animation to complete
- View the generated caption below your image

### 3. Interact with Results
- **Copy Caption**: Click the "Copy" button to copy to clipboard
- **Regenerate**: Click "Regenerate Caption" for a different result
- **Upload New**: Click "Upload New Image" to start over

### Keyboard Shortcuts
- `Ctrl/Cmd + V`: Paste image from clipboard
- `Ctrl/Cmd + C`: Copy caption (when no text selected)
- `Escape`: Reset and upload new image

## API Endpoints

### POST /upload
Upload an image and generate a caption
- **Body**: multipart/form-data with file field
- **Response**: JSON with filename and caption

### POST /caption
Generate a new caption for an existing image
- **Body**: JSON with filename field
- **Response**: JSON with generated caption

### GET /health
Check server and model status
- **Response**: JSON with health status

## Model Architecture

### Feature Extraction
- **ResNet50**: Pre-trained on ImageNet
- **Input Size**: 224x224 RGB images
- **Output**: 2048-dimensional feature vector

### Caption Generation
- **Simplified LSTM-style approach**: Demonstrates the architecture
- **Vocabulary**: Basic English words and phrases
- **Output**: Natural language caption (10-15 words)

## File Upload Details

### Supported Formats
- PNG (Portable Network Graphics)
- JPG/JPEG (Joint Photographic Experts Group)

### File Size Limit
- Maximum: 16MB per image
- Recommended: Under 5MB for faster processing

### Storage
- Images are stored temporarily in `/uploads/`
- Automatic cleanup of files older than 1 hour
- No long-term storage of user images

## Performance Notes

### First Load
- Initial model loading may take 10-30 seconds
- Subsequent requests are much faster (2-5 seconds)

### Memory Usage
- ResNet50 model: ~100MB RAM
- Feature processing: ~50MB RAM per image
- Total recommended: 2GB+ RAM available

## Troubleshooting

### Common Issues

**1. "Model loading failed"**
- Check TensorFlow installation: `pip show tensorflow`
- Verify Python version compatibility
- Restart the application

**2. "File upload failed"**
- Check file format (PNG/JPG/JPEG only)
- Verify file size (< 16MB)
- Check disk space in uploads directory

**3. "Caption generation failed"**
- Ensure image is not corrupted
- Try uploading a different image
- Check server logs for errors

**4. "Server not responding"**
- Check if Flask is running: `python app.py`
- Verify port 5000 is not in use
- Check firewall settings

### Debug Mode
To enable debug mode with detailed error messages:
```python
# In app.py, change the last line to:
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Development Notes

### Code Structure
- **app.py**: Main application with Flask routes and AI model
- **templates/index.html**: Frontend UI with modern design
- **static/css/style.css**: Professional styling and animations
- **static/js/script.js**: Interactive JavaScript functionality

### Key Features Implemented
- Drag-and-drop file upload
- Real-time loading states
- Error handling and validation
- Responsive design
- Copy to clipboard functionality
- Toast notifications
- Keyboard shortcuts

### Security Considerations
- File type validation
- File size limits
- Secure filename generation
- Temporary file storage
- Input sanitization

## Production Deployment

### For Production Use
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Implement proper logging
3. Add database for persistent storage
4. Use a trained LSTM model for better captions
5. Implement user authentication
6. Add rate limiting
7. Use HTTPS/SSL certificates

### Environment Variables
```bash
# Set Flask environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Set upload directory
export UPLOAD_FOLDER=/path/to/uploads
```

## Contributing

### Enhancement Ideas
- [ ] Train a proper LSTM model on COCO dataset
- [ ] Add multiple language support
- [ ] Implement batch processing
- [ ] Add image editing features
- [ ] Create user accounts and history
- [ ] Add API key authentication
- [ ] Implement caching for better performance

## License

This project is for educational purposes. Feel free to modify and use it for learning and development.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments in each file
3. Test with different image formats and sizes
4. Verify all dependencies are installed correctly

---

**Built with**: Flask, TensorFlow, HTML5, CSS3, JavaScript  
**Compatible**: Python 3.8+, Modern browsers  
**Last Updated**: 2024
