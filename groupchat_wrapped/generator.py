"""HTML generator for Group Chat Wrapped."""

from pathlib import Path
from .analyzer import AnalysisResult, CategoryResult


def generate_html(result: AnalysisResult, output_path: Path) -> None:
    """Generate an HTML presentation from analysis results."""
    
    html_content = f'''<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#1a1a2e">
    <title>{result.conversation_title} - Wrapped 2025</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎁</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
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
            margin-right: 15px;
        }}

        .score {{
            font-weight: 600;
            opacity: 0.9;
            margin-left: 10px;
            white-space: nowrap;
        }}

        /* Horizontal Timeline for group identity changes */
        .timeline-slide-content {{
            max-width: 95vw !important;
            width: 95vw !important;
            padding-bottom: 80px !important;
        }}
        
        .horizontal-timeline-wrapper {{
            width: 100%;
            padding: 10px;
            margin: 20px 0;
        }}
        
        .timeline-names-row {{
            display: flex;
            width: calc(100% - 35px);
            margin-bottom: 0;
            align-items: flex-end;
            overflow: visible;
        }}
        
        .timeline-names-above {{
            align-items: flex-end;
        }}
        
        .timeline-names-below {{
            align-items: flex-start;
            margin-top: 0;
        }}
        
        .timeline-names-below .timeline-name-entry {{
            flex-direction: column-reverse;
        }}
        
        .timeline-names-below .name-connector {{
            margin-bottom: 0;
        }}
        
        .timeline-name-empty {{
            visibility: hidden;
            height: 0;
            min-height: 0;
        }}
        
        .timeline-name-entry {{
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 30px;
            padding: 0 1px;
            overflow: visible;
        }}
        
        .name-connector {{
            width: 3px;
            height: 12px;
            opacity: 0.7;
        }}
        
        .name-bubble {{
            background: rgba(255,255,255,0.1);
            border: 2px solid;
            border-radius: 10px;
            padding: 4px 8px;
            text-align: center;
            backdrop-filter: blur(5px);
            margin-bottom: 0;
            white-space: nowrap;
            width: auto;
            min-width: auto;
        }}
        
        .name-text {{
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            line-height: 1.2;
            white-space: nowrap;
            overflow: visible;
        }}
        
        .name-date {{
            display: block;
            font-size: 0.65rem;
            opacity: 0.6;
            margin-top: 3px;
        }}
        
        .timeline-bar-container {{
            display: flex;
            align-items: center;
            width: 100%;
        }}
        
        .timeline-bar {{
            display: flex;
            flex: 1;
            height: 45px;
            border-radius: 22px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        .timeline-segment {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-width: 35px;
            transition: transform 0.3s, filter 0.3s;
            cursor: pointer;
            border-right: 2px solid rgba(0,0,0,0.2);
        }}
        
        .timeline-segment:last-child {{
            border-right: none;
        }}
        
        .timeline-segment:hover {{
            transform: scaleY(1.15);
            filter: brightness(1.2);
            z-index: 10;
        }}
        
        .segment-days {{
            font-size: 0.7rem;
            font-weight: 700;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            background: rgba(0,0,0,0.25);
            padding: 2px 6px;
            border-radius: 8px;
        }}
        
        .timeline-arrow-head {{
            width: 0;
            height: 0;
            border-top: 22px solid transparent;
            border-bottom: 22px solid transparent;
            border-left: 30px solid #43e97b;
            margin-left: -2px;
        }}
        
        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
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

        /* Text wrapping for extra-info */
        .extra-info {{
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-word;
            max-width: 100%;
            hyphens: auto;
        }}

        /* Network Graph styles - Cytoscape.js */
        .network-graph-container {{
            width: 100%;
            max-width: 600px;
            height: 400px;
            margin: 20px auto;
            position: relative;
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            overflow: visible;
        }}

        .cytoscape-graph {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: block;
            touch-action: none;
        }}

        .graph-tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 0.9rem;
            pointer-events: none;
            z-index: 1000;
            max-width: 280px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            opacity: 0;
            transition: opacity 0.2s;
            text-align: left;
            line-height: 1.5;
        }}

        .graph-tooltip.visible {{
            opacity: 1;
            pointer-events: auto;
        }}

        .graph-tooltip-title {{
            font-weight: 700;
            margin-bottom: 5px;
            font-size: 1rem;
        }}

        .graph-tooltip-emoji {{
            margin-top: 8px;
            font-size: 1.1rem;
        }}

        .graph-legend {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0,0,0,0.5);
            padding: 8px 15px;
            border-radius: 10px;
            font-size: 0.8rem;
            backdrop-filter: blur(5px);
        }}

        /* Responsive - Tablets */
        @media (max-width: 768px) {{
            .slide-content {{
                padding: 20px;
            }}
            
            .title {{
                font-size: 1.8rem;
            }}
            
            .icon {{
                font-size: 4rem;
            }}
            
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
            
            .winner {{
                font-size: 2rem;
            }}
            
            .extra-info {{
                font-size: 1rem;
            }}
            
            .fun-fact {{
                font-size: 0.85rem;
                padding: 8px 15px;
            }}
            
            /* Graph responsive - Tablet */
            .network-graph-container {{
                height: 350px;
                max-width: 100%;
            }}
        }}
        
        /* Responsive - Mobile phones */
        @media (max-width: 480px) {{
            .slide-content {{
                padding: 15px;
            }}
            
            .title {{
                font-size: 1.4rem;
            }}
            
            .subtitle {{
                font-size: 0.9rem;
            }}
            
            .icon {{
                font-size: 3rem;
            }}
            
            .nav {{
                bottom: 10px;
                gap: 10px;
            }}
            
            .nav button {{
                padding: 8px 16px;
                font-size: 0.9rem;
            }}

            .top-list li {{
                font-size: 0.9rem;
                padding: 8px 12px;
                flex-wrap: wrap;
            }}
            
            .top-list .name {{
                flex: 1 1 60%;
                min-width: 0;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            
            .top-list .score {{
                flex: 0 0 auto;
                font-size: 0.8rem;
            }}
            
            .winner {{
                font-size: 1.5rem;
            }}
            
            .extra-info {{
                font-size: 0.9rem;
            }}
            
            .fun-fact {{
                font-size: 0.75rem;
                padding: 6px 12px;
                word-break: break-word;
            }}
            
            .start-overlay h1 {{
                font-size: 2rem !important;
            }}
            
            .start-overlay .start-emoji {{
                font-size: 4rem !important;
            }}
            
            .tap-hint {{
                font-size: 0.85rem;
            }}
            
            /* Timeline mobile */
            .timeline-container {{
                padding: 10px;
            }}
            
            .timeline-item {{
                font-size: 0.75rem;
            }}
            
            /* Graph responsive - Mobile */
            .network-graph-container {{
                height: 320px;
                max-width: 100%;
                margin: 10px auto;
            }}
            
            .graph-legend {{
                font-size: 0.7rem;
                padding: 6px 10px;
            }}
        }}
        
        /* Very small phones */
        @media (max-width: 360px) {{
            .title {{
                font-size: 1.2rem;
            }}
            
            .top-list li {{
                padding: 6px 10px;
            }}
            
            .nav button {{
                padding: 6px 12px;
                font-size: 0.8rem;
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
        
        /* Suspense / Reveal phases */
        .teaser-phase {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.5s ease;
        }}
        
        .teaser-icon {{
            animation: pulse 1.5s infinite, bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .suspense-dots {{
            font-size: 4rem;
            margin: 30px 0;
            display: flex;
            gap: 10px;
        }}
        
        .suspense-dots span {{
            animation: dotPulse 1.5s infinite;
            opacity: 0.3;
        }}
        
        .suspense-dots span:nth-child(2) {{
            animation-delay: 0.3s;
        }}
        
        .suspense-dots span:nth-child(3) {{
            animation-delay: 0.6s;
        }}
        
        @keyframes dotPulse {{
            0%, 100% {{ opacity: 0.3; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.3); }}
        }}
        
        .tap-hint {{
            font-size: 1.1rem;
            opacity: 0.6;
            margin-top: 20px;
            animation: fadeInOut 2s infinite;
        }}
        
        @keyframes fadeInOut {{
            0%, 100% {{ opacity: 0.4; }}
            50% {{ opacity: 0.8; }}
        }}
        
        .reveal-phase {{
            animation: revealSlide 0.6s ease;
        }}
        
        .reveal-phase.hidden,
        .teaser-phase.hidden {{
            display: none;
        }}
        
        @keyframes revealSlide {{
            0% {{
                opacity: 0;
                transform: scale(0.8);
            }}
            50% {{
                transform: scale(1.05);
            }}
            100% {{
                opacity: 1;
                transform: scale(1);
            }}
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

    <div class="container" id="slideContainer">
        <!-- Intro Slide -->
        <div class="slide intro-slide" data-category="intro" data-no-suspense="true">
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
        <button class="nav-btn" onclick="prevSlide()">← Poprzedni</button>
        <button class="nav-btn" onclick="nextSlide()">Następny →</button>
    </nav>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        let isPlaying = false;
        const audioBtn = document.getElementById('audioControl');
        
        // Background music using Web Audio API
        let bgMusicContext = null;
        let bgMusicGain = null;
        let bgMusicPlaying = false;
        let bgMusicInterval = null;
        
        function startBackgroundMusic() {{
            if (bgMusicPlaying) return;
            bgMusicContext = new (window.AudioContext || window.webkitAudioContext)();
            bgMusicGain = bgMusicContext.createGain();
            bgMusicGain.connect(bgMusicContext.destination);
            bgMusicGain.gain.value = 0.08;
            bgMusicPlaying = true;
            
            // Ambient looping melody pattern
            const chords = [
                [261, 329, 392], // C major
                [293, 369, 440], // D minor  
                [349, 440, 523], // F major
                [392, 494, 587], // G major
            ];
            
            let chordIndex = 0;
            
            function playBackgroundChord() {{
                if (!bgMusicPlaying) return;
                const chord = chords[chordIndex % chords.length];
                chord.forEach(freq => {{
                    const osc = bgMusicContext.createOscillator();
                    const gain = bgMusicContext.createGain();
                    osc.connect(gain);
                    gain.connect(bgMusicGain);
                    osc.type = 'sine';
                    osc.frequency.value = freq;
                    gain.gain.setValueAtTime(0.15, bgMusicContext.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, bgMusicContext.currentTime + 1.8);
                    osc.start();
                    osc.stop(bgMusicContext.currentTime + 2);
                }});
                chordIndex++;
            }}
            
            playBackgroundChord();
            bgMusicInterval = setInterval(playBackgroundChord, 2000);
        }}
        
        function stopBackgroundMusic() {{
            bgMusicPlaying = false;
            if (bgMusicInterval) {{
                clearInterval(bgMusicInterval);
                bgMusicInterval = null;
            }}
            if (bgMusicGain) {{
                bgMusicGain.gain.value = 0;
            }}
        }}

        function updateProgress() {{
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progress').style.width = progress + '%';
        }}
        
        // Track which slides have been revealed
        const revealedSlides = new Set();
        
        function isSlideRevealed(index) {{
            return revealedSlides.has(index);
        }}
        
        function revealCurrentSlide() {{
            const slide = slides[currentSlide];
            const teaser = slide.querySelector('.teaser-phase');
            const reveal = slide.querySelector('.reveal-phase');
            
            // Check if this slide has suspense phases
            if (!teaser || !reveal) return false;
            
            // Check if already revealed
            if (isSlideRevealed(currentSlide)) return false;
            
            // Hide teaser, show reveal
            teaser.style.display = 'none';
            reveal.classList.remove('hidden');
            revealedSlides.add(currentSlide);
            
            // Play reveal sound
            const melodyFn = getCategorySound(currentSlide);
            if (melodyFn) melodyFn();
            
            return true;
        }}
        
        function resetSlidePhases(index) {{
            const slide = slides[index];
            const teaser = slide.querySelector('.teaser-phase');
            const reveal = slide.querySelector('.reveal-phase');
            
            if (teaser && reveal && !isSlideRevealed(index)) {{
                teaser.style.display = 'flex';
                reveal.classList.add('hidden');
            }}
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
            
            // Reset phases for this slide if not revealed
            resetSlidePhases(currentSlide);
            
            // For slides without suspense (intro, summary), play sound directly
            const slide = slides[currentSlide];
            const noSuspense = slide.getAttribute('data-no-suspense') === 'true';
            const hasSuspense = slide.querySelector('.teaser-phase') !== null;
            
            if (oldSlide !== currentSlide && (!hasSuspense || isSlideRevealed(currentSlide) || noSuspense)) {{
                const melodyFn = getCategorySound(currentSlide);
                if (melodyFn) melodyFn();
            }}
            
            // Trigger confetti on last slide
            if (currentSlide === totalSlides - 1) {{
                createConfetti();
                categoryMelodies['summary']();
            }}
        }}
        
        // Handle click/tap on slide to reveal
        document.getElementById('slideContainer').addEventListener('click', (e) => {{
            // Don't trigger on navigation buttons
            if (e.target.closest('.nav-btn') || e.target.closest('.audio-control')) return;
            
            const slide = slides[currentSlide];
            const teaser = slide.querySelector('.teaser-phase');
            
            // If slide has teaser and not revealed, reveal it
            if (teaser && teaser.style.display !== 'none' && !isSlideRevealed(currentSlide)) {{
                revealCurrentSlide();
            }}
        }});

        function nextSlide() {{
            // If current slide has unrevealed teaser, reveal first
            const slide = slides[currentSlide];
            const teaser = slide.querySelector('.teaser-phase');
            if (teaser && teaser.style.display !== 'none' && !isSlideRevealed(currentSlide)) {{
                revealCurrentSlide();
                return;
            }}
            showSlide(currentSlide + 1);
        }}

        function prevSlide() {{
            showSlide(currentSlide - 1);
        }}

        function toggleAudio() {{
            if (isPlaying) {{
                stopBackgroundMusic();
                audioBtn.textContent = '🔇';
                isPlaying = false;
            }} else {{
                startBackgroundMusic();
                audioBtn.textContent = '🔊';
                isPlaying = true;
            }}
        }}

        function startPresentation() {{
            document.getElementById('startOverlay').classList.add('hidden');
            // Start background music
            startBackgroundMusic();
            audioBtn.textContent = '🔊';
            isPlaying = true;
            // Resume audio context for sound effects
            if (audioContext.state === 'suspended') {{
                audioContext.resume();
            }}
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

        // Sound effects using Web Audio API - unique melody for each category
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        function playMelody(notes, waveType = 'sine', noteDuration = 0.15, noteGap = 0.1) {{
            if (!isPlaying) return;
            notes.forEach((freq, i) => {{
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                osc.type = waveType;
                osc.frequency.value = freq;
                const startTime = audioContext.currentTime + i * noteGap;
                gain.gain.setValueAtTime(0.12, startTime);
                gain.gain.exponentialRampToValueAtTime(0.01, startTime + noteDuration);
                osc.start(startTime);
                osc.stop(startTime + noteDuration);
            }});
        }}
        
        // Unique melodies for each category
        const categoryMelodies = {{
            // 🦉 Nocny Marek - mysterious owl hoot descending
            'night_owl': () => playMelody([880, 660, 440, 330], 'sine', 0.2, 0.15),
            
            // 🔥 Dzień Apokalipsy - intense rising alarm
            'busiest_day': () => playMelody([200, 300, 400, 500, 600, 800], 'sawtooth', 0.08, 0.06),
            
            // 🚪 Syn Marnotrawny - welcome back fanfare
            'prodigal_son': () => playMelody([392, 494, 588, 784], 'triangle', 0.25, 0.2),
            
            // 👑 Król Spamu - royal trumpets
            'spam_king': () => playMelody([523, 523, 659, 784, 659, 784, 1047], 'triangle', 0.18, 0.12),
            
            // ⌨️ Maszyna do Pisania - typewriter clicks
            'typing_machine': () => {{
                [0, 50, 100, 150, 200, 250].forEach(delay => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'square';
                        osc.frequency.value = 1200 + Math.random() * 400;
                        gain.gain.setValueAtTime(0.08, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.03);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.03);
                    }}, delay);
                }});
            }},
            
            // 📜 Poeta - elegant harp arpeggio
            'poet': () => playMelody([523, 659, 784, 988, 1175, 1319], 'sine', 0.3, 0.1),
            
            // 📚 Słownik - book page flip sounds
            'dictionary': () => playMelody([2000, 1800, 2200, 1600, 2400], 'sine', 0.05, 0.08),
            
            // 👻 Duch - spooky ghost whoosh
            'ghost': () => {{
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, audioContext.currentTime);
                osc.frequency.exponentialRampToValueAtTime(100, audioContext.currentTime + 0.5);
                gain.gain.setValueAtTime(0.15, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                osc.start();
                osc.stop(audioContext.currentTime + 0.5);
            }},
            
            // 🎬 Reżyser - movie clapper
            'starter': () => playMelody([800, 1000, 800, 1200], 'square', 0.05, 0.08),
            
            // 🚪 Zamykacz - door closing thud
            'closer': () => {{
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(150, audioContext.currentTime);
                osc.frequency.exponentialRampToValueAtTime(50, audioContext.currentTime + 0.2);
                gain.gain.setValueAtTime(0.3, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
                osc.start();
                osc.stop(audioContext.currentTime + 0.3);
            }},
            
            // ❤️ Reakcjonista - heart beating
            'reactor': () => {{
                [0, 200, 600, 800].forEach((delay, i) => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sine';
                        osc.frequency.value = i % 2 === 0 ? 80 : 100;
                        gain.gain.setValueAtTime(0.2, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.15);
                    }}, delay);
                }});
            }},
            
            // ⭐ Celebryta - star twinkle
            'celebrity': () => playMelody([1568, 1760, 1976, 2093, 1760, 2349], 'sine', 0.12, 0.08),
            
            // 💥 Viral - explosion boom
            'viral_message': () => {{
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(100, audioContext.currentTime);
                osc.frequency.exponentialRampToValueAtTime(30, audioContext.currentTime + 0.4);
                gain.gain.setValueAtTime(0.25, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                osc.start();
                osc.stop(audioContext.currentTime + 0.5);
                // Add high crackle
                setTimeout(() => playMelody([3000, 2500, 3500, 2000], 'square', 0.03, 0.02), 50);
            }},
            
            // 📸 Paparazzo - camera shutter
            'paparazzo': () => {{
                const osc = audioContext.createOscillator();
                const gain = audioContext.createGain();
                osc.connect(gain);
                gain.connect(audioContext.destination);
                osc.type = 'square';
                osc.frequency.value = 4000;
                gain.gain.setValueAtTime(0.1, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.02);
                osc.start();
                osc.stop(audioContext.currentTime + 0.02);
                setTimeout(() => {{
                    const osc2 = audioContext.createOscillator();
                    const gain2 = audioContext.createGain();
                    osc2.connect(gain2);
                    gain2.connect(audioContext.destination);
                    osc2.type = 'square';
                    osc2.frequency.value = 3000;
                    gain2.gain.setValueAtTime(0.08, audioContext.currentTime);
                    gain2.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.03);
                    osc2.start();
                    osc2.stop(audioContext.currentTime + 0.03);
                }}, 80);
            }},
            
            // 🤡 Śmieszek - funny bouncy sound
            'comedian': () => playMelody([300, 500, 400, 600, 350, 700], 'triangle', 0.1, 0.07),
            
            // 🔍 Detektyw - investigation reveal
            'detective': () => playMelody([220, 277, 330, 440], 'triangle', 0.2, 0.18),
            
            // 🔗 Linkomaniak - digital connection beeps
            'link_maniac': () => playMelody([1047, 1319, 1047, 1568, 1319], 'square', 0.08, 0.1),
            
            // 😎 Emoji Master - playful ascending
            'emoji_king': () => playMelody([392, 440, 494, 523, 587, 659, 698, 784], 'sine', 0.08, 0.06),
            
            // 📝 Pisarz - pen writing scratch
            'writer': () => {{
                [0, 80, 160, 280, 350].forEach(delay => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sawtooth';
                        osc.frequency.value = 800 + Math.random() * 600;
                        gain.gain.setValueAtTime(0.04, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.06);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.06);
                    }}, delay);
                }});
            }},
            
            // ⏰ Godzina Szczytu - clock ticking then alarm
            'peak_hour': () => {{
                [0, 150, 300].forEach(delay => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sine';
                        osc.frequency.value = 1000;
                        gain.gain.setValueAtTime(0.1, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.05);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.05);
                    }}, delay);
                }});
                setTimeout(() => playMelody([880, 880, 1100, 880], 'triangle', 0.15, 0.1), 450);
            }},
            
            // 🎭 Metamorfozy - theatrical transformation sound
            'group_identity': () => {{
                // Mysterious rising transformation
                playMelody([220, 330, 440, 550, 660, 880], 'sine', 0.15, 0.12);
                setTimeout(() => {{
                    playMelody([440, 523, 659, 784], 'triangle', 0.2, 0.1);
                }}, 700);
            }},
            
            // 🏷️ Sieć Oznaczeń - network connection sounds
            'mentions_graph': () => {{
                // Digital network pings
                [0, 100, 200, 350, 500].forEach((delay, i) => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sine';
                        osc.frequency.value = 600 + i * 150;
                        gain.gain.setValueAtTime(0.1, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.15);
                    }}, delay);
                }});
            }},
            
            // ❤️ Sieć Reakcji - love connection sounds
            'reactions_graph': () => {{
                // Heartbeat with rising tones
                [0, 200, 500, 700].forEach((delay, i) => {{
                    setTimeout(() => {{
                        const osc = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        osc.connect(gain);
                        gain.connect(audioContext.destination);
                        osc.type = 'sine';
                        osc.frequency.value = 300 + i * 100;
                        gain.gain.setValueAtTime(0.15, audioContext.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
                        osc.start();
                        osc.stop(audioContext.currentTime + 0.2);
                    }}, delay);
                }});
            }},
            
            // 📊 Podsumowanie - grand finale fanfare
            'summary': () => {{
                playMelody([523, 659, 784, 1047, 1319, 1568], 'triangle', 0.25, 0.12);
                setTimeout(() => playMelody([784, 988, 1175, 1568], 'sine', 0.4, 0.15), 600);
            }},
            
            // Default intro sound
            'intro': () => playMelody([440, 554, 659, 880], 'sine', 0.2, 0.15)
        }};
        
        function getCategorySound(slideIndex) {{
            const slide = slides[slideIndex];
            const categoryId = slide.getAttribute('data-category');
            return categoryMelodies[categoryId] || categoryMelodies['intro'];
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

        // Graph tooltip functions
        function showGraphTooltip(graphId, edgeIdx, x, y) {{
            const data = window.graphData[graphId][edgeIdx];
            const tooltip = document.getElementById('tooltip-' + graphId);
            const container = document.getElementById('graph-container-' + graphId);
            
            if (!tooltip || !data) return;
            
            let html = '<div class="graph-tooltip-title">';
            if (data.isSelf) {{
                html += data.from + ' → ' + data.from + ' (sam sobie)';
            }} else {{
                html += data.from + ' → ' + data.to;
            }}
            html += '</div>';
            html += '<div><strong>' + data.weight + '</strong> ' + (graphId === 'reactions_graph' ? 'reakcji' : 'oznaczeń') + '</div>';
            
            if (data.emojis) {{
                html += '<div class="graph-tooltip-emoji">' + data.emojis + '</div>';
            }}
            
            tooltip.innerHTML = html;
            tooltip.classList.add('visible');
            
            // Position tooltip
            const rect = container.getBoundingClientRect();
            const tooltipRect = tooltip.getBoundingClientRect();
            
            if (x + tooltipRect.width > rect.width - 10) {{
                x = rect.width - tooltipRect.width - 10;
            }}
            if (y + tooltipRect.height > rect.height - 10) {{
                y = y - tooltipRect.height - 10;
            }}
            
            tooltip.style.left = Math.max(10, x) + 'px';
            tooltip.style.top = Math.max(10, y) + 'px';
        }}
        
        function hideGraphTooltip(graphId) {{
            const tooltip = document.getElementById('tooltip-' + graphId);
            if (tooltip) {{
                tooltip.classList.remove('visible');
            }}
        }}
        
        // Initialize Cytoscape graphs
        function initCytoscapeGraph(graphId) {{
            const container = document.getElementById('cy-' + graphId);
            if (!container || !window.cyElements[graphId]) {{
                console.log('Cytoscape: container or elements not found for', graphId);
                return;
            }}
            if (window.cyInstances[graphId]) {{
                console.log('Cytoscape: already initialized for', graphId);
                return; // Already initialized
            }}
            
            // Force container dimensions - ensure proper sizing
            const parent = container.parentElement;
            
            // Get computed dimensions, fallback to reasonable defaults
            const computedStyle = window.getComputedStyle(parent);
            let width = parseInt(computedStyle.width) || parent.offsetWidth || 600;
            let height = parseInt(computedStyle.height) || parent.offsetHeight || 400;
            
            // Ensure minimum dimensions
            width = Math.max(width, 300);
            height = Math.max(height, 300);
            
            // Apply dimensions explicitly to both container and canvas holder
            parent.style.width = width + 'px';
            parent.style.height = height + 'px';
            container.style.width = width + 'px';
            container.style.height = height + 'px';
            
            console.log('Cytoscape: initializing', graphId, 'with size', width, 'x', height);
            
            const elements = window.cyElements[graphId];
            
            const cy = cytoscape({{
                container: container,
                elements: [...elements.nodes, ...elements.edges],
                style: [
                    {{
                        selector: 'node',
                        style: {{
                            'background-color': 'data(color)',
                            'label': 'data(label)',
                            'color': '#ffffff',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'font-size': '10px',
                            'font-weight': '600',
                            'font-family': 'Poppins, sans-serif',
                            'text-outline-color': 'rgba(0,0,0,0.5)',
                            'text-outline-width': '2px',
                            'width': '56px',
                            'height': '56px',
                            'border-width': '2px',
                            'border-color': 'rgba(255,255,255,0.3)',
                            'transition-property': 'width, height, opacity',
                            'transition-duration': '0.2s'
                        }}
                    }},
                    {{
                        selector: 'node.hover',
                        style: {{
                            'width': '68px',
                            'height': '68px',
                            'border-width': '3px',
                            'z-index': 10
                        }}
                    }},
                    {{
                        selector: 'node.dimmed',
                        style: {{
                            'opacity': 0.2
                        }}
                    }},
                    {{
                        selector: 'node.connected',
                        style: {{
                            'opacity': 1
                        }}
                    }},
                    {{
                        selector: 'edge',
                        style: {{
                            'width': 'data(width)',
                            'line-color': 'data(color)',
                            'target-arrow-color': 'data(color)',
                            'target-arrow-shape': 'triangle',
                            'arrow-scale': 1.2,
                            'curve-style': 'bezier',
                            'opacity': 0.7,
                            'label': 'data(weight)',
                            'font-size': '10px',
                            'font-weight': 'bold',
                            'font-family': 'Poppins, sans-serif',
                            'color': '#ffffff',
                            'text-outline-color': 'rgba(0,0,0,0.8)',
                            'text-outline-width': '3px',
                            'text-background-color': 'rgba(0,0,0,0.5)',
                            'text-background-opacity': 0.8,
                            'text-background-padding': '3px',
                            'text-background-shape': 'roundrectangle',
                            'loop-direction': '0deg',
                            'loop-sweep': '60deg',
                            'control-point-step-size': 50,
                            'transition-property': 'opacity, width',
                            'transition-duration': '0.2s'
                        }}
                    }},
                    {{
                        selector: 'edge.highlighted',
                        style: {{
                            'opacity': 1,
                            'width': 'mapData(width, 2, 8, 4, 12)',
                            'z-index': 10
                        }}
                    }},
                    {{
                        selector: 'edge.dimmed',
                        style: {{
                            'opacity': 0.1
                        }}
                    }},
                    {{
                        selector: 'edge:selected',
                        style: {{
                            'opacity': 1,
                            'width': 'mapData(width, 2, 8, 4, 12)'
                        }}
                    }}
                ],
                layout: {{
                    name: 'circle',
                    avoidOverlap: true,
                    spacingFactor: 1.2,
                    padding: 50,
                    animate: false
                }},
                userZoomingEnabled: false,
                userPanningEnabled: false,
                boxSelectionEnabled: false,
                autoungrabify: true,
                wheelSensitivity: 0,
                minZoom: 0.5,
                maxZoom: 2,
                pixelRatio: 'auto'
            }});
            
            window.cyInstances[graphId] = cy;
            
            // Center and fit the graph after layout
            cy.on('layoutstop', function() {{
                setTimeout(function() {{
                    cy.resize();
                    cy.fit(null, 40);
                    cy.center();
                }}, 50);
            }});
            
            // Also fit immediately after ready
            cy.ready(function() {{
                setTimeout(function() {{
                    cy.resize();
                    cy.fit(null, 40);
                    cy.center();
                }}, 100);
            }});
            
            // Node hover - highlight outgoing edges and target nodes
            cy.on('mouseover', 'node', function(e) {{
                const node = e.target;
                node.addClass('hover');
                
                // Dim all elements first
                cy.elements().addClass('dimmed');
                node.removeClass('dimmed');
                
                // Highlight outgoing edges and their targets
                const outgoingEdges = node.outgoers('edge');
                outgoingEdges.removeClass('dimmed').addClass('highlighted');
                
                // Keep target nodes visible
                outgoingEdges.targets().removeClass('dimmed').addClass('connected');
                
                // Also highlight self-loops
                const selfLoops = cy.edges().filter(edge => 
                    edge.source().id() === node.id() && edge.target().id() === node.id()
                );
                selfLoops.removeClass('dimmed').addClass('highlighted');
            }});
            
            cy.on('mouseout', 'node', function(e) {{
                const node = e.target;
                node.removeClass('hover');
                cy.elements().removeClass('dimmed highlighted connected');
            }});
            
            // Edge tooltip - use separate handlers for tap and mouseover
            cy.on('tap', 'edge', function(e) {{
                e.stopPropagation();
                const edge = e.target;
                const idx = edge.data('idx');
                const renderedPos = edge.renderedMidpoint();
                showGraphTooltip(graphId, idx, renderedPos.x, renderedPos.y);
            }});
            
            cy.on('mouseover', 'edge', function(e) {{
                const edge = e.target;
                const idx = edge.data('idx');
                const renderedPos = edge.renderedMidpoint();
                showGraphTooltip(graphId, idx, renderedPos.x, renderedPos.y);
            }});
            
            cy.on('mouseout', 'edge', function() {{
                hideGraphTooltip(graphId);
            }});
            
            // Click on empty space to hide tooltip
            cy.on('tap', function(e) {{
                if (e.target === cy) {{
                    hideGraphTooltip(graphId);
                }}
            }});
            
            // Node tap - stop propagation so it doesn't interfere
            cy.on('tap', 'node', function(e) {{
                e.stopPropagation();
            }});
        }}
        
        // Initialize graphs when their slide is revealed (after click)
        function initGraphsOnReveal(slideIndex) {{
            const slide = slides[slideIndex];
            if (!slide) return;
            
            const graphIds = ['mentions_graph', 'reactions_graph'];
            graphIds.forEach(graphId => {{
                if (slide.dataset.category === graphId) {{
                    // Wait for reveal animation and DOM to update
                    setTimeout(() => {{
                        initCytoscapeGraph(graphId);
                    }}, 400);
                }}
            }});
        }}
        
        // Also try to init graph when navigating to a slide that's already revealed
        function tryInitGraphOnSlide(slideIndex) {{
            const slide = slides[slideIndex];
            if (!slide) return;
            
            const graphIds = ['mentions_graph', 'reactions_graph'];
            graphIds.forEach(graphId => {{
                if (slide.dataset.category === graphId && isSlideRevealed(slideIndex)) {{
                    setTimeout(() => {{
                        if (!window.cyInstances[graphId]) {{
                            initCytoscapeGraph(graphId);
                        }} else {{
                            // Resize and re-center if already exists
                            const cy = window.cyInstances[graphId];
                            cy.resize();
                            cy.fit(null, 40);
                            cy.center();
                        }}
                    }}, 150);
                }}
            }});
        }}
        
        // Hook into revealCurrentSlide to init graphs
        const originalRevealCurrentSlide = revealCurrentSlide;
        revealCurrentSlide = function() {{
            const result = originalRevealCurrentSlide();
            if (result) {{
                initGraphsOnReveal(currentSlide);
            }}
            return result;
        }};
        
        // Hook into showSlide to try init if already revealed
        const originalShowSlide = showSlide;
        showSlide = function(index) {{
            originalShowSlide(index);
            tryInitGraphOnSlide(index);
            // Update URL hash
            if (slides[index]) {{
                const category = slides[index].dataset.category;
                if (category) {{
                    history.replaceState(null, '', '#' + category);
                }} else {{
                    history.replaceState(null, '', '#slide-' + index);
                }}
            }}
        }};
        
        // Parse URL hash to get initial slide
        function getSlideFromHash() {{
            const hash = window.location.hash.substring(1);
            if (!hash) return 0;
            
            // Try to find by category id
            for (let i = 0; i < slides.length; i++) {{
                if (slides[i].dataset.category === hash) {{
                    return i;
                }}
            }}
            
            // Try slide-N format
            const match = hash.match(/^slide-(\\d+)$/);
            if (match) {{
                const idx = parseInt(match[1], 10);
                if (idx >= 0 && idx < slides.length) {{
                    return idx;
                }}
            }}
            
            return 0;
        }}
        
        // Handle hash change (back/forward navigation)
        window.addEventListener('hashchange', function() {{
            const targetSlide = getSlideFromHash();
            if (targetSlide !== currentSlide) {{
                showSlide(targetSlide);
            }}
        }});

        // Initialize from hash or start
        const initialSlide = getSlideFromHash();
        if (initialSlide > 0 || window.location.hash) {{
            // Skip start overlay when using hash navigation (for testing)
            document.getElementById('startOverlay').classList.add('hidden');
            
            // Auto-reveal all slides up to and including target for testing
            for (let i = 0; i <= initialSlide; i++) {{
                revealedSlides.add(i);
                const teaserPhase = slides[i].querySelector('.teaser-phase');
                const revealPhase = slides[i].querySelector('.reveal-phase');
                if (teaserPhase) teaserPhase.classList.add('hidden');
                if (revealPhase) revealPhase.classList.remove('hidden');
            }}
            
            // Initialize graphs if we're on a graph slide
            setTimeout(() => {{
                tryInitGraphOnSlide(initialSlide);
            }}, 200);
        }}
        showSlide(initialSlide);
        updateProgress();
    </script>
</body>
</html>'''
    
    output_path.write_text(html_content, encoding='utf-8')


