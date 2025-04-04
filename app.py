from travel import create_app, db
import os

# Expose create_app for the Flask CLI
create_app = create_app

app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)