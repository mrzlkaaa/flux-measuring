import os
from flask import Flask, render_template

name = "greetings"

python_folder, _ = os.path.split(os.getcwd())
template_folder_path = os.path.join(python_folder, "templates")
static_folder_path = os.path.join(python_folder, "static", name)

app = Flask(__name__)
app.template_folder = template_folder_path
app._static_folder = static_folder_path

#! use lambda func instead!
img_count = lambda x: [i for i in os.listdir(app._static_folder) if x in i]

@app.route('/')
@app.route('/home')
def home():
    wires, foils = img_count("wire"), img_count("foil")
    return render_template(f"{name}/home.html", wires=wires, foils=foils)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5002", debug=True)