def generate_graph_slide(cat: CategoryResult) -> str:
    """Generate HTML for a network graph slide using Cytoscape.js."""
    import json
    import html
    
    edges = cat.winners  # List of dicts with 'from', 'to', 'weight', and optionally 'emojis'
    is_reactions = cat.category_id == "reactions_graph"
    
    # Collect unique nodes
    nodes_set = set()
    for edge in edges:
        nodes_set.add(edge['from'])
        nodes_set.add(edge['to'])
    
    nodes = list(nodes_set)
    node_colors = ['#f093fb', '#667eea', '#4facfe', '#43e97b', '#f5576c', '#ffd700', '#ff6b6b', '#48dbfb', '#a29bfe', '#fd79a8']
    
    # Unique ID for this graph
    graph_id = cat.category_id
    
    # Build Cytoscape elements
    cy_nodes = []
    for i, node in enumerate(nodes):
        display_name = node.split()[0] if node else node
        if len(display_name) > 8:
            display_name = display_name[:7] + "."
        cy_nodes.append({
            'data': {
                'id': node,
                'label': display_name,
                'color': node_colors[i % len(node_colors)]
            }
        })
    
    # Calculate max weight for scaling
    max_weight = max(edge['weight'] for edge in edges) if edges else 1
    
    cy_edges = []
    edge_data = []  # For tooltip data
    for idx, edge in enumerate(edges):
        is_self_loop = edge['from'] == edge['to']
        weight = edge['weight']
        
        # Get color based on 'from' node
        from_idx = nodes.index(edge['from'])
        color = node_colors[from_idx % len(node_colors)]
        
        # Scale width based on weight (2-8 px)
        width = max(2, min(8, (weight / max_weight) * 8))
        
        cy_edges.append({
            'data': {
                'id': f'e{idx}',
                'source': edge['from'],
                'target': edge['to'],
                'weight': weight,
                'color': color,
                'width': width,
                'idx': idx
            }
        })
        
        # Build tooltip data
        from_name = edge['from'].split()[0] if edge['from'] else edge['from']
        to_name = edge['to'].split()[0] if edge['to'] else edge['to']
        
        tooltip_data = {
            'from': from_name,
            'to': to_name,
            'weight': weight,
            'isSelf': is_self_loop
        }
        
        if is_reactions and 'emojis' in edge and edge['emojis']:
            emoji_str = ' '.join([f"{e if e != '❤' else '❤️'}×{c}" for e, c in edge['emojis'][:5]])
            tooltip_data['emojis'] = emoji_str
        
        edge_data.append(tooltip_data)
    
    # JSON encode data
    cy_elements = {'nodes': cy_nodes, 'edges': cy_edges}
    elements_json = json.dumps(cy_elements, ensure_ascii=False)
    edge_data_json = json.dumps(edge_data, ensure_ascii=False)
    
    # Assemble the slide
    slide = f'''
        <div class="slide" data-category="{cat.category_id}">
            <div class="slide-content">
                <div class="teaser-phase">
                    <span class="icon teaser-icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <p class="subtitle">{cat.subtitle}</p>
                    <div class="suspense-dots"><span>.</span><span>.</span><span>.</span></div>
                    <p class="tap-hint">Kliknij aby zobaczyć wyniki</p>
                </div>
                <div class="reveal-phase hidden">
                    <span class="icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <div class="network-graph-container" id="graph-container-{graph_id}">
                        <div class="cytoscape-graph" id="cy-{graph_id}"></div>
                        <div class="graph-tooltip" id="tooltip-{graph_id}"></div>
                        <div class="graph-legend">
                            Kliknij strzałkę aby zobaczyć szczegóły
                        </div>
                    </div>
                    {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                    {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
                </div>
            </div>
        </div>
        <script>
            window.graphData = window.graphData || {{}};
            window.graphData['{graph_id}'] = {edge_data_json};
            window.cyElements = window.cyElements || {{}};
            window.cyElements['{graph_id}'] = {elements_json};
            window.cyInstances = window.cyInstances || {{}};
        </script>'''
    
    return slide


