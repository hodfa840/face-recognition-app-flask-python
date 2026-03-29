from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Redirect to dashboard or render home."""
    return render_template('dashboard.html')

@bp.route('/dashboard')
def dashboard():
    """Main dashboard with use case selection."""
    return render_template('dashboard.html')

@bp.route('/base')
def legacy_base():
    return redirect(url_for('main.dashboard'))

@bp.route('/faceapp')
def legacy_faceapp():
    return redirect(url_for('analysis.index'))

@bp.route('/faceapp/gender', methods=['GET', 'POST'])
def legacy_gender():
    return redirect(url_for('analysis.index'))

@bp.route('/about')
def about():
    """Project description and CV highlights."""
    return render_template('about.html')
