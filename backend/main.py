# 필요한 라이브러리 가져오기
import json
from fastapi import FastAPI, Form, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from models import User_Info, Sign_Up_Success, User_Login, User_Chat, Bot_Chat, Chat_History
import requests

app = FastAPI(title="부트캠프 ChatGPT API 서버", version="1.0.0")

BOOTHCAMP_API_URL = "https://dev.wenivops.co.kr/services/openai-api"

# CORS 설정
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    # 프론트엔드 포트 번호
    "http://127.0.0.1:5500"
]

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 허용할 오리진 목록
    allow_credentials=True,       # 쿠키 등 자격 증명 허용
    allow_methods=["*"],          # 모든 HTTP 메소드(GET, POST 등) 허용
    allow_headers=["*"],          # 모든 HTTP 헤더 허용
)

# 메모리 저장용
users_db = {}
chat_history = {}


# request_bot_api
# request_bot_api 함수
def request_bot_api(user_message: str, history: list = None) -> str:
    # 챗봇의 성격을 정의하는 시스템 프롬프트 (유지)
    system_prompt = """
    당신은 쿨하고 시크한 음악 전문가입니다.
    사용자에게 무심하지만 정확하게 음악을추천해주세요.
    추천할 때는 곡명, 아티스트를 포함해서 설명해주세요.
    키워드로 추천 요청이 온 경우, 해당 키워드를 기준으로 선곡한 이유도 간단히 설명해주세요.
    """
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # 대화 맥락 유지
    if history:
        for chat in history:
            messages.append({"role": "user", "content": chat['user_message']})
            messages.append({"role": "assistant", "content": chat['bot_response']})

    messages.append({"role": "user", "content": user_message})

    data = {
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(BOOTHCAMP_API_URL, json=messages)

    # 디버깅용 출력 추가
    print("API 응답 상태코드:", response.status_code)
    print("API 응답 내용:", response.json())

    if response.status_code == 200:
        response_data = response.json()
        # 안전한 응답 처리
        try:
            return response_data['choices'][0]['message']['content']
        except KeyError as e:
            print(f"응답 구조 오류: {e}")
            print("실제 응답:", response_data)
            return "죄송합니다. 음악 추천을 처리하는 중 오류가 발생했습니다."
    else:
        print(f"API 호출 실패: {response.status_code}")
        return "음악 추천 서비스가 일시적으로 이용 불가합니다."


# ---엔드포인트---
@app.get("/")
def root():
    return {"message": "음악 추천 챗봇 API"}


# 회원가입 엔드포인트
@app.post("/users")
def sign_up(user_id: str = Form(...), password: str = Form(...)):
    #기본 검증
    if not user_id.strip() or not password.strip():
        raise HTTPException(status_code=400, detail="아이디와 비밀번호는 공백일 수 없습니다")

    # 중복 아이디 확인
    if user_id in users_db:
        raise HTTPException(status_code=400, detail="이미 사용중인 아이디입니다.")
   
    users_db[user_id] = password
    return Sign_Up_Success(message="회원가입을 축하드립니다!", user_id= user_id)


# 로그인 엔드포인트
@app.post("/login")
def login(user_id: str = Form(...), password: str = Form(...)):
    # 사용자 아이디 존재 & 비밀번호 일치 확인
    if (user_id not in users_db or users_db[user_id] != password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 일치하지 않습니다.")
    
    # 성공 시 응답
    return {"message": "로그인 성공", "user_id": user_id}

# 채팅 기록 조회 엔드포인트
@app.get("/chats/history/{user_id}")
def get_chat_history(user_id: str):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")
    
    return {"history": chat_history.get(user_id, [])}

# 채팅 엔드포인트
@app.post("/chats")
def chat(user_chat: User_Chat):
    if user_chat.user_id not in users_db:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")
    
    # 챗봇 API에 history 데이터를 함께 전달
    # request_bot_api에 history 인자를 전달하도록 수정
    bot_response = request_bot_api(user_chat.user_message, history=user_chat.history)

    # 특정 사용자의 chat_history 초기화
    if user_chat.user_id not in chat_history:
         chat_history[user_chat.user_id]= []

    # 객체 생성으로 저장
    chat_logs = Bot_Chat(
        user_message=user_chat.user_message,
        bot_response=bot_response
    )

    # chat_logs 객체를 딕셔너리로 변환하여 저장
    chat_history[user_chat.user_id].append(chat_logs.dict())
    
    # 응답 반환
    return chat_logs