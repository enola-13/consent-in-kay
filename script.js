// Store current message
let currentMessage = "";

// Handle Send Button
function handleSend() {
    let input = document.getElementById("messageInput");
    let text = input.value;

    if (!text) return;

    currentMessage = text;

    let result = analyzeMessage(text);

    // If risky → show popup
    if (result !== "Safe") {
        showPopup(result, text);
    } else {
        addMessage(text, "user");

        let aiReply = generateAIResponse(text);
        addMessage(aiReply, "ai");
    }

    input.value = "";
}

// Analyze message (basic detection)
function analyzeMessage(text) {
    let email = /\S+@\S+\.\S+/;
    let phone = /\d{8}/;
    let password = /password|pass|pwd|1234/i;

    if (password.test(text)) return "Sensitive";
    if (email.test(text) || phone.test(text)) return "Personal";

    return "Safe";
}

// Show popup
function showPopup(type, text) {
    let popup = document.getElementById("popup");
    let popupText = document.getElementById("popupText");

    popupText.innerText =
        `⚠️ You are about to share ${type} data\n\n` +
        `.  Detected: ${text}\n\n` +
        `.  This will be sent to KAY AI Assistant\n\n` +
        `.  This data may be used to generate responses and improve the system.\n\n` +
        `Do you want to continue?`;

    popup.classList.remove("hidden");
}

// Confirm send (Allow)
function confirmSend() {
    addMessage(currentMessage, "user");

    let aiReply = generateAIResponse(currentMessage);
    addMessage(aiReply, "ai");

    closePopup();
}

// Close popup (Deny)
function closePopup() {
    document.getElementById("popup").classList.add("hidden");
}

// Add message to chat
function addMessage(text, sender) {
    let chat = document.getElementById("chatBox");

    let msg = document.createElement("div");
    msg.classList.add("message", sender);

    msg.innerText = text;

    chat.appendChild(msg);

    chat.scrollTop = chat.scrollHeight;
}

// AI Logic
function generateAIResponse(text) {
    let msg = text.toLowerCase().trim();
    if (
    msg === "hi" ||
    msg === "hello" ||
    msg === "hey"
) {
    return "👋 Hi there! How may I help you?";
}
    // List type queries
    if (msg.includes("book")) {
    return `📚 Here are 5 great books you can read:

1. Atomic Habits  
2. The Alchemist  
3. Rich Dad Poor Dad  
4. Ikigai  
5. The Psychology of Money  

Let me know if you want books in a specific category!`;
}

    // Question
    if (msg.includes("?")) {
        return "🤖 That's an interesting question! I'll try to help you.";
    }

    // Default reply
    return `💬 I See you are asking: "${text}". `;
}
document.getElementById("messageInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        handleSend();
    }
});
let input = document.getElementById("messageInput");

input.addEventListener("input", function () {
    let text = input.value;
    let result = analyzeMessage(text);

    // Remove old colors
    input.classList.remove("safe", "personal", "sensitive");

    // Apply new color
    if (result === "Safe") {
        input.classList.add("safe");
    } else if (result === "Personal") {
        input.classList.add("personal");
    } else if (result === "Sensitive") {
        input.classList.add("sensitive");
    }
});