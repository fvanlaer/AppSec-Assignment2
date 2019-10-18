import os
import sys
from flask import Flask, render_template

sys.path.append(os.path.dirname(__name__))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()