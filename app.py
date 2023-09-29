import os.path
import yaml

from flask import Flask, render_template, request, jsonify
from helper import *

app = Flask(__name__)

resources_path = os.path.join(os.getcwd(), 'resources')

explainer = get_explainer()
summary_plot = get_summary_plot(explainer)


@app.route('/')
def index():
    inputs_file = os.path.join(resources_path, 'inputs.yaml')

    with open(inputs_file, 'r') as f:
        features = yaml.safe_load(f)

    return render_template('index.html', features=features)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    prep_data = preprocess_data(data)

    prediction = predict(prep_data)

    force_plot, explanation = get_local_explanations(explainer, prep_data, prediction)

    plots = [
        ('html', force_plot),
        ('img', summary_plot)
    ]

    result = render_template('result.html', loan_status=prediction[0], explanation=explanation, plots=plots)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
