// particles-bg.js
(function(){
    const colors = [
        'particle-blue', 'particle-orange', 'particle-green', 'particle-purple', 'particle-gray'
    ];
    const sizes = [
        'particle-xs', 'particle-sm', 'particle-md', 'particle-lg', 'particle-xl'
    ];
    const numParticles = window.innerWidth > 900 ? 28 : 13;
    function randomBetween(a, b) { return a + Math.random() * (b - a); }
    function createParticle() {
        const p = document.createElement('div');
        p.classList.add('particle');
        p.classList.add(
            colors[Math.floor(Math.random() * colors.length)],
            sizes[Math.floor(Math.random() * sizes.length)]
        );
        p.style.left = `${randomBetween(0, 100)}vw`;
        p.style.bottom = `-${randomBetween(2, 30)}vh`;
        p.style.animationDelay = `${randomBetween(0, 12)}s`;
        p.style.animationDuration = `${randomBetween(15, 36)}s`;
        p.style.transform = `rotate(${randomBetween(0, 360)}deg)`;
        return p;
    }
    function launchParticles() {
        let bg = document.querySelector('.particles-bg');
        if (!bg) {
            bg = document.createElement('div');
            bg.className = 'particles-bg';
            document.body.prepend(bg);
        }
        for(let i = 0; i < numParticles; i++) {
            bg.appendChild(createParticle());
        }
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", launchParticles);
    } else {
        launchParticles();
    }
})();