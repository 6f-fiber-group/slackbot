import os
from bot_app import app

@app.route('/')
def index():
  return 'Hello World!'

if __name__ == "__main__":
  app.run(
    host = os.environ.get("HOST", "127.0.0.1"),
    port = int(os.environ.get('PORT', 5000)),
    debug = False
  )