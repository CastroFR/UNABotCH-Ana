class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            closeTooltip: document.querySelector('.close-tooltip'),
            tooltip: document.querySelector('.chatbox__tooltip'),
            tooltipClosed: false,
            faqBox: document.getElementById('faq-box'), // Nuevo reference
            // Nuevas referencias agregadas
            questionsWrapper: document.querySelector('.quick-questions-wrapper'),
            messagesContainer: document.querySelector('.chatbox__messages')
        }

        this.state = false;
        this.messages = [];
        this.questionsVisible = true; // Nuevo estado para preguntas
        this.faqVisible = true; // Nuevo estado independiente
    }

    display() {
        const {openButton, chatBox, sendButton, closeTooltip, tooltip} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })

        // Cerrar tooltip
        closeTooltip.addEventListener('click', () => {
            tooltip.classList.add('hidden');
            this.args.tooltipClosed = true;
        });

        // Inicializar preguntas
        this.initQuestions();

        // Mostrar tooltip al cargar
        setTimeout(() => {
            tooltip.classList.remove('hidden');
        }, 1000);
    }

    // Nuevo método para preguntas frecuentes
    initQuestions() {
        // Event listener específico para FAQ
        this.args.faqBox.querySelector('.close-quick-questions').addEventListener('click', () => {
            this.toggleFAQ();
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // Cerrar tooltip SOLO si no estaba cerrado manualmente
        if(this.state && !this.args.tooltipClosed) {
            this.args.tooltip.classList.add('hidden');
        }

        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    // Nuevo método para toggle de preguntas
    toggleFAQ() {
        this.faqVisible = !this.faqVisible;
        this.args.faqBox.classList.toggle('hidden', !this.faqVisible);
    }

    onSendButton(chatbox, text = null) {
        const textField = chatbox.querySelector('input');
        const text1 = text || textField.value;
        
        if (text1.trim() === "") return;
    
        // ✅ Agrega el mensaje del usuario UNA sola vez
        const userMsg = { name: "User", message: text1 };
        this.messages.push(userMsg);
        this.updateChatText(chatbox); // Actualiza la UI aquí
    
        fetch(`${$SCRIPT_ROOT}/predict`, {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            headers: { 'Content-Type': 'application/json' },
        })
        .then(r => r.json())
        .then(r => {
            // ✅ Agrega la respuesta del bot
            const botMsg = { name: "Sam", message: r.answer };
            this.messages.push(botMsg);
            this.updateChatText(chatbox);
            textField.value = '';
        })
        .catch(error => {
            console.error('Error:', error);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

        // Auto-scroll al último mensaje
        setTimeout(() => {
            chatmessage.scrollTop = chatmessage.scrollHeight;
        }, 100);
    }

    // Método modificado para preguntas rápidas
    sendQuickQuestion(question, chatBox) {
        this.toggleFAQ();

        // Crear mensaje manualmente
        //let msg = { name: "User", message: question };
        //this.messages.push(msg);
        
        // Simular envío
        this.onSendButton(this.args.chatBox, question);
        
        //this.updateChatText(this.args.chatBox);
        //this.sendMessage(question, this.args.chatBox);
    }

}



const chatbox = new Chatbox();
chatbox.display();