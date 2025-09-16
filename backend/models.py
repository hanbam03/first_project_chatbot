from typing import List, Optional
from pydantic import BaseModel
# Pydantic 모델 정의
# 회원가입
class User_Info(BaseModel):
    user_id: str
    password: str


# 회원가입 성공 응답
class Sign_Up_Success(BaseModel):
    message: str
    user_id: str


# 로그인
class User_Login(BaseModel):
    user_id: str
    password: str


# 채팅
# 유저의 요청!
class User_Chat(BaseModel):
    user_id: str
    user_message: str
    history: Optional[List[dict]] = None


# 서버의 응답 -> 봇이 답변
class Bot_Chat(BaseModel):
    user_message: str
    bot_response: str


# 채팅 기록 조회
class Chat_History(BaseModel):
    user_id: str
    history: List[Bot_Chat]