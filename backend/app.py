from app import create_app
from mongoengine import connect

if __name__ == '__main__':
    connect('aigis')
    app = create_app()
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
