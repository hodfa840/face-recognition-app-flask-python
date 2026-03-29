from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
import os
import uuid
import base64
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename
from ..utils.ml_engine import analyzer

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """Upload and analyze face for emotions, age, gender."""
    return render_template('analysis.html')

@bp.route('/upload', methods=['POST'])
def upload_and_analyze():
    """Handle image upload and run DeepFace analysis."""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Save file with unique name
        extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{extension}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Run analysis
        result = analyzer.analyze(filepath)
        
        # Handle engine errors (e.g., model loading issues)
        if 'error' in result:
             flash(f"Analysis Engine Error: {result['error']}")
             return redirect(url_for('analysis.index'))
        
        # Handle cases where no faces were detected
        if not result.get('faces') or result.get('count', 0) == 0:
            flash("No faces detected in the provided image.")
            return redirect(url_for('analysis.index'))
        
        return render_template('analysis_result.html', result=result, image=unique_filename)

@bp.route('/live')
def live_view():
    """Render the live webcam analysis view."""
    return render_template('live.html')

@bp.route('/live_frame', methods=['POST'])
def live_frame():
    """Handle base64 frame from webcam and return analysis."""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "No image data"}), 400
        
        # Robust base64 extraction
        image_b64 = data['image']
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
            
        image_data = base64.b64decode(image_b64)
        
        # Save temp frame (with enhancement)
        temp_filename = f"live_{uuid.uuid4()}.jpg"
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], temp_filename)
        
        # Save frame as-is — aggressive sharpening/contrast hurts gender CNN accuracy
        img = Image.open(BytesIO(image_data))
        img = img.convert("RGB")
        img.save(temp_path, "JPEG", quality=95)
        
        # Set accuracy backend
        # Always use the shared opencv-based analyzer (no retinaface weights needed)
        result = analyzer.analyze(temp_path)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({"results": result})
        
    except Exception as e:
        current_app.logger.error(f"Live Frame Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    return render_template('analysis.html', error="Invalid file type.")

@bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for asynchronous analysis (webcam or direct upload)."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{extension}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        result = analyzer.analyze(filepath)
        return jsonify(result)
    
    return jsonify({"error": "Invalid format"}), 400
