"""HTML generator for Group Chat Wrapped."""

from pathlib import Path
from .analyzer import AnalysisResult, CategoryResult


def generate_html(result: AnalysisResult, output_path: Path) -> None:
    """Generate an HTML presentation from analysis results."""
    
    html_content = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{result.conversation_title} - Wrapped 2025</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            overflow-x: hidden;
            color: white;
        }}

        .container {{
            max-width: 100vw;
            overflow: hidden;
        }}

        /* Slide styles */
        .slide {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px 20px 120px 20px;
            position: relative;
            overflow: hidden;
        }}

        .slide::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: moveBackground 20s linear infinite;
        }}

        @keyframes moveBackground {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(50px, 50px); }}
        }}

        /* Gradient backgrounds for slides */
        .slide:nth-child(odd) {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        .slide:nth-child(even) {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}

        .slide:nth-child(3n) {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}

        .slide:nth-child(4n) {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}

        .slide:nth-child(5n) {{
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        }}

        .slide:nth-child(6n) {{
            background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        }}

        .slide:nth-child(7n) {{
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        }}

        .slide-content {{
            position: relative;
            z-index: 1;
            text-align: center;
            max-width: 800px;
            animation: fadeInUp 0.8s ease-out;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .icon {{
            font-size: 80px;
            margin-bottom: 20px;
            display: block;
            animation: bounce 2s infinite;
        }}

        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
            40% {{ transform: translateY(-20px); }}
            60% {{ transform: translateY(-10px); }}
        }}

        .title {{
            font-size: clamp(2rem, 8vw, 4rem);
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 10px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: clamp(1rem, 3vw, 1.5rem);
            font-weight: 400;
            opacity: 0.9;
            margin-bottom: 40px;
        }}

        .winner {{
            font-size: clamp(2rem, 10vw, 5rem);
            font-weight: 900;
            margin: 30px 0;
            background: linear-gradient(to right, #fff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: glow 2s ease-in-out infinite alternate;
        }}

        @keyframes glow {{
            from {{ filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.5)); }}
            to {{ filter: drop-shadow(0 0 40px rgba(255, 215, 0, 0.8)); }}
        }}

        .value {{
            font-size: clamp(1.5rem, 5vw, 3rem);
            font-weight: 700;
            color: rgba(255,255,255,0.95);
            margin-bottom: 20px;
        }}

        .extra-info {{
            font-size: 1.2rem;
            font-weight: 600;
            background: rgba(255,255,255,0.2);
            padding: 15px 30px;
            border-radius: 50px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }}

        .fun-fact {{
            font-size: 1rem;
            font-style: italic;
            opacity: 0.8;
            margin-top: 20px;
        }}

        /* Top 5 list */
        .top-list {{
            list-style: none;
            text-align: left;
            margin: 30px 0;
        }}

        .top-list li {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 25px;
            margin: 10px 0;
            background: rgba(255,255,255,0.15);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            font-size: 1.2rem;
            transition: transform 0.3s, background 0.3s;
        }}

        .top-list li:hover {{
            transform: translateX(10px);
            background: rgba(255,255,255,0.25);
        }}

        .top-list li:first-child {{
            background: linear-gradient(90deg, rgba(255,215,0,0.4), rgba(255,255,255,0.15));
            font-size: 1.4rem;
            font-weight: 700;
        }}

        .rank {{
            font-weight: 900;
            margin-right: 15px;
            min-width: 30px;
        }}

        .name {{
            flex: 1;
        }}

        .score {{
            font-weight: 600;
            opacity: 0.9;
        }}

        /* Intro slide */
        .intro-slide {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        }}

        .intro-title {{
            font-size: clamp(3rem, 12vw, 8rem);
            font-weight: 900;
            background: linear-gradient(45deg, #f093fb, #f5576c, #667eea, #4facfe);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientMove 5s ease infinite;
        }}

        @keyframes gradientMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .intro-subtitle {{
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            margin-top: 20px;
            opacity: 0.8;
        }}

        .year {{
            font-size: clamp(4rem, 15vw, 10rem);
            font-weight: 900;
            color: rgba(255,255,255,0.1);
            position: absolute;
            bottom: 20px;
            right: 20px;
        }}

        /* Navigation */
        .nav {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 1000;
        }}

        .nav button {{
            padding: 15px 30px;
            font-size: 1.2rem;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            background: rgba(255,255,255,0.2);
            color: white;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }}

        .nav button:hover {{
            background: rgba(255,255,255,0.4);
            transform: scale(1.05);
        }}

        .progress {{
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, #f093fb, #f5576c, #667eea);
            z-index: 1000;
            transition: width 0.3s;
        }}

        /* Audio controls */
        .audio-control {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(255,255,255,0.2);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 24px;
            cursor: pointer;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }}

        .audio-control:hover {{
            background: rgba(255,255,255,0.4);
            transform: scale(1.1);
        }}

        /* Confetti effect */
        .confetti {{
            position: fixed;
            width: 10px;
            height: 10px;
            background: #f00;
            top: -10px;
            animation: fall linear forwards;
        }}

        @keyframes fall {{
            to {{
                transform: translateY(100vh) rotate(720deg);
            }}
        }}

        /* Summary slide special */
        .summary-content {{
            background: rgba(0,0,0,0.3);
            padding: 40px;
            border-radius: 30px;
            backdrop-filter: blur(20px);
        }}

        .summary-stats {{
            white-space: pre-line;
            font-size: 1.3rem;
            line-height: 2;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .nav {{
                bottom: 15px;
            }}
            
            .nav button {{
                padding: 10px 20px;
                font-size: 1rem;
            }}

            .top-list li {{
                font-size: 1rem;
                padding: 10px 15px;
            }}
        }}

        /* Start overlay */
        .start-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            cursor: pointer;
        }}

        .start-overlay.hidden {{
            display: none;
        }}

        .start-btn {{
            padding: 25px 60px;
            font-size: 2rem;
            font-weight: 700;
            border: none;
            border-radius: 60px;
            cursor: pointer;
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
            box-shadow: 0 10px 40px rgba(240, 147, 251, 0.4);
            transition: all 0.3s;
            animation: pulse 2s infinite;
        }}

        .start-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 15px 50px rgba(240, 147, 251, 0.6);
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}

        .start-icon {{
            font-size: 100px;
            margin-bottom: 30px;
            animation: bounce 2s infinite;
        }}

        .start-title {{
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #f093fb, #f5576c, #667eea, #4facfe);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientMove 5s ease infinite;
        }}

        .start-subtitle {{
            font-size: 1.2rem;
            opacity: 0.7;
            margin-bottom: 40px;
        }}
    </style>
