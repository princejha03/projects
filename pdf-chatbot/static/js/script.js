document.getElementById('uploadForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    alert(data.message);
};

async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const messagesDiv = document.getElementById('messages');
    if (userInput.trim() === "") return;

    messagesDiv.innerHTML += `<div>You: ${userInput}</div>`;
    document.getElementById('userInput').value = '';

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });
    const data = await response.json();
    messagesDiv.innerHTML += `<div>Bot: ${data.response}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
