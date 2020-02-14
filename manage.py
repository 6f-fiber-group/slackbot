import os
import json
from flask import render_template
from backend import app

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/hello')
def hello():
  return json.dumps({
    "text": "hello"
  })

if __name__ == "__main__":
  host = os.environ.get("HOST", "127.0.0.1")
  port = int(os.environ.get('PORT', 5000))
  debug = False

  app.run(host=host, port=port, debug=debug)

  # ssl_context=(
  #   os.environ.get("SERVER_CERTIFICATE"),
  #   os.environ.get("SERVER_PRIVATE_KEY")
  #   )

  # print(ssl_context)

  # import ssl
  # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  # print(os.environ.get("SERVER_CERTIFICATE"),
  #   os.environ.get("SERVER_PRIVATE_KEY"))
  # ssl_context.load_cert_chain(
  #   os.environ.get("SERVER_CERTIFICATE"),
  #   os.environ.get("SERVER_PRIVATE_KEY")
    # )
  # if os.getenv("FLASK_APP_ENV") == "production":
  #   app.run(host=host, port=port, debug=debug)
  # else:
  #   app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)