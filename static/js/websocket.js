let socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('simulation_response', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system-message');

    try {
        const response = JSON.parse(data.response);
        const content = document.createElement('div');
        content.classList.add('message-content');

        // Create timestamp element
        const timestamp = document.createElement('div');
        timestamp.classList.add('message-timestamp');
        timestamp.textContent = new Date(response.timestamp).toLocaleTimeString();
        messageElement.appendChild(timestamp);

        // Add copy button
        const copyButton = document.createElement('button');
        copyButton.classList.add('copy-button');
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.onclick = () => {
            const textToCopy = response.type === 'simulation_response' ? response.response : response.error;
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    copyButton.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                    }, 2000);
                })
                .catch(err => console.error('Failed to copy:', err));
        };
        messageElement.appendChild(copyButton);

        // Format and display the main response
        if (response.type === 'simulation_response') {
            content.innerHTML = response.response.replace(/\n/g, '<br>');
        } else if (response.type === 'error') {
            content.innerHTML = `Error: ${response.error}`;
            messageElement.classList.add('error-message');
        }

        messageElement.appendChild(content);
    } catch (error) {
        console.error('Error parsing response:', error);
        const content = document.createElement('p');
        content.textContent = data.response;
        messageElement.appendChild(content);
    }

    const chatWindow = document.getElementById('chat-window');
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Hide loading indicator when response is received
    window.setLoading(false);
});

socket.on('simulation_error', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'error-message');
    messageElement.textContent = 'Error: ' + data.error;
    document.getElementById('chat-window').appendChild(messageElement);
    window.setLoading(false);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    window.setLoading(false);
});

// Export chat functionality
document.getElementById('export-chat')?.addEventListener('click', () => {
    const messages = [];
    document.querySelectorAll('.message').forEach(msg => {
        const timestamp = msg.querySelector('.message-timestamp')?.textContent || '';
        const content = msg.querySelector('.message-content')?.textContent || msg.textContent;
        const isUser = msg.classList.contains('user-message');
        messages.push(`[${timestamp}] ${isUser ? 'User' : 'System'}: ${content}\n`);
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
});

// Add keyboard shortcut for copying message content
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
        const selection = window.getSelection();
        if (selection.toString()) {
            e.preventDefault();
            navigator.clipboard.writeText(selection.toString())
                .then(() => console.log('Text copied'))
                .catch(err => console.error('Failed to copy:', err));
        }
    }
});