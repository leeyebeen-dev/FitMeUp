from flask import Flask, render_template, request, redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['user_info'] = request.form
        return redirect(url_for('main_page'))
    return render_template('index.html')

@app.route('/main', methods=['GET'])
def main_page():
    user_info = session.get('user_info', {})
    
    if not all(key in user_info for key in ['name', 'age', 'gender', 'height', 'weight', 'ability', 'preference']):
        return redirect(url_for('index', _external=True, _scheme='https', message="모든 사용자 정보를 채워주세요."))
    
    exercise_plan = """
    안녕하세요, {name}님. 
    당신을 위한 개인 맞춤형 운동 계획을 제안해드립니다:
    1. 월요일: 러닝 30분
    2. 화요일: 스트레칭 15분, 요가 30분
    3. 수요일: 러닝 30분
    4. 목요일: 스트레칭 15분, 피트니스 30분
    5. 금요일: 러닝 30분
    6. 토요일: 스트레칭 15분, 요가 30분
    7. 일요일: 휴식

    이 운동 계획은 {name}님의 개인적인 운동 능력과 선호하는 운동을 고려하여 작성되었습니다. 
    하지만 이 계획은 일반적인 조언일 뿐, 개인의 건강 상태나 피트니스 수준에 따라 적절한 조정이 
    필요할 수 있습니다. 
    운동을 시작하기 전에는 항상 의사나 전문가와 상의하시는 것이 좋습니다.
    """.format(name=user_info['name'])
    return render_template('main.html', user_info=user_info, exercise_plan=exercise_plan)

   
   # GPT 연동 시 사용하는 코드
    '''
    openai.api_key = your_openai_key

    @app.route('/main', methods=['GET'])
    def main_page():
        user_info = session.get('user_info', {})
        
        if not all(key in user_info for key in ['name', 'age', 'gender', 'height', 'weight', 'ability', 'preference']):
            return redirect(url_for('index', _external=True, _scheme='https', message="모든 사용자 정보를 채워주세요."))
        
        chat_model = "gpt-3.5-turbo"
        messages = [
            {
                'role': 'system',
                'content': '당신은 헬스 트레이너이면서 건강에 대해 잘 아는 사람입니다. 초보자도 쉽게 접근할 수 있는 정보를 제공해주세요.'
            },
            {
                'role': 'user',
                'content': f"""{user_info['name']}님의 정보:
    - 나이: {user_info['age']}
    - 성별: {user_info['gender']}
    - 키: {user_info['height']}
    - 몸무게: {user_info['weight']}
    - 운동 능력: {user_info['ability']}
    - 선호하는 운동: {user_info['preference']}
    이 정보를 바탕으로 맞춤 운동 계획을 제안해주세요."""
            }
        ]

        response = openai.ChatCompletion.create(
            model=chat_model,
            messages=messages
        )
        exercise_plan = response['choices'][0]['message']['content']
        return render_template('main.html', user_info=user_info, exercise_plan=exercise_plan)
    '''   

if __name__ == '__main__':
    app.run(debug=True, port=8080)

