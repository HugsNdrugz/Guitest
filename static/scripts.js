// Highlight Active Sidebar Link
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.sidebar nav a');
    const currentPath = window.location.pathname;

    links.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Simulate Typing Indicator
function simulateTyping() {
    const typingContainer = document.createElement('div');
    typingContainer.className = 'typing-indicator';
    typingContainer.innerText = 'Typing...';

    const messagesContainer = document.querySelector('.messages-container');
    messagesContainer.appendChild(typingContainer);

    setTimeout(() => {
        messagesContainer.removeChild(typingContainer);
    }, 2000);
}

// Example Usage: Uncomment to test typing simulation
// simulateTyping();