</head>
<body>
    <div class="start-overlay" id="startOverlay" onclick="startPresentation()">
        <div class="start-icon">🎉</div>
        <h1 class="start-title">WRAPPED 2025</h1>
        <p class="start-subtitle">{result.conversation_title}</p>
        <button class="start-btn">🎵 Start z muzyką</button>
    </div>

    <div class="progress" id="progress"></div>
    <button class="audio-control" id="audioControl" onclick="toggleAudio()">🔇</button>
    
    <audio id="backgroundMusic" loop preload="auto">
        <source src="https://cdn.pixabay.com/audio/2022/10/18/audio_16e07a8c0c.mp3" type="audio/mpeg">
    </audio>

    <div class="container" id="slideContainer">
        <!-- Intro Slide -->
        <div class="slide intro-slide" data-category="intro">
            <div class="slide-content">
                <div class="icon">🎉</div>
                <h1 class="intro-title">WRAPPED</h1>
                <p class="intro-subtitle">{result.conversation_title}</p>
                <p class="subtitle" style="margin-top: 30px;">
                    {result.total_messages:,} wiadomości • {result.total_participants} uczestników<br>
                    {result.date_range[0].strftime('%d.%m.%Y')} - {result.date_range[1].strftime('%d.%m.%Y')}
                </p>
            </div>
            <div class="year">2025</div>
        </div>

        {generate_slides(result.categories)}
    </div>

    <nav class="nav">
        <button onclick="prevSlide()">← Poprzedni</button>
        <button onclick="nextSlide()">Następny →</button>
    </nav>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        let isPlaying = false;
        const audio = document.getElementById('backgroundMusic');
        const audioBtn = document.getElementById('audioControl');

        function updateProgress() {{
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }}

        function showSlide(index) {{
            if (index < 0) index = 0;
            if (index >= totalSlides) index = totalSlides - 1;
            
            const oldSlide = currentSlide;
            currentSlide = index;
            slides.forEach((slide, i) => {{
                slide.style.display = i === currentSlide ? 'flex' : 'none';
            }});
            
            updateProgress();
            
            // Play sound effect for this slide
            if (oldSlide !== currentSlide) {{
                const sound = getCategorySound(currentSlide);
                playSound(sound);
            }}
            
            // Trigger confetti on last slide
            if (currentSlide === totalSlides - 1) {{
                createConfetti();
                playSound('fanfare');
            }}
        }}

        function nextSlide() {{
            showSlide(currentSlide + 1);
        }}

        function prevSlide() {{
            showSlide(currentSlide - 1);
        }}

        function toggleAudio() {{
            if (isPlaying) {{
                audio.pause();
                audioBtn.textContent = '🔇';
            }} else {{
                audio.play().catch(e => console.log('Audio play failed:', e));
                audioBtn.textContent = '🔊';
            }}
            isPlaying = !isPlaying;
        }}

        function startPresentation() {{
            document.getElementById('startOverlay').classList.add('hidden');
            // Try multiple audio sources
            audio.volume = 0.5;
            const playPromise = audio.play();
            if (playPromise !== undefined) {{
                playPromise.then(() => {{
                    audioBtn.textContent = '🔊';
                    isPlaying = true;
                }}).catch(e => {{
                    console.log('Audio play failed:', e);
                    // Still enable sound effects even if background music fails
                    isPlaying = true;
                    audioBtn.textContent = '🔊';
                }});
            }}
            // Resume audio context for sound effects
            if (audioContext.state === 'suspended') {{
                audioContext.resume();
            }}
            isPlaying = true;
        }}

        function createConfetti() {{
            const colors = ['#f093fb', '#f5576c', '#667eea', '#4facfe', '#43e97b', '#ffd700'];
            
            for (let i = 0; i < 100; i++) {{
                setTimeout(() => {{
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
                    confetti.style.width = (Math.random() * 10 + 5) + 'px';
                    confetti.style.height = confetti.style.width;
                    document.body.appendChild(confetti);
                    
                    setTimeout(() => confetti.remove(), 5000);
                }}, i * 50);
            }}
        }}

        // Sound effects using Web Audio API
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        function playSound(type) {{
            if (!isPlaying) return; // Only play sounds if audio is enabled
            
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            switch(type) {{
                case 'whoosh':
                    // Whoosh sound for slide transition
                    oscillator.type = 'sine';
                    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.15);
                    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.15);
                    break;
                    
                case 'reveal':
                    // Reveal sound for winner announcement
                    oscillator.type = 'triangle';
                    oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.1);
                    oscillator.frequency.exponentialRampToValueAtTime(600, audioContext.currentTime + 0.2);
                    gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.3);
                    break;
                    
                case 'fanfare':
                    // Fanfare for final slide
                    const notes = [523, 659, 784, 1047]; // C5, E5, G5, C6
                    notes.forEach((freq, i) => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'triangle';
                        osc.frequency.value = freq;
                        gain.gain.setValueAtTime(0.1, audioContext.currentTime + i * 0.15);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + i * 0.15 + 0.4);
                        osc.start(audioContext.currentTime + i * 0.15);
                        osc.stop(audioContext.currentTime + i * 0.15 + 0.4);
                    }});
                    return;
                    
                case 'pop':
                    // Pop sound
                    oscillator.type = 'sine';
                    oscillator.frequency.setValueAtTime(600, audioContext.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.05);
                    gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.05);
                    break;
                    
                case 'drum':
                    // Drum roll effect
                    oscillator.type = 'square';
                    oscillator.frequency.value = 150;
                    gainNode.gain.setValueAtTime(0.05, audioContext.currentTime);
                    for (let i = 0; i < 10; i++) {{
                        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime + i * 0.05);
                        gainNode.gain.setValueAtTime(0.02, audioContext.currentTime + i * 0.05 + 0.025);
                    }}
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.6);
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.6);
                    break;
                    
                case 'sparkle':
                    // Sparkle/magic sound
                    const sparkleNotes = [1200, 1400, 1600, 1800, 2000];
                    sparkleNotes.forEach((freq, i) => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sine';
                        osc.frequency.value = freq;
                        gain.gain.setValueAtTime(0.08, audioContext.currentTime + i * 0.08);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + i * 0.08 + 0.2);
                        osc.start(audioContext.currentTime + i * 0.08);
                        osc.stop(audioContext.currentTime + i * 0.08 + 0.2);
                    }});
                    return;
            }}
        }}
        
        // Category-specific sounds
        const categorySounds = {{
            'night_owl': 'sparkle',
            'busiest_day': 'drum',
            'prodigal_son': 'reveal',
            'spam_king': 'fanfare',
            'typing_machine': 'pop',
            'poet': 'sparkle',
            'dictionary': 'pop',
            'ghost': 'whoosh',
            'starter': 'reveal',
            'closer': 'whoosh',
            'reactor': 'sparkle',
            'celebrity': 'fanfare',
            'viral_message': 'fanfare',
            'paparazzo': 'pop',
            'comedian': 'pop',
            'detective': 'reveal',
            'link_maniac': 'pop',
            'emoji_king': 'sparkle',
            'writer': 'reveal',
            'peak_hour': 'drum',
            'summary': 'fanfare'
        }};
        
        function getCategorySound(slideIndex) {{
            const slide = slides[slideIndex];
            const categoryId = slide.getAttribute('data-category');
            return categorySounds[categoryId] || 'whoosh';
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                prevSlide();
            }}
        }});

        // Touch/swipe support
        let touchStartX = 0;
        let touchEndX = 0;

        document.addEventListener('touchstart', e => {{
            touchStartX = e.changedTouches[0].screenX;
        }});

        document.addEventListener('touchend', e => {{
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }});

        function handleSwipe() {{
            const threshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > threshold) {{
                if (diff > 0) {{
                    nextSlide();
                }} else {{
                    prevSlide();
                }}
            }}
        }}

        // Initialize
        showSlide(0);
        updateProgress();
    </script>
