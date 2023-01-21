from flask import request

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['POST'])
def test():

    scoreList = []
    numericalValues = ["Mostly Disagree",
                       "Slightly Disagree", "Slightly Agree", "Mostly Agree"]

    network = []

    personalities = ['logical{}', 'spatial{}',
                     'interpersonal{}', 'intrapersonal{}']

    if request.method == "POST":
        print("if is working")
        scoreChoco = 0
        score = 0
        form = request.form.get("form1")
        sum = 0

    for i in personalities:

        score = 0
        for j in range(1, 6):
            choco = request.form.get((i.format(j)))

            if choco in numericalValues:
                score += numericalValues.index(choco)+1

            print(score, "  ", i)
            scoreList.append(score)
    print(scoreList)

    # return render_template("/ug-pg/te/result_te.html")
if __name__ == '__main__':
    app.run(debug=True)
