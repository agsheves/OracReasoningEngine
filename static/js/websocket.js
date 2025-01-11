let socket = io();
let currentScenario = null; // Store the current scenario for editing
let isFirstMessage = true; // Track if this is the first message in a conversation
const chatWindow = document.getElementById('chat-window'); //Added for easier access

function addMessage(message, isUser = false) {
    if (isFirstMessage && !isUser) {
        // Clear default welcome message when first user message is sent
        chatWindow.innerHTML = '';
        isFirstMessage = false;
    }

    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'system-message');

    const content = document.createElement('p');
    content.textContent = message;
    messageElement.appendChild(content);

    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('simulation_response', (data) => {
    try {
        const response = JSON.parse(data.response);
        addMessage(response.response);

        if (response.state_update) {
            addMessage(`State Update: ${response.state_update}`);
        }

        if (response.available_actions && response.available_actions.length > 0) {
            addMessage('Available actions: ' + response.available_actions.join(', '));
        }
    } catch (error) {
        console.error('Error parsing response:', error);
        addMessage(data.response);
    }
    window.setLoading(false);
});

socket.on('simulation_confirmation', (data) => {
    currentScenario = data;
    const content = `
        <h3>📋 Scenario Analysis</h3>
        <div class="scenario-details">
            <p><strong>Type:</strong> ${data.heuristic}</p>
            <div class="scenario-content">
                ${data.scenario.split('\n').map(line => {
                    if (!line.trim()) return '';
                    if (line.includes('===')) {
                        return `<h4>${line.replace(/=/g, '').trim()}</h4>`;
                    }
                    if (line.startsWith('-')) {
                        return `<li>${line.substring(1).trim()}</li>`;
                    }
                    if (line.includes(':')) {
                        const [key, value] = line.split(':');
                        return `<p><strong>${key.trim()}:</strong> ${value.trim()}</p>`;
                    }
                    return `<p>${line}</p>`;
                }).join('')}
            </div>
        </div>
        <div class="confirmation-buttons">
            <button onclick="confirmSimulation(true)" class="btn">✓ Confirm Scenario</button>
            <button onclick="editScenario()" class="btn edit">✎ Edit</button>
            <button onclick="confirmSimulation(false)" class="btn">✗ Cancel</button>
        </div>
    `;
    addMessage(content);
    window.setLoading(false);
});

socket.on('simulation_error', (data) => {
    addMessage('Error: ' + data.error, false);
    window.setLoading(false);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    window.setLoading(false);
});

window.confirmSimulation = function(confirmed) {
    if (confirmed) {
        isFirstMessage = false; // Set to false after confirming first scenario
    }
    socket.emit('confirm_simulation', confirmed);
    if (confirmed) {
        window.setLoading(true);
    }
}

window.editScenario = function() {
    const messageInput = document.getElementById('message-input');
    if (currentScenario) {
        messageInput.value = currentScenario.original_prompt || '';
        messageInput.focus();
        messageInput.scrollIntoView({ behavior: 'smooth' });
    }
}

window.isFirstMessage = isFirstMessage;