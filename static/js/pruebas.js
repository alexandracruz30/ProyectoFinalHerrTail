// ===== ZONA DE PRUEBAS - JAVASCRIPT INTERACTIVO =====

class ZonaPruebas {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.createParticleSystem();
    }

    init() {
        // Elementos del DOM
        this.fileInput = document.getElementById('file-input');
        this.dropzone = document.querySelector('.dropzone-demo');
        this.dropzoneText = document.getElementById('dropzone-text');
        this.form = document.getElementById('form-prediccion');
        this.btnPredecir = document.querySelector('.btn-predecir');
        this.resultadosCard = document.querySelector('.pruebas-card');
        
        // Estados
        this.isProcessing = false;
        this.imagePreview = null;
        
        // Configuración de animaciones
        this.particles = [];
        this.animationId = null;
    }

    setupEventListeners() {
        // Drag and Drop
        this.dropzone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.dropzone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.dropzone.addEventListener('drop', (e) => this.handleDrop(e));
        
        // File input change
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Form submit
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        // Hover effects
        this.setupHoverEffects();
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    // ===== DRAG & DROP FUNCTIONALITY =====
    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropzone.classList.add('drag-over');
        this.createDragEffect();
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropzone.classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropzone.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
            this.createDropEffect();
        }
    }

    // ===== FILE HANDLING =====
    handleFileSelect(e) {
        if (e.target.files.length > 0) {
            this.processFile(e.target.files[0]);
        }
    }

    processFile(file) {
        // Validar tipo de archivo
        if (!this.validateFile(file)) return;
        
        // Actualizar UI
        this.updateDropzoneText(file.name);
        
        // Crear preview
        this.createImagePreview(file);
        
        // Animación de éxito
        this.animateFileSuccess();
    }

    validateFile(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff'];
        const maxSize = 10 * 1024 * 1024; // 10MB
        
        if (!validTypes.includes(file.type)) {
            this.showError('❌ Tipo de archivo no válido. Use JPG, PNG o TIFF');
            return false;
        }
        
        if (file.size > maxSize) {
            this.showError('❌ Archivo muy grande. Máximo 10MB');
            return false;
        }
        
        return true;
    }

    createImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagePreview = e.target.result;
            this.showImagePreview();
        };
        reader.readAsDataURL(file);
    }

    showImagePreview() {
        const imageCard = document.querySelector('.zona-pruebas-col3 .pruebas-card:last-child .pruebas-card-body');
        imageCard.innerHTML = `
            <div class="image-preview-container" style="position: relative;">
                <img src="${this.imagePreview}" alt="Vista previa" 
                     style="width:230px; height:230px; border-radius:12px; box-shadow:0 4px 20px rgba(24,105,213,0.3); 
                            transition: all 0.3s ease; image-rendering: pixelated;"
                     onload="this.style.opacity='1'" class="preview-image">
                <div class="image-overlay">
                    <div class="scanning-line"></div>
                </div>
            </div>
            <div class="preview-info" style="margin-top:12px; color:#757b8a; font-size:0.9em;">
                ✅ Imagen cargada correctamente
            </div>
        `;
        
        // Activar botón predecir
        this.btnPredecir.disabled = false;
        this.btnPredecir.classList.add('ready');
    }

    // ===== FORM SUBMISSION =====
    async handleFormSubmit(e) {
        if (this.isProcessing) {
            e.preventDefault();
            return;
        }
        
        this.startPrediction();
        // El formulario continúa con su envío normal
    }

    startPrediction() {
        this.isProcessing = true;
        this.btnPredecir.innerHTML = `
            <div class="loading-spinner"></div>
            <span style="margin-left: 8px;">Analizando...</span>
        `;
        this.btnPredecir.disabled = true;
        
        // Animación de procesamiento
        this.startProcessingAnimation();
        
        // Simular análisis (en caso de que el servidor tarde)
        this.simulateAnalysis();
    }

    simulateAnalysis() {
        const steps = [
            { text: '🔍 Preparando imagen...', delay: 500 },
            { text: '🧠 Ejecutando modelo...', delay: 1000 },
            { text: '📊 Calculando probabilidades...', delay: 800 },
            { text: '✨ Finalizando...', delay: 400 }
        ];
        
        let currentStep = 0;
        const updateStep = () => {
            if (currentStep < steps.length && this.isProcessing) {
                this.showAnalysisStep(steps[currentStep].text);
                setTimeout(() => {
                    currentStep++;
                    updateStep();
                }, steps[currentStep - 1]?.delay || 0);
            }
        };
        
        updateStep();
    }

    showAnalysisStep(text) {
        const resultCard = document.querySelector('.zona-pruebas-col3 .pruebas-card:first-child .pruebas-card-body');
        resultCard.innerHTML = `
            <div style="text-align:center; color:#1869d5;">
                <div class="analysis-pulse"></div>
                <div style="margin-top: 15px; font-size: 1.1em;">${text}</div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>
        `;
    }

    // ===== VISUAL EFFECTS =====
    createParticleSystem() {
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '1000';
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);
        
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
    }

    createDropEffect() {
        const rect = this.dropzone.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 20; i++) {
            this.particles.push({
                x: centerX,
                y: centerY,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.5) * 8,
                life: 60,
                color: `hsl(${210 + Math.random() * 60}, 70%, 60%)`
            });
        }
        
        this.animateParticles();
    }

    createDragEffect() {
        // Efecto sutil de partículas en el borde del dropzone
        const rect = this.dropzone.getBoundingClientRect();
        
        if (Math.random() < 0.3) {
            this.particles.push({
                x: rect.left + Math.random() * rect.width,
                y: rect.top + Math.random() * rect.height,
                vx: (Math.random() - 0.5) * 2,
                vy: -Math.random() * 2,
                life: 30,
                color: '#1869d5'
            });
        }
        
        this.animateParticles();
    }

    animateParticles() {
        if (this.animationId) return;
        
        const animate = () => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.particles = this.particles.filter(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.life--;
                
                const alpha = particle.life / 60;
                this.ctx.fillStyle = particle.color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, 3, 0, Math.PI * 2);
                this.ctx.fill();
                
                return particle.life > 0;
            });
            
            if (this.particles.length > 0) {
                this.animationId = requestAnimationFrame(animate);
            } else {
                this.animationId = null;
            }
        };
        
        animate();
    }

    startProcessingAnimation() {
        const imageContainer = document.querySelector('.image-preview-container');
        if (imageContainer) {
            imageContainer.classList.add('processing');
        }
    }

    // ===== HOVER EFFECTS =====
    setupHoverEffects() {
        const cards = document.querySelectorAll('.pruebas-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 8px 25px rgba(0,0,0,0.1)';
            });
            
            card.addEventListener('mouseleave', (e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '';
            });
        });
    }

    // ===== UTILITY FUNCTIONS =====
    updateDropzoneText(filename) {
        this.dropzoneText.innerHTML = `
            <span style="color: #1869d5; font-weight: 600;">✅ ${filename}</span><br>
            <span class="dropzone-subtext">Archivo listo para procesar</span>
        `;
    }

    animateFileSuccess() {
        this.dropzone.classList.add('success-animation');
        setTimeout(() => {
            this.dropzone.classList.remove('success-animation');
        }, 1000);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-toast';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            background: #ff4757; color: white; padding: 12px 20px;
            border-radius: 8px; font-weight: 500; box-shadow: 0 4px 12px rgba(255,71,87,0.3);
            transform: translateX(100%); transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => errorDiv.style.transform = 'translateX(0)', 100);
        setTimeout(() => {
            errorDiv.style.transform = 'translateX(100%)';
            setTimeout(() => errorDiv.remove(), 300);
        }, 3000);
    }

    handleKeyboard(e) {
        // Ctrl/Cmd + U para subir archivo
        if ((e.ctrlKey || e.metaKey) && e.key === 'u') {
            e.preventDefault();
            this.fileInput.click();
        }
        
        // Enter para predecir (si hay imagen)
        if (e.key === 'Enter' && !this.isProcessing && this.imagePreview) {
            this.form.submit();
        }
    }
}

