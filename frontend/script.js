// HTML 페이지가 완전히 로드된 후 스크립트 실행
document.addEventListener("DOMContentLoaded", function() {
    
    let userId = null; // 로그인 성공 시 user_id를 저장할 변수

    // --회원가입 버튼--
    const registerBtn = document.getElementById("register-btn");
    registerBtn.addEventListener("click", function(){
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const formData = new FormData();
        formData.append("user_id", username);
        formData.append("password", password);

        fetch("http://localhost:8000/users", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail);
                });
            }
        })
        .then(data => {
            alert("회원가입 성공: " + data.message);
        })
        .catch(error => {
            alert("오류: " + error.message);
        });
    });

    // --로그인 버튼--
    const loginBtn = document.getElementById("login-btn");
    loginBtn.addEventListener("click", function() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const formData = new FormData();
        formData.append("user_id", username);
        formData.append("password", password);

        fetch("http://localhost:8000/login", {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail);
                });
            }
        })
        .then(data => {
            userId = data.user_id; 
            
            document.getElementById("login-section").style.display = "none";
            document.getElementById("chat-section").style.display = "block";
        })
        .catch(error => {
            alert("오류: " + error.message);
        });
    });

    // -- 전송 버튼 --
    const sendBtn = document.getElementById("send-button");
    const messageInput = document.getElementById("message-input");
    const messageBox = document.getElementById("message");

    if (sendBtn) {
        sendBtn.addEventListener("click", async function() {
            const message = messageInput.value;
            
            if (message.trim() !== "") {
                const userMessageDiv = document.createElement("div");
                userMessageDiv.classList.add("user-message");
                userMessageDiv.textContent = message;
                messageBox.appendChild(userMessageDiv);
                messageInput.value = "";
                messageBox.scrollTop = messageBox.scrollHeight;
                
                const botLoadingDiv = document.createElement("div");
                botLoadingDiv.classList.add("bot-message", "loading");
                botLoadingDiv.textContent = "답변을 준비하고 있습니다...";
                messageBox.appendChild(botLoadingDiv);
                messageBox.scrollTop = messageBox.scrollHeight;

                try {
                    const historyResponse = await fetch(`http://localhost:8000/chats/history/${userId}`);
                    if (!historyResponse.ok) {
                        throw new Error("채팅 기록을 불러오는 데 실패했습니다.");
                    }
                    const historyData = await historyResponse.json();
                    
                    const chatData = {
                        user_id: userId,
                        user_message: message,
                        history: historyData.history
                    };

                    const chatResponse = await fetch("http://localhost:8000/chats", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(chatData)
                    });
                    
                    if (!chatResponse.ok) {
                        const errorData = await chatResponse.json();
                        throw new Error(errorData.detail);
                    }
                    
                    const data = await chatResponse.json();

                    messageBox.removeChild(botLoadingDiv);
                    
                    const botMessageDiv = document.createElement("div");
                    botMessageDiv.classList.add("bot-message");
                    botMessageDiv.textContent = data.bot_response;
                    messageBox.appendChild(botMessageDiv);
                    
                    messageBox.scrollTop = messageBox.scrollHeight;

                } catch (error) {
                    if (messageBox.contains(botLoadingDiv)) {
                        messageBox.removeChild(botLoadingDiv);
                    }
                    console.error("챗봇 통신 오류:", error);
                    alert("챗봇과 통신 중 오류가 발생했습니다: " + error.message);
                }
            }
        });
    } else {
        console.log("전송 버튼을 찾을 수 없음");
    }
    // 채팅 기록 보기 버튼 (전송 버튼 코드 다음에 추가)
const historyBtn = document.getElementById("history-btn");
if (historyBtn) {
    historyBtn.addEventListener("click", async function() {
        try {
            const response = await fetch(`http://localhost:8000/chats/history/${userId}`);
            const data = await response.json();
            
            // 간단하게 alert으로 표시
            let historyText = "=== 채팅 기록 ===\n";
            data.history.forEach(chat => {
                historyText += `사용자: ${chat.user_message}\n`;
                historyText += `챗봇: ${chat.bot_response}\n\n`;
            });
            
            alert(historyText || "채팅 기록이 없습니다.");
        } catch (error) {
            alert("채팅 기록을 불러오는데 실패했습니다.");
        }
    });
}
});