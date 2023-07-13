from injectors.flask import FlaskContainer

app = FlaskContainer.app

if __name__ == "__main__":
    FlaskContainer.run()
