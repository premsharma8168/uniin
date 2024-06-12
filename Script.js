const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navLinks.classList.toggle('active');
});
// JavaScript code goes here
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbot = document.getElementById('chatbot');
const chatbotClose = document.getElementById('chatbot-close');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatbotToggle.addEventListener('click', () => {
    chatbot.style.display = 'block';
});

chatbotClose.addEventListener('click', () => {
    chatbot.style.display = 'none';
});

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (message) {
        displayMessage('You', message);
        chatInput.value = '';
        // Add your AI chatbot logic here
        displayMessage('UNIIN AI', 'This is a sample response from the UNIIN AI chatbot.');
    }
});

function displayMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
const chatbotToggl = document.getElementById('chatbot-toggle');

chatbotToggle.addEventListener('click', () => {
window.ChatbotKitWidget.open();
});
