import os
import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def load_data():
    file_path = 'data/climb.txt'
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')

        # Process each row
        for row in reader:
            word_list.append(row[3])
            word_dict[f"{row[0]}_{row[1]}_{row[2]}"] = row[3]


word_list = []
word_dict = {}
load_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit-guess', methods=['POST'])
def submit_guess():
    # Get the JSON data from the request
    data = request.get_json()
    guess = data.get('guess', '').lower()

    # Failed to load word list
    if not word_list:
        return jsonify({"status": "error", "message": "server error (cannot read data)"})

    # Validate the input
    error_msg = validate_input(guess)

    if error_msg is not None:
        return jsonify({"status": "error", "message": error_msg})

    results = []
    next = 'climb'
    round = 6
    word_str = 'climb'

    while next:
        next, word_str, json_output = determine(next, guess, word_str, round)
        round = round - 1
        results.append(json_output)

    if round < 0:
        return jsonify({"status": "error", "message": "Server error (cannot solve)"})

    while round > 0:
        results.append({"word": "", "result": []})
        round = round - 1

    return jsonify({"status": "success", "message": "", "results": results})


def validate_input(guess: str) -> str:
    if len(guess) != 5:
        return "Not 5 letters"

    if not guess in word_list:
        return "Not a word in the list"


def determine(input: str, answer: str, word_str: str, round: int):
    if round <= 0:
        return None, None, {"word": "", "result": []}

    if input == answer:
        return None, word_str, {"word": input.upper(), "result": ["Green"] * 5}

    result_array = calculate_state(input, answer)
    result_string = ",".join(result_array)
    result_key = f"{round-1}_{word_str}_{result_string}"
    next = word_dict[result_key]

    if not next:
        raise Exception("cannot solve")

    return next, f"{word_str},{next}", {"word": input.upper(), "result": result_array}


def calculate_state(input: str, answer: str):
    result = ["Gray"] * 5
    input_used = [False] * 5
    answer_used = [False] * 5

    for i in range(0, 5):
        if input[i] == answer[i]:
            input_used[i] = True
            answer_used[i] = True
            result[i] = "Green"

    for i in range(0, 5):
        if answer_used[i]:
            continue

        for j in range(0, 5):
            if input_used[j]:
                continue
            if input[j] == answer[i]:
                input_used[j] = True
                answer_used[i] = True
                result[j] = "Yellow"
                break

    return result


# register template context handler


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
