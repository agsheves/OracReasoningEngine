document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatWindow = document.getElementById('chat-window');
    
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
    
    sendButton.addEventListener('click', handleInput);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleInput();
        }
    });
});
