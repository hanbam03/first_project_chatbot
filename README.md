# :musical_note::robot: 음악 추천 챗봇
ChatGPT API를 활용한 개인화된 음악 추천 서비스
## 1. 프로젝트 설명(어떤 기능이 있는가)
ChatGPT API를 이용하여 간단한 인공지능 챗봇을 구현해보는 프로젝트입니다.

**주요 기능**
- 사용자 회원가입/로그인
- AI 챗봇과 실시간 음악 추천 대화
- 사용자별 채팅 기록 저장
- 반응형 채팅 인터페이스

## :wrench: 기술 스택

**백엔드**
- FastAPI (Python)
- 메모리 기반 데이터 저장
- ChatGPT API 연동

**프론트엔드**
- HTML5, CSS3, JavaScript
- Fetch API를 통한 비동기 통신

**API**
- ChatGPT API

## :zap: 주요 구현 기능

### 1. :closed_lock_with_key: 사용자 인증 시스템
- 회원가입 시 입력값 검증 (아이디/비밀번호 형식 체크)
- 중복 아이디 방지
- 로그인 성공 시 채팅 화면으로 자동 전환

### 2. :robot: 음악 추천 챗봇
- "쿨하고 시크한 음악 전문가" 설정
- 키워드, 아티스트, 가사 기반 추천
- 추천 이유 상세 설명 제공
- 실시간 대화형 인터페이스

### 3. :speech_balloon: 채팅 기록 관리
- 사용자별 대화 내역 분리 저장
- 채팅 기록 조회 기능
- 서버 재시작 전까지 데이터 유지

### 4. :art: 사용자 경험 최적화
- 메시지 전송 후 입력창 자동 초기화
- 사용자/챗봇 메시지 시각적 구분
- 로딩 상태 표시

## API 엔드포인트

```
POST /users          # 회원가입
POST /login          # 로그인
POST /chats          # 챗봇 대화
GET /chats/history/{user_id}  # 채팅 기록 조회
```

## ❓ 실행하는 방법

### 1. 라이브러리와 가상환경 설치
```
# 가상환경 생성
python -m venv venv
.\venv\Scripts\activate

# 라이브러리 설치
pip install fastapi uvicorn requests python-multipart
```
### 2. 서버 실행
```
uvicorn main:app --reload
```

### 접속
- 백엔드 API: http://localhost:8000
- 백엔드 문서: http://localhost:8000/docs  
- 프론트엔드: http://localhost:5500 (Live Server 사용시)

## 구현 결과

- **회원가입/로그인**: 입력 검증 및 에러 처리 완료
- **채팅 기능**: 실시간 AI 음악 추천 대화 구현
- **데이터 관리**: 사용자별 채팅 기록 분리 저장
- **UI/UX**: 직관적인 채팅 인터페이스 제공

## 향후 개선 계획

- 구체적인 컨셉의 챗봇 설정
- 데이터베이스 연동을 통한 영구 데이터 저장
- 로그아웃 기능 및 세션 관리
- 채팅 기록 UI 개선
