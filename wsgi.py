from app import app
 
# When a Python script is run directly, __name__(filename like run) is set to "__main__"
if __name__ == "__main__":
  # This line initializes the database by creating all the tables defined by the SQLAlchemy models and ensures that all the tables are created before the application starts 
  db.create_all()
  # This line starts the Flask server
  app.run(debug=True)