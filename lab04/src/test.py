from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get():
    return "sucsess"

@app.route('/test', methods=['GET'])
def test():
    abort(400)

@app.route('/post', methods=['POST'])
def post():
    data = request.form
    return data.get("key")

if __name__ == '__main__':
    app.run(debug=True)
