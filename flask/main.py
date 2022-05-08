from flask import Flask
from backend.main_page import mainBP

app = Flask(__name__)


app.register_blueprint(mainBP, url_prefix="")

app.secret_key = "sxchahsdiusd324wdasd"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", ssl_context=('certificate/cert.pem', 'certificate/key.pem'))