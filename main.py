from travel import create_app

# Initialise Web App
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)