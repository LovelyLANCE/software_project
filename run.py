import os
from emall import create_app

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    app = create_app()
    app.run(debug=True, host=host, port=8082)