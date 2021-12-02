from detec_libApp import create_app
from flask_cors import CORS

app = create_app()
CORS(app)
print(app.__class__.__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5001", debug=True)