from app import create_app #importing create application function that stores our app instance

app = create_app()

if __name__ == "__main__":
     app.run(debug=True)
