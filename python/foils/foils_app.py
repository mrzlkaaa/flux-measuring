from foilsApp import create_app

app = create_app()
# db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)