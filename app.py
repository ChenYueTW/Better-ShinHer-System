from flask import Flask
from absentation import absentation_app
from curriculum import curriculum_app
from exam import exam_app
from moral import moral_app

app = Flask(__name__)

app.register_blueprint(absentation_app)
app.register_blueprint(curriculum_app)
app.register_blueprint(exam_app)
app.register_blueprint(moral_app)

if __name__  == '__main__':
    app.run(host="0.0.0.0", port=8000)