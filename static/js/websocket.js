let socket = io();
let currentScenario = null; // Store the current scenario for editing

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('simulation_response', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system-message');

    try {
        const response = JSON.parse(data.response);
        const content = document.createElement('p');
        content.textContent = response.response;
        messageElement.appendChild(content);

        if (response.state_update) {
            const stateUpdate = document.createElement('div');
            stateUpdate.classList.add('state-update');
            stateUpdate.textContent = `State Update: ${response.state_update}`;
            messageElement.appendChild(stateUpdate);
        }

        if (response.available_actions && response.available_actions.length > 0) {
            const actions = document.createElement('div');
            actions.classList.add('available-actions');
            actions.textContent = 'Available actions: ' + response.available_actions.join(', ');
            messageElement.appendChild(actions);
        }
    } catch (error) {
        console.error('Error parsing response:', error);
        const content = document.createElement('p');
        content.textContent = data.response;
        messageElement.appendChild(content);
    }

    document.getElementById('chat-window').appendChild(messageElement);
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;

    // Hide loading indicator when response is received
    window.setLoading(false);
});

socket.on('simulation_confirmation', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system-message');

    // Store the current scenario data for editing
    currentScenario = data;

    const content = document.createElement('div');
    content.innerHTML = `
        <h3>📋 Scenario Analysis</h3>
        <div class="scenario-details">
            <p><strong>Type:</strong> ${data.heuristic}</p>
            <div class="scenario-content">
                ${data.scenario.split('\n').map(line => {
                    // Skip empty lines
                    if (!line.trim()) return '';

                    // Format section headers
                    if (line.includes('===')) {
                        return `<h4>${line.replace(/=/g, '').trim()}</h4>`;
                    }

                    // Handle bullet points and regular text
                    if (line.startsWith('-')) {
                        return `<li>${line.substring(1).trim()}</li>`;
                    }

                    // Handle key-value pairs
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
    messageElement.appendChild(content);

    document.getElementById('chat-window').appendChild(messageElement);
    document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;

    // Hide loading indicator when confirmation is requested
    window.setLoading(false);
});

socket.on('simulation_error', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'error-message');
    messageElement.textContent = 'Error: ' + data.error;
    document.getElementById('chat-window').appendChild(messageElement);

    // Hide loading indicator on error
    window.setLoading(false);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    // Hide loading indicator on disconnect
    window.setLoading(false);
});

// Add to global scope for button onclick handlers
window.confirmSimulation = function(confirmed) {
    socket.emit('confirm_simulation', confirmed);
    if (confirmed) {
        window.setLoading(true);
    }
}

// Add edit functionality
window.editScenario = function() {
    const messageInput = document.getElementById('message-input');
    if (currentScenario) {
        // Copy original prompt back to input field
        messageInput.value = currentScenario.original_prompt || '';
        messageInput.focus();
        // Scroll input into view
        messageInput.scrollIntoView({ behavior: 'smooth' });
    }
}