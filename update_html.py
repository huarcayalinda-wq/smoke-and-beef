import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add GSAP and Lenis
if 'gsap.min.js' not in content:
    content = content.replace('</head>', '''
    <!-- GSAP & Lenis -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.34/dist/lenis.min.js"></script>
    <style>
        /* Lenis */
        html.lenis { height: auto; }
        .lenis.lenis-smooth { scroll-behavior: auto !important; }
        .lenis.lenis-smooth [data-lenis-prevent] { overscroll-behavior: contain; }
        .lenis.lenis-stopped { overflow: hidden; }

        /* Loader */
        #loader {
            position: fixed; inset: 0; background: var(--bg-darker); color: white;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            font-family: var(--font-heading); font-size: 2rem; flex-direction: column; gap: 1rem;
        }
        .progress-bar { width: 200px; height: 4px; background: #333; border-radius: 4px; overflow: hidden; }
        .progress-fill { width: 0%; height: 100%; background: var(--primary); transition: width 0.1s; }

        /* Scroll Canvas Container */
        .video-scroll-container {
            height: 800vh;
            position: relative;
        }

        .canvas-wrapper {
            position: sticky;
            top: 0;
            height: 100vh;
            width: 100%;
            overflow: hidden;
            background: #000;
        }

        #hero-canvas {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .hero-overlay-section {
            position: absolute;
            inset: 0;
            z-index: 10;
            clip-path: circle(150% at 50% 50%); /* Starts fully open */
        }

        /* Giant Text */
        .giant-text-wrapper {
            position: absolute;
            top: 50%; left: 0;
            transform: translateY(-50%);
            z-index: 5;
            white-space: nowrap;
            pointer-events: none;
        }

        #giant-text {
            font-size: 15vw;
            font-family: var(--font-heading);
            color: rgba(255, 255, 255, 0.4);
            text-transform: uppercase;
            font-weight: 900;
            margin: 0;
        }

        /* Stats Section */
        #stats-section {
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.90);
            z-index: 8;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
        }
        
        .stats-grid {
            display: flex; gap: 4rem; text-align: center; color: white;
            flex-wrap: wrap; justify-content: center;
        }

        .stat-item {
            font-family: var(--font-heading);
        }

        .stat-number {
            font-size: 5rem; font-weight: 900; color: var(--primary);
            line-height: 1;
        }

        .stat-label {
            font-size: 1.2rem; font-family: var(--font-body);
            text-transform: uppercase; letter-spacing: 2px;
        }

        /* Persistent CTA */
        .persistent-cta {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            box-shadow: 0 10px 25px rgba(249, 115, 22, 0.4);
            opacity: 0; pointer-events: none; transition: opacity 0.3s;
        }
        .persistent-cta.visible { opacity: 1; pointer-events: auto; }

        /* Animations */
        .gsap-fade-up, .gsap-slide-left, .gsap-slide-right, .gsap-scale-up {
            opacity: 0;
            visibility: hidden;
        }
        
        .left-align { text-align: left !important; }
        .hero-title.left-align { font-size: clamp(2.5rem, 6vw, 4.5rem); max-width: 600px; }
    </style>
</head>''')

# Replace Body start
new_body_start = '''<body>

    <div id="loader">
        <div class="loader-text">Cargando experiencia... 0%</div>
        <div class="progress-bar"><div class="progress-fill" id="loader-fill"></div></div>
    </div>

    <!-- Persistent CTA -->
    <a href="#hamburguesas" class="btn btn-primary btn-large persistent-cta" id="floating-cta">¡PIDE AHORA!</a>

    <!-- Canvas Section -->
    <div class="video-scroll-container" id="video-container">
        <div class="canvas-wrapper">
            <canvas id="hero-canvas"></canvas>

            <div class="giant-text-wrapper">
                <h1 id="giant-text">EL AUTÉNTICO SABOR A LA PARRILLA • SMOKE & BEEF • </h1>
            </div>

            <div id="stats-section">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number"><span class="counter" data-target="1500">0</span>+</div>
                        <div class="stat-label">Burgers Servidas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number"><span class="counter" data-target="100">0</span>%</div>
                        <div class="stat-label">Carne Angus</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number"><span class="counter" data-target="24">0</span>h</div>
                        <div class="stat-label">Macerado</div>
                    </div>
                </div>
            </div>

            <header class="hero hero-overlay-section" id="hero-section">
                <div class="hero-overlay"></div>
                <div class="container hero-content left-align" style="margin: 0; max-width: 100%;">
                    <div class="hero-badge">
                        <span class="live-dot"></span> Abierto hoy · 12pm–11pm
                    </div>
                    <h1 class="hero-title left-align">LO MEJOR ESTÁ EN LA PARRILLA</h1>
                    <p class="hero-subtitle left-align">Descubre el verdadero sabor de nuestras hamburguesas al humo.</p>
                </div>
            </header>
        </div>
    </div>
'''

