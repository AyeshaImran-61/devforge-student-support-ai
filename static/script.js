const chat = document.getElementById("chat");
const input = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");

// Send button
sendBtn.addEventListener("click", sendMessage);

// Press Enter to send
input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto resize textarea
input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
});

// New Chat button
document.getElementById("newChat").addEventListener("click", () => {
    chat.innerHTML = `
        <div class="welcome">
            <div class="ai-avatar">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="welcome-text">
                <h2>Hello 👋</h2>
                <p>
                    I'm your DEVFORGE Student Support AI.
                    Ask me anything about Python, FastAPI,
                    LangGraph, GitHub, Render, AI Engineering,
                    or your internship.
                </p>
            </div>
        </div>
    `;
});

async function sendMessage() {

    const message = input.value.trim();

    if (!message) return;

    // Remove welcome message
    const welcome = document.querySelector(".welcome");
    if (welcome) welcome.remove();

    // User message
    chat.innerHTML += `
        <div class="message user">
            <div class="bubble">
                ${message}
            </div>
        </div>
    `;

    // Thinking animation
    chat.innerHTML += `
        <div class="message bot" id="thinking">
            <div class="bubble">
                ⏳ Thinking...
            </div>
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    input.value = "";
    input.style.height = "auto";

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        document.getElementById("thinking").remove();

        chat.innerHTML += `
            <div class="message bot">
                <div class="bubble">
                    ${marked.parse(data.response)}
                </div>
            </div>
        `;

        // Highlight code blocks
        document.querySelectorAll("pre code").forEach((block) => {
            hljs.highlightElement(block);
        });

    } catch (error) {

        const thinking = document.getElementById("thinking");
        if (thinking) thinking.remove();

        chat.innerHTML += `
            <div class="message bot">
                <div class="bubble">
                    ❌ Unable to connect to the server.
                </div>
            </div>
        `;
    }

    chat.scrollTop = chat.scrollHeight;
}