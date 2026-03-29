from flask import Blueprint, render_template, request, flash, current_app, jsonify, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from ..utils.ml_engine import analyzer

bp = Blueprint('recognition', __name__, url_prefix='/recognition')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/verify', methods=['GET', 'POST'])
def verify_face():
    """Compare two images to see if they are the same person."""
    if request.method == 'POST':
        if 'img1' not in request.files or 'img2' not in request.files:
            flash('Two images are required.')
            return redirect(request.url)
        
        img1 = request.files['img1']
        img2 = request.files['img2']
        
        if img1 and allowed_file(img1.filename) and img2 and allowed_file(img2.filename):
            # Save files with unique names
            u1 = f"v1_{uuid.uuid4()}.{img1.filename.rsplit('.', 1)[1].lower()}"
            u2 = f"v2_{uuid.uuid4()}.{img2.filename.rsplit('.', 1)[1].lower()}"
            
            p1 = os.path.join(current_app.config['UPLOAD_FOLDER'], u1)
            p2 = os.path.join(current_app.config['UPLOAD_FOLDER'], u2)
            
            img1.save(p1)
            img2.save(p2)
            
            # Run DeepFace verify
            # 'VGG-Face' is a good default, also 'Facenet'
            model_name = request.form.get('model', 'VGG-Face')
            result = analyzer.verify(p1, p2, model_name=model_name)
            
            if 'error' in result:
                # If error occurs (like weights missing), show error on the verification page
                flash(f"Verification Engine Error: {result['error']}")
                return redirect(request.url)
            
            return render_template('verification_result.html', result=result, img1=u1, img2=u2)
        
        flash('Invalid image format.')
        return redirect(request.url)

    return render_template('verification.html')

@bp.route('/identify', methods=['GET', 'POST'])
def identify_face():
    """Find a face in a database of known faces."""
    # (Optional: If the user provides a DB directory, identify the person.)
    # For CV, we could pre-load a small DB of people.
    return render_template('identify.html')
