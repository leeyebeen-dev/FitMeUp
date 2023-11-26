import openai

openai.api_key = 'your-api-key'

def chat_with_gpt3(user_info):
    # 사용자 정보를 채팅 메시지로 변환
    messages = [
        {"role": "system", "content": "You are a helpful trainer."},
    ]
    for key, value in user_info.items():
        messages.append({"role": "user", "content": f"My {key} is {value}"})
    messages.append({"role": "user", "content": "What should be my fitness plan based on my health, ability, gender, and age?"})

    # GPT-3와의 채팅 생성
    response = openai.ChatCompletion.create(
      model="text-davinci-002",
      messages=messages
    )

    # 채팅 응답에서 마지막 메시지(모델의 답변) 반환
    plan = response['choices'][0]['message']['content']
    return plan