def generate_slides(categories: list[CategoryResult]) -> str:
    """Generate HTML for all category slides."""
    slides_html = []
    
    for cat in categories:
        if cat.category_id == "group_identity" and cat.winners:
            # Horizontal timeline with names alternating above/below to avoid overlap
            colors = ['#f093fb', '#667eea', '#4facfe', '#43e97b', '#f5576c', '#ffd700', '#ff6b6b', '#48dbfb']
            timeline_segments = ""
            timeline_names_above = ""
            timeline_names_below = ""
            
            for i, entry in enumerate(cat.winners[:8]):  # Max 8 entries
                color = colors[i % len(colors)]
                
                timeline_segments += f'''
                    <div class="timeline-segment" style="flex: {entry['days']}; background: {color};" title="{entry['name']} ({entry['days']} dni)">
                        <span class="segment-days">{entry['days']}d</span>
                    </div>'''
                
                # Alternate between above and below rows
                name_entry = f'''
                    <div class="timeline-name-entry" style="flex: {entry['days']};">
                        <div class="name-bubble" style="border-color: {color}; background: linear-gradient(135deg, {color}22, {color}11);">
                            <span class="name-text">{entry['name']}</span>
                            <span class="name-date">{entry['date']}</span>
                        </div>
                        <div class="name-connector" style="background: {color};"></div>
                    </div>'''
                
                # Empty placeholder for the other row
                empty_entry = f'''
                    <div class="timeline-name-entry timeline-name-empty" style="flex: {entry['days']};"></div>'''
                
                if i % 2 == 0:
                    timeline_names_above += name_entry
                    timeline_names_below += empty_entry
                else:
                    timeline_names_above += empty_entry
                    timeline_names_below += name_entry
            
            slide = f'''
        <div class="slide" data-category="{cat.category_id}">
            <div class="slide-content timeline-slide-content">
                <div class="teaser-phase">
                    <span class="icon teaser-icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <p class="subtitle">{cat.subtitle}</p>
                    <div class="suspense-dots"><span>.</span><span>.</span><span>.</span></div>
                    <p class="tap-hint">Kliknij aby zobaczyć wyniki</p>
                </div>
                <div class="reveal-phase hidden">
                    <span class="icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <div class="horizontal-timeline-wrapper">
                        <div class="timeline-names-row timeline-names-above">
                            {timeline_names_above}
                        </div>
                        <div class="timeline-bar-container">
                            <div class="timeline-bar">
                                {timeline_segments}
                            </div>
                            <div class="timeline-arrow-head"></div>
                        </div>
                        <div class="timeline-names-row timeline-names-below">
                            {timeline_names_below}
                        </div>
                    </div>
                    {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                    {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
                </div>
            </div>
        </div>'''
        elif cat.category_id in ("mentions_graph", "reactions_graph") and cat.winners:
            # Network graph visualization
            slide = generate_graph_slide(cat)
        elif cat.winners and len(cat.winners) > 1:
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
                <div class="teaser-phase">
                    <span class="icon teaser-icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <p class="subtitle">{cat.subtitle}</p>
                    <div class="suspense-dots"><span>.</span><span>.</span><span>.</span></div>
                    <p class="tap-hint">Kliknij aby zobaczyć wyniki</p>
                </div>
                <div class="reveal-phase hidden">
                    <span class="icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <ul class="top-list">
                        {list_items}
                    </ul>
                    {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                    {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
                </div>
            </div>
        </div>'''
        elif cat.category_id == "summary":
            # Summary slide - no suspense
            slide = f'''
        <div class="slide intro-slide" data-category="{cat.category_id}" data-no-suspense="true">
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
                <div class="teaser-phase">
                    <span class="icon teaser-icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <p class="subtitle">{cat.subtitle}</p>
                    <div class="suspense-dots"><span>.</span><span>.</span><span>.</span></div>
                    <p class="tap-hint">Kliknij aby zobaczyć wyniki</p>
                </div>
                <div class="reveal-phase hidden">
                    <span class="icon">{cat.icon}</span>
                    <h2 class="title">{cat.title}</h2>
                    <p class="winner">{cat.winner}</p>
                    {f'<p class="value">{cat.value}</p>' if cat.value else ''}
                    {f'<p class="extra-info">{cat.extra_info}</p>' if cat.extra_info else ''}
                    {f'<p class="fun-fact">{cat.fun_fact}</p>' if cat.fun_fact else ''}
                </div>
            </div>
        </div>'''
        
        slides_html.append(slide)
    
    return '\n'.join(slides_html)
