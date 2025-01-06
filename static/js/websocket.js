let socket = io();

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
});

socket.on('simulation_error', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'error-message');
    messageElement.textContent = 'Error: ' + data.error;
    document.getElementById('chat-window').appendChild(messageElement);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});