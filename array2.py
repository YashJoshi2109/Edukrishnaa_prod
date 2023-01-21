import json
from unittest import result

from flask import request

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/tenth/test2page.html')


@app.route('/test', methods=['POST'])
def test():

    output = request.get_json()
    print(output)  # This is the output that was stored in the JSON within the browser
    print(type(output))
    # this converts the json output to a python dictionary
    result = json.loads(output)
    print(result)  # Printing the new dictionary
    print(type(result))  # this shows the json converted as a python dictionary
    return result
# d=test

# print(d)


if __name__ == '__main__':
    app.run(debug=True)
