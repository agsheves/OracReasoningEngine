document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatWindow = document.getElementById('chat-window');
    const exportButton = document.getElementById('export-chat');

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'system-message');

        const content = document.createElement('p');
        content.textContent = message;
        messageElement.appendChild(content);

        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function handleInput() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, true);
            socket.emit('simulate', { input: message });
            messageInput.value = '';
        }
    }

    function exportChat() {
        const messages = [];
        chatWindow.querySelectorAll('.message').forEach(msg => {
            const isUser = msg.classList.contains('user-message');
            const content = msg.textContent;
            messages.push(`${isUser ? 'User' : 'System'}: ${content}\n`);
        });

        const chatText = messages.join('\n');
        const blob = new Blob([chatText], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'worldsim-chat-export.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }

    sendButton.addEventListener('click', handleInput);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleInput();
        }
    });

    exportButton.addEventListener('click', exportChat);
});