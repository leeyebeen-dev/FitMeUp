from flask import Flask, render_template, request
from my_gpt import generate_plan

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = {
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'health': request.form.get('health'),
            'ability': request.form.get('ability'),
            'goal': request.form.get('goal')
        }
        plan = generate_plan(user_info)
        return render_template('plan.html', user_info=user_info, plan=plan)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
