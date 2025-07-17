document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('llmForm');
    const input = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const micButton = document.getElementById('micButton');
    const messagesArea = document.getElementById('messagesArea');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const recordingStatus = document.getElementById('recordingStatus');
    const imageInput = document.getElementById('imageInput');
    const imageButton = document.getElementById('imageButton');

    // Función para agregar mensajes al chat
    function addMessage(content, sender) {
        let messageDiv = document.createElement('div');
        messageDiv.className = `flex gap-3 items-start max-w-full w-full fade-in-up ${sender === 'user' ? 'user-message' : 'ai-message'}`;
        
        const avatarClass = sender === 'user' 
            ? 'w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-base gradient-secondary text-white shadow-md'
            : 'w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-base gradient-primary text-white shadow-md';
        
        const avatarIcon = sender === 'user' ? 'fas fa-user' : 'fas fa-brain';
        
        const messageTextClass = sender === 'user'
            ? 'gradient-secondary text-white border-orange-600 shadow-md'
            : 'bg-white border-blue-100 text-blue-900 shadow-sm';
        
        messageDiv.innerHTML = `
            <div class="${avatarClass}">
                <i class="${avatarIcon}"></i>
            </div>
            <div class="flex-1 min-w-0 w-full">
                <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-sm text-blue-900">${sender === 'user' ? 'Tú' : 'Asistente AI'}</span>
                    <span class="text-xs text-gray-500">Ahora</span>
                </div>
                <div class="bg-white p-3 rounded-xl border border-blue-100 text-blue-900 text-base leading-relaxed shadow-sm break-words ${messageTextClass}">
                    ${content}
                </div>
            </div>
        `;
        
        messagesArea.appendChild(messageDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    // Función para mostrar mensaje de carga
    function showLoadingMessage() {
        let loadingDiv = document.createElement('div');
        loadingDiv.className = 'flex gap-3 items-start max-w-full w-full fade-in-up';
        loadingDiv.id = 'loadingMessage';
        
        loadingDiv.innerHTML = `
            <div class="w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 text-base gradient-primary text-white shadow-md">
                <i class="fas fa-brain"></i>
            </div>
            <div class="flex-1 min-w-0 w-full">
                <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-sm text-blue-900">Asistente AI</span>
                    <span class="text-xs text-gray-500">Escribiendo...</span>
                </div>
                <div class="bg-white p-3 rounded-xl border border-blue-100 text-blue-900 text-base leading-relaxed shadow-sm">
                    <div class="flex items-center gap-2 text-gray-500 italic">
                        <span>Escribiendo</span>
                        <div class="inline-flex gap-1 loading-dots">
                            <span class="w-1 h-1 rounded-full bg-gray-500"></span>
                            <span class="w-1 h-1 rounded-full bg-gray-500"></span>
                            <span class="w-1 h-1 rounded-full bg-gray-500"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesArea.appendChild(loadingDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function removeLoadingMessage() {
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }

    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });

    // Enviar texto al LLM por AJAX
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const question = input.value.trim();
        if (!question) return;
        
        if (welcomeScreen) welcomeScreen.style.display = 'none';
        
        addMessage(question, 'user');
        input.value = "";
        input.style.height = 'auto';
        sendButton.disabled = true;
        sendButton.className = sendButton.className.replace('gradient-primary', 'bg-gray-300') + ' cursor-not-allowed';
        
        showLoadingMessage();

        try {
            // Hacer llamada real al servidor Django
            const response = await fetch('/llm-api/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ question: question })
            });
            
            const data = await response.json();
            removeLoadingMessage();
            
            if (data.respuesta) {
                addMessage(data.respuesta, 'ai');
            } else if (data.error) {
                addMessage(`Error: ${data.error}`, 'ai');
            } else {
                addMessage('Error: respuesta inesperada del servidor', 'ai');
            }
            
        } catch (err) {
            removeLoadingMessage();
            addMessage(`Error al comunicarse con el servidor: ${err.message}`, 'ai');
        }
        
        sendButton.disabled = false;
        sendButton.className = sendButton.className.replace('bg-gray-300 cursor-not-allowed', 'gradient-primary');
    });

    // Grabación de audio
    let mediaRecorder;
    let audioChunks = [];
    micButton.addEventListener('click', async function() {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        sampleRate: 16000,
                        sampleSize: 16,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });
                
                // Usar formato compatible
                const options = {
                    mimeType: 'audio/webm;codecs=opus'
                };
                
                // Fallback para otros formatos si webm no está soportado
                if (!MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
                    if (MediaRecorder.isTypeSupported('audio/mp4')) {
                        options.mimeType = 'audio/mp4';
                    } else if (MediaRecorder.isTypeSupported('audio/ogg')) {
                        options.mimeType = 'audio/ogg';
                    } else {
                        options.mimeType = 'audio/wav';
                    }
                }
                
                mediaRecorder = new MediaRecorder(stream, options);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = e => {
                    if (e.data.size > 0) audioChunks.push(e.data);
                };
                
                mediaRecorder.onstop = async () => {
                    recordingStatus.classList.add('hidden');
                    
                    // Crear blob con tipo MIME correcto
                    const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
                    
                    // Verificar que el blob no esté vacío
                    if (audioBlob.size === 0) {
                        addMessage('Error: No se pudo capturar audio. Intenta de nuevo.', 'ai');
                        return;
                    }
                    
                    if (welcomeScreen) welcomeScreen.style.display = 'none';
                    addMessage('<i class="fas fa-microphone mr-2"></i>[Audio enviado]', 'user');
                    
                    // Procesar audio en el servidor
                    showLoadingMessage();
                    
                    try {
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'audio.wav');
                        formData.append('ruido_segundos', '1');
                        
                        const response = await fetch('/procesar_audio/', {
                            method: 'POST',
                            body: formData
                        });
                        
                        const data = await response.json();
                        removeLoadingMessage();
                        
                        if (data.error) {
                            addMessage(`Error: ${data.error}`, 'ai');
                        } else {
                            addMessage(`<b>Transcripción:</b> ${data.pregunta}`, 'user');
                            addMessage(data.respuesta, 'ai');
                            
                            // Reproducir audio de respuesta si está disponible
                            if (data.audio_url) {
                                const audioElement = new Audio(data.audio_url);
                                audioElement.play().catch(e => console.log('Error reproduciendo audio:', e));
                            }
                        }
                    } catch (error) {
                        removeLoadingMessage();
                        addMessage(`Error procesando audio: ${error.message}`, 'ai');
                    }
                };
                
                mediaRecorder.start();
                recordingStatus.classList.remove('hidden');
                micButton.innerHTML = '<i class="fas fa-stop"></i>';
                
                setTimeout(() => {
                    if (mediaRecorder.state === 'recording') {
                        mediaRecorder.stop();
                        micButton.innerHTML = '<i class="fas fa-microphone"></i>';
                    }
                }, 5000);
                
            } catch (err) {
                alert("No se pudo acceder al micrófono.");
            }
        } else if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            recordingStatus.classList.add('hidden');
        }
    });

    // Subida de imágenes
    imageButton.addEventListener('click', () => imageInput.click());
    
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (!file) return;
        
        if (welcomeScreen) welcomeScreen.style.display = 'none';
        
        const reader = new FileReader();
        reader.onload = async function(e) {
            addMessage('<i class="fas fa-image mr-2"></i>[Imagen enviada]', 'user');
            addMessage(`<img src="${e.target.result}" class="max-w-xs border border-gray-300 rounded-lg shadow-sm">`, 'user');
            
            // Hacer llamada real al servidor para procesar imagen
            showLoadingMessage();
            
            try {
                const formData = new FormData();
                formData.append('image', file);
                
                const response = await fetch('/llm/procesar-imagen/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                });
                
                const data = await response.json();
                removeLoadingMessage();
                
                if (data.respuesta) {
                    addMessage(data.respuesta, 'ai');
                } else if (data.error) {
                    addMessage(`Error: ${data.error}`, 'ai');
                } else {
                    addMessage('Error: respuesta inesperada del servidor', 'ai');
                }
                
            } catch (err) {
                removeLoadingMessage();
                addMessage(`Error al procesar imagen: ${err.message}`, 'ai');
            }
        };
        reader.readAsDataURL(file);
    });

    // Focus en el input
    input.focus();
});