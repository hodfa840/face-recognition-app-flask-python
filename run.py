from app import create_app
import os

app = create_app()

# PRODUCTION FIX: Serve static files through Gunicorn for Hugging Face Spaces
# This ensures that uploaded biometric images are displayed correctly (fixes 200 0 error)
try:
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static': os.path.join(app.root_path, 'static')
    })
except Exception as e:
    print(f"Middleware not configured: {e}")

if __name__ == "__main__":
    # In development, use debug=True
    # For production, use a WSGI server like Gunicorn
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
