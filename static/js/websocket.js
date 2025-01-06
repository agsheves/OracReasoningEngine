let socket = io();

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('simulation_response', (data) => {
    const response = JSON.parse(data.response);
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'system-message');
    
    const content = document.createElement('p');
    content.textContent = response.response;
    messageElement.appendChild(content);
    
    if (response.available_actions && response.available_actions.length > 0) {
        const actions = document.createElement('div');
        actions.classList.add('available-actions');
        actions.textContent = 'Available actions: ' + response.available_actions.join(', ');
        messageElement.appendChild(actions);
    }
    
    document.getElementById('chat-window').appendChild(messageElement);
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
