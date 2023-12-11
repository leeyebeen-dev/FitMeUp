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
    {name}님을 위한 개인 맞춤형 운동 계획과 루틴을 제안해드립니다!
    1. 걷기 운동 계획
    걷기 운동을 선호하시므로, 매일 걷기 운동을 포함한 루틴을 계획해보겠습니다. 
    걷기는 심장 건강을 유지하고 체력을 향상시키는 데 도움이 되며, 일상 생활에서 쉽게 실천할 수 
    있는 운동입니다. 매일 아침 30분간 빠르게 걷는 것으로 시작해보세요.
    2. 스트레칭
    걷기 운동 전후에는 반드시 스트레칭을 해주세요. 스트레칭은 근육과 관절을 풀어주어 부상을 
    예방하고, 운동 효과를 높여줍니다.
    3. 근력 운동
    운동 능력이 '하'라고 하셨으므로, 부담 없는 근력 운동을 추천드립니다. 
    웨이트를 사용하지 않는 라이트한 스쿼트, 런지 등의 운동을 하루 15분 정도 실시해보세요.
    4. 식사 계획
    운동만큼 중요한 것이 식사입니다. 단백질이 풍부한 식사를 하여 근육 회복을 도와주세요.

    이 루틴은 {name}님의 개인적인 운동 능력과 선호하는 운동을 고려하여 작성되었습니다. 
    아래는 유튜브에서 괜찮은 운동 루틴 영상을 몇 개 찾아봤습니다. 이것들을 참고하면 좋을 것 
    같아요.
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

