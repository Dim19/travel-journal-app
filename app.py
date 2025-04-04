from travel import create_app, db
import os

# Expose create_app for the Flask CLI
create_app = create_app

app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)