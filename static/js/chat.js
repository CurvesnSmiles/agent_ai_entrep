document.addEventListener("DOMContentLoaded", function() {
    const darkModeSwitch = document.querySelector('#dark-mode-switch');
    const toggleSidebarButton = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');

    // Fonction pour activer/désactiver le mode sombre
    darkModeSwitch.addEventListener('change', function() {
        document.body.classList.toggle('light-mode');
        chatLog.classList.toggle('dark-mode-chat-text');
    });

    // Fonction pour afficher/masquer la barre latérale
    toggleSidebarButton.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // Variable pour suivre l'état de la réponse automatique
    let isAutoReplying = false;

    // Gestion de l'événement de click sur le bouton "Send"
    sendButton.addEventListener('click', function() {
        sendMessage();
    });

    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim(); // Récupère le message de l'utilisateur et supprime les espaces blancs au début et à la fin
        if (message !== '') {
            // Crée un élément de message et l'ajoute au chat
            const messageContainer = document.createElement('div');
            messageContainer.className = 'message-container';

            const userTag = document.createElement('b');
            userTag.textContent = 'You';
            messageContainer.appendChild(userTag);

            const breakElement1 = document.createElement('br');
            messageContainer.appendChild(breakElement1);

            const messageElement = document.createElement('span');
            messageElement.className = 'message user';
            messageElement.textContent = message;
            messageContainer.appendChild(messageElement);

            const breakElement2 = document.createElement('br');
            messageContainer.appendChild(breakElement2);

            const timeElement = document.createElement('span');
            timeElement.className = 'message-time';
            timeElement.textContent = getCurrentTime();
            messageContainer.appendChild(timeElement);

            chatLog.appendChild(messageContainer);

            // Efface le champ de saisie après l'envoi du message
            userInput.value = '';
            
            // Mettre le focus sur le champ de saisie
            userInput.focus();

            // Marquer que le chat est en train de répondre
            isAutoReplying = true;

            // Envoie une réponse automatique après un court délai
            sendAutoReply();
        }
    }

    // Fonction pour envoyer une réponse automatique avec un effet de dactylographie
    
    // Effet de dactylographie
    function typeEffect(text, element, callback) {
        let index = 0;
        const typingSpeed = 10; // Vitesse de frappe en millisecondes

        function type() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                setTimeout(type, typingSpeed);
            } else {
                element.classList.remove('typing');
                // Appeler le callback une fois que l'effet de dactylographie est terminé
                if (typeof callback === 'function') {
                    callback();
                }
            }
        }

        type();
    }

    // Fonction pour obtenir l'heure actuelle au format HH:MM
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
});