// ===== CSS DINÁMICO =====
const dynamicCSS = `
    .drag-over {
        background: linear-gradient(135deg, rgba(24,105,213,0.1), rgba(24,105,213,0.05)) !important;
        border-color: #1869d5 !important;
        transform: scale(1.02);
    }

    .success-animation {
        animation: successPulse 1s ease;
    }

    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .btn-predecir.ready {
        background: linear-gradient(135deg, #1869d5, #0f4c75);
        box-shadow: 0 4px 15px rgba(24,105,213,0.4);
        transform: translateY(-1px);
    }

    .loading-spinner {
        width: 16px; height: 16px; border: 2px solid #fff3;
        border-top: 2px solid #fff; border-radius: 50%;
        animation: spin 1s linear infinite; display: inline-block;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .analysis-pulse {
        width: 60px; height: 60px; margin: 0 auto;
        background: linear-gradient(135deg, #1869d5, #4c9eff);
        border-radius: 50%; position: relative;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }

    .progress-bar {
        width: 200px; height: 4px; background: #e1e5e9;
        border-radius: 2px; margin: 20px auto; overflow: hidden;
    }

    .progress-fill {
        height: 100%; background: linear-gradient(90deg, #1869d5, #4c9eff);
        border-radius: 2px; animation: progressFlow 2s ease-in-out infinite;
    }

    @keyframes progressFlow {
        0% { width: 0%; }
        50% { width: 70%; }
        100% { width: 100%; }
    }

    .image-preview-container.processing .preview-image {
        filter: brightness(1.1) contrast(1.1);
        animation: imageAnalysis 3s ease-in-out infinite;
    }

    @keyframes imageAnalysis {
        0%, 100% { filter: brightness(1.1) contrast(1.1); }
        50% { filter: brightness(1.3) contrast(1.2) saturate(1.2); }
    }

    .scanning-line {
        position: absolute; top: 0; left: 0; right: 0;
        height: 2px; background: linear-gradient(90deg, transparent, #1869d5, transparent);
        animation: scanLine 2s linear infinite;
    }

    @keyframes scanLine {
        0% { transform: translateY(0); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(230px); opacity: 0; }
    }

    .error-toast {
        animation: toastSlide 0.3s ease;
    }

    @keyframes toastSlide {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
`;

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', () => {
    // Inyectar CSS dinámico
    const style = document.createElement('style');
    style.textContent = dynamicCSS;
    document.head.appendChild(style);
    
    // Inicializar aplicación
    new ZonaPruebas();
    
    // Easter egg: Konami code
    let konamiCode = [];
    const konami = [38,38,40,40,37,39,37,39,66,65];
    document.addEventListener('keydown', (e) => {
        konamiCode.push(e.keyCode);
        if (konamiCode.length > 10) konamiCode.shift();
        if (konamiCode.join(',') === konami.join(',')) {
            document.body.style.filter = 'hue-rotate(180deg)';
            setTimeout(() => document.body.style.filter = '', 3000);
        }
    });
});

// ===== UTILIDADES GLOBALES =====
window.ZonaPruebas = {
    // Función para simular resultados (para testing)
    simularResultado: (clase, probabilidades) => {
        const resultCard = document.querySelector('.zona-pruebas-col3 .pruebas-card:first-child .pruebas-card-body');
        resultCard.innerHTML = `
            <div style="text-align:center; color:#1869d5; width:100%;">
                <span style="font-size:1.16em; font-weight:500;">Predicción del modelo:</span><br>
                <span style="font-size:1.35em; font-weight:700; color:#1869d5;">${clase}</span>
                <h4 style="margin:12px 0 4px 0; color:#46546c;">Probabilidades:</h4>
                <ul style="display:inline-block; text-align:left; font-size:1.03em; margin:0 auto;">
                    ${Object.entries(probabilidades).map(([label, prob]) => 
                        `<li>${label}: <span style="color:#1869d5; font-weight:600;">${prob.toFixed(3)}</span></li>`
                    ).join('')}
                </ul>
            </div>
        `;
    }
};