</body>
</html>'''
    
    output_path.write_text(html_content, encoding='utf-8')


def generate_slides(categories: list[CategoryResult]) -> str:
    """Generate HTML for all category slides."""
    slides_html = []
    
    for cat in categories:
        if cat.winners and len(cat.winners) > 1:
            # Top list style
            list_items = ""
            for i, (name, score) in enumerate(cat.winners[:5], 1):
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                medal = medals[i-1] if i <= 5 else f"{i}."
                list_items += f'''
                    <li>
                        <span class="rank">{medal}</span>
                        <span class="name">{name}</span>
                        <span class="score">{score}</span>
                    </li>'''
            
            slide = f'''
        <div class="slide" data-category="{cat.category_id}">
            <div class="slide-content">
                <span class="icon">{cat.icon}</span>
                <h2 class="title">{cat.title}</h2>
                <p class="subtitle">{cat.subtitle}</p>
                <ul class="top-list">
                    {list_items}
                </ul>
                {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
            </div>
        </div>'''
        elif cat.category_id == "summary":
            # Summary slide
            slide = f'''
        <div class="slide intro-slide" data-category="{cat.category_id}">
            <div class="slide-content summary-content">
                <span class="icon">{cat.icon}</span>
                <h2 class="title">{cat.title}</h2>
                <p class="subtitle">{cat.subtitle}</p>
                <p class="summary-stats">{cat.extra_info}</p>
                {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
                <p class="extra-info" style="margin-top: 30px;">🎉 Dzięki za wspólny rok! 🎉</p>
            </div>
        </div>'''
        else:
            # Single winner style
            slide = f'''
        <div class="slide" data-category="{cat.category_id}">
            <div class="slide-content">
                <span class="icon">{cat.icon}</span>
                <h2 class="title">{cat.title}</h2>
                <p class="subtitle">{cat.subtitle}</p>
                <p class="winner">{cat.winner}</p>
                {f'<p class="value">{cat.value}</p>' if cat.value else ''}
                {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
            </div>
        </div>'''
        
        slides_html.append(slide)
    
    return '\n'.join(slides_html)