content = re.sub(r'<body>.*?<header class="hero">.*?</header>', new_body_start, content, flags=re.DOTALL)

# Add GSAP animation classes to sections instead of fade-section
content = content.replace('<section id="promos" class="section section-dark fade-section">', '<section id="promos" class="section section-dark gsap-slide-left">')
content = content.replace('<section id="hamburguesas" class="section section-light fade-section">', '<section id="hamburguesas" class="section section-light gsap-fade-up">')
content = content.replace('<section id="combos" class="section section-gray fade-section">', '<section id="combos" class="section section-gray gsap-scale-up">')
content = content.replace('<section id="extras" class="section section-light fade-section">', '<section id="extras" class="section section-light gsap-slide-right">')
content = content.replace('<section id="bebidas" class="section section-gray fade-section">', '<section id="bebidas" class="section section-gray gsap-slide-left">')

# Modify Scripts
script_start = content.find('<script>')
if script_start != -1:
    new_script = '''<script>
        document.addEventListener("DOMContentLoaded", () => {
            
            // Lenis Setup
            const lenis = new Lenis({
                duration: 1.2,
                easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
                smooth: true
            });

            lenis.on('scroll', ScrollTrigger.update);
            gsap.ticker.add((time) => {
                lenis.raf(time * 1000);
            });
            gsap.ticker.lagSmoothing(0, 0);

            // 1. Navbar Solid on Scroll
            const navbar = document.getElementById('navbar');
            const filterWrapper = document.getElementById('filter-wrapper');
            const navHeight = navbar ? navbar.offsetHeight : 0;
            const floatingCta = document.getElementById('floating-cta');

            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    if (navbar) navbar.classList.add('scrolled');
                } else {
                    if (navbar) navbar.classList.remove('scrolled');
                }

                // Sticky filters logic
                const videoContainer = document.getElementById('video-container');
                if (videoContainer && window.scrollY > videoContainer.offsetHeight - 50) {
                    if (filterWrapper) filterWrapper.classList.add('sticky');
                    floatingCta.classList.add('visible');
                } else {
                    if (filterWrapper) filterWrapper.classList.remove('sticky');
                    floatingCta.classList.remove('visible');
                }
            });

            // 2. Filter Pills Smooth Scroll
            const pills = document.querySelectorAll('.filter-pill');
            const sections = document.querySelectorAll('.section');

            pills.forEach(pill => {
                pill.addEventListener('click', (e) => {
                    const targetId = pill.getAttribute('data-target');
                    const targetSection = document.getElementById(targetId);
                    if(targetSection) {
                        const offsetTop = targetSection.offsetTop - (filterWrapper ? filterWrapper.offsetHeight : 0) - navHeight;
                        lenis.scrollTo(offsetTop);
                    }
                });
            });

            // Update Active Pill
            window.addEventListener('scroll', () => {
                let current = '';
                sections.forEach(section => {
                    const sectionTop = section.offsetTop;
                    if (scrollY >= (sectionTop - (filterWrapper ? filterWrapper.offsetHeight : 0) - navHeight - 100)) {
                        current = section.getAttribute('id');
                    }
                });
                pills.forEach(pill => {
                    pill.classList.remove('active');
                    if (pill.getAttribute('data-target') === current) {
                        pill.classList.add('active');
                    }
                });
            });

            // --- CANVAS EXPERIENCE ---
            const canvas = document.getElementById('hero-canvas');
            const context = canvas.getContext('2d');
            const frameCount = 160; 
            const images = [];
            let loadedCount = 0;

            for (let i = 1; i <= frameCount; i++) {
                const img = new Image();
                const frameNum = i.toString().padStart(4, '0');
                img.src = `frames/frame_${frameNum}.webp`;
                img.onload = () => {
                    loadedCount++;
                    const percent = Math.round((loadedCount / frameCount) * 100);
                    document.querySelector('.loader-text').innerText = `Cargando experiencia... ${percent}%`;
                    document.getElementById('loader-fill').style.width = `${percent}%`;
                    if (loadedCount === frameCount) {
                        document.getElementById('loader').style.display = 'none';
                        render(0);
                        initGSAP();
                    }
                };
                images.push(img);
            }

            function render(index) {
                if (images[index]) {
                    canvas.width = window.innerWidth;
                    canvas.height = window.innerHeight;
                    const img = images[index];
                    const hRatio = canvas.width / img.width;
                    const vRatio = canvas.height / img.height;
                    const ratio  = Math.max(hRatio, vRatio);
                    const centerShift_x = (canvas.width - img.width*ratio) / 2;
                    const centerShift_y = (canvas.height - img.height*ratio) / 2;  
                    
                    context.clearRect(0,0,canvas.width, canvas.height);
                    context.drawImage(img, 0,0, img.width, img.height,
                                       centerShift_x,centerShift_y,img.width*ratio, img.height*ratio);  
                }
            }

            window.addEventListener("resize", () => render(0));

            function initGSAP() {
                // Scroll Canvas Timeline
                const obj = { frame: 0 };
                const tl = gsap.timeline({
                    scrollTrigger: {
                        trigger: "#video-container",
                        start: "top top",
                        end: "+=800%",
                        scrub: 0.5,
                        pin: true
                    }
                });

                // Animate frames
                tl.to(obj, {
                    frame: frameCount - 1,
                    snap: "frame",
                    ease: "none",
                    onUpdate: () => render(obj.frame)
                }, 0);

                // Circular reveal (Hero disappears)
                tl.to("#hero-section", {
                    clipPath: "circle(0% at 50% 50%)",
                    ease: "power2.inOut",
                    duration: 0.1
                }, 0);

                // Giant Text Horizontal Scroll
                tl.to("#giant-text", {
                    xPercent: -50,
                    ease: "none",
                    duration: 0.8
                }, 0.1);

                // Stats Section appear
                tl.to("#stats-section", {
                    opacity: 1,
                    duration: 0.1
                }, 0.8);

                // Section Animations
                const sectionsToAnimate = [
                    { sel: '.gsap-slide-left', x: -100, y: 0, scale: 1 },
                    { sel: '.gsap-slide-right', x: 100, y: 0, scale: 1 },
                    { sel: '.gsap-fade-up', x: 0, y: 100, scale: 1 },
                    { sel: '.gsap-scale-up', x: 0, y: 0, scale: 0.8 }
                ];

                sectionsToAnimate.forEach(anim => {
                    gsap.utils.toArray(anim.sel).forEach(el => {
                        gsap.set(el, { autoAlpha: 0, x: anim.x, y: anim.y, scale: anim.scale });
                        gsap.to(el, {
                            scrollTrigger: {
                                trigger: el,
                                start: "top 80%",
                            },
                            autoAlpha: 1,
                            x: 0,
                            y: 0,
                            scale: 1,
                            duration: 1,
                            ease: "power3.out"
                        });
                    });
                });

                // Stats Counters
                ScrollTrigger.create({
                    trigger: "#video-container",
                    start: "top -700%", // Start when stats section is visible
                    onEnter: () => {
                        const counters = document.querySelectorAll('.counter');
                        counters.forEach(counter => {
                            const target = +counter.getAttribute('data-target');
                            gsap.to(counter, {
                                innerText: target,
                                duration: 2,
                                snap: { innerText: 1 },
                                ease: "power2.out"
                            });
                        });
                    },
                    once: true
                });
            }

            // Efecto 3: Scroll Animations (Parallax)
            const parallaxImgs = document.querySelectorAll('.card-img img');
            parallaxImgs.forEach(img => img.classList.add('parallax-img'));
            
            // GSAP Parallax for images instead of native JS for better perf with Lenis
            parallaxImgs.forEach(img => {
                gsap.to(img, {
                    yPercent: 20,
                    ease: "none",
                    scrollTrigger: {
                        trigger: img.parentElement,
                        start: "top bottom",
                        end: "bottom top",
                        scrub: true
                    }
                });
            });
        });
    </script>
</body>
</html>'''
    content = content[:script_start] + new_script

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")
