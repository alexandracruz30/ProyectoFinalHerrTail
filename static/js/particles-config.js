// Custom particles.js configuration for CNN Model Explorer
function initParticles() {
    // Theme-aware particle colors
    const isDark = document.documentElement.classList.contains('dark');
    
    const lightThemeConfig = {
        particles: {
            color: { value: ["#183b6b", "#e97228", "#00c37e", "#ba3259"] },
            line_linked: { color: "#183b6b", opacity: 0.2 }
        }
    };
    
    const darkThemeConfig = {
        particles: {
            color: { value: ["#5ca8f8", "#f8b97d", "#3bf7b8", "#e299b3"] },
            line_linked: { color: "#5ca8f8", opacity: 0.3 }
        }
    };
    
    const config = {
        "particles": {
            "number": {
                "value": window.innerWidth > 768 ? 60 : 30,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": isDark ? darkThemeConfig.particles.color : lightThemeConfig.particles.color,
            "shape": {
                "type": ["circle", "triangle"],
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 6
                }
            },
            "opacity": {
                "value": 0.6,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 4,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 3,
                    "size_min": 0.5,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": isDark ? darkThemeConfig.particles.line_linked.color : lightThemeConfig.particles.line_linked.color,
                "opacity": isDark ? darkThemeConfig.particles.line_linked.opacity : lightThemeConfig.particles.line_linked.opacity,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": true,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 100,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    };
    
    // Initialize particles
    if (window.pJSDom && window.pJSDom.length > 0) {
        // Destroy existing particles before creating new ones
        window.pJSDom[0].pJS.fn.vendors.destroypJS();
        window.pJSDom = [];
    }
    
    particlesJS('particles-js', config);
}

// Initialize particles when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add slight delay to ensure all elements are ready
    setTimeout(initParticles, 100);
});

// Reinitialize particles when theme changes
function reinitializeParticlesOnThemeChange() {
    // Add slight delay to allow theme transition
    setTimeout(initParticles, 300);
}

// Export for use in theme toggle functions
window.reinitializeParticlesOnThemeChange = reinitializeParticlesOnThemeChange;