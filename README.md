<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stefan Sendyk</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Fraunces:ital,wght@1,600;1,900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --red: #ff1500;
      --black: #0b0b0c;
      --black-2: #18181a;
      --blue: #2f5fff;
      --iri-cyan: #5be9ff;
      --iri-pink: #ff6ec7;
      --iri-purple: #9b5cff;
      --paper: #f2f0ec;
      --dim: #9a9a9e;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: 'Space Mono', monospace;
      color: var(--paper);
      background: var(--red);
      line-height: 1.6;
      padding: 28px 16px;
    }

    .panel {
      max-width: 860px;
      margin: 0 auto;
      background: var(--black);
      position: relative;
      overflow: hidden;
      clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 28px 100%, 0 calc(100% - 28px));
    }

    /* fabric weave texture */
    .panel::before {
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 50;
      opacity: 0.1;
      mix-blend-mode: overlay;
      background-image:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.5) 0 1px, transparent 1px 3px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.5) 0 1px, transparent 1px 3px);
    }

    .inner {
      padding: 50px 40px 70px;
      position: relative;
      z-index: 2;
    }

    /* red sharp corner tabs */
    .corner {
      position: absolute;
      width: 46px;
      height: 46px;
      background: var(--red);
      z-index: 3;
    }
    .corner-tl { top: 0; left: 0; clip-path: polygon(0 0, 100% 0, 0 100%); }
    .corner-br { bottom: 0; right: 0; clip-path: polygon(100% 100%, 0 100%, 100% 0); }

    /* HERO */
    .hero {
      position: relative;
      padding: 10px 0 40px;
      overflow: hidden;
    }

    .paint-flow {
      position: absolute;
      top: -10%;
      right: -15%;
      width: 70%;
      height: 140%;
      z-index: 0;
      opacity: 0.95;
      filter: blur(0.3px);
      pointer-events: none;
    }

    .hero-content {
      position: relative;
      z-index: 2;
    }

    .specimen-box {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: var(--red);
      color: var(--black);
      padding: 6px 14px;
      font-weight: 700;
      font-size: 0.78rem;
      letter-spacing: 0.05em;
      margin-bottom: 30px;
    }

    h1 {
      font-family: 'Anton', sans-serif;
      font-weight: 400;
      font-size: clamp(3rem, 9vw, 4.8rem);
      margin: 0;
      line-height: 0.92;
      letter-spacing: -0.01em;
      text-transform: uppercase;
      color: var(--paper);
    }

    .tagline {
      margin-top: 22px;
      font-family: 'Fraunces', serif;
      font-style: italic;
      font-weight: 600;
      font-size: 1.1rem;
      color: var(--iri-cyan);
    }

    /* SECTIONS */
    section {
      margin-top: 60px;
      position: relative;
      z-index: 2;
    }

    .section-head {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 26px;
    }

    .section-num {
      font-weight: 700;
      font-size: 0.85rem;
      border: 2px solid var(--red);
      color: var(--red);
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    h2 {
      font-family: 'Fraunces', serif;
      font-style: italic;
      font-weight: 900;
      font-size: 1.55rem;
      margin: 0;
      text-transform: uppercase;
      color: var(--paper);
    }

    /* thin paint divider */
    .flow-divider {
      width: 100%;
      height: 10px;
      margin: 56px 0 -16px;
      opacity: 0.85;
    }

    /* CHIPS */
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      list-style: none;
      padding: 0;
      margin: 0;
    }

    .chip {
      background: var(--black-2);
      border: 2px solid var(--blue);
      color: var(--iri-cyan);
      padding: 8px 16px;
      font-size: 0.82rem;
      font-weight: 700;
      transition: transform 0.12s ease, background 0.12s ease, color 0.12s ease;
    }

    .chip:hover {
      background: var(--blue);
      color: var(--black);
      transform: translate(-2px, -2px);
    }

    .chip.on-hold {
      border-color: var(--red);
      color: var(--red);
      opacity: 0.6;
      text-decoration: line-through;
    }

    .chip .status {
      display: block;
      font-size: 0.62rem;
      font-weight: 400;
      text-decoration: none;
      margin-top: 2px;
      text-transform: none;
    }

    /* PROJECT CARD */
    .card {
      position: relative;
      padding: 30px 30px;
      background: var(--black-2);
      border: 2px solid var(--blue);
    }

    .card h3 {
      font-family: 'Fraunces', serif;
      font-style: italic;
      font-weight: 900;
      margin: 0 0 10px;
      font-size: 1.4rem;
      color: var(--paper);
    }

    .card p {
      margin: 0;
      font-size: 0.9rem;
      color: var(--dim);
    }

    .card .tag {
      position: absolute;
      top: -14px;
      right: 20px;
      background: var(--red);
      color: var(--black);
      padding: 4px 10px;
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
    }

    /* CONTACT */
    .contact-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }

    .contact-btn {
      flex: 1 1 240px;
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 18px;
      background: var(--black-2);
      border: 2px solid var(--blue);
      color: var(--paper);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.86rem;
      transition: border-color 0.12s ease, transform 0.12s ease;
    }

    .contact-btn:hover {
      border-color: var(--red);
      transform: translate(3px, -3px);
    }

    .contact-icon {
      width: 28px;
      height: 28px;
      background: var(--red);
      color: var(--black);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.85rem;
      font-weight: 700;
      flex-shrink: 0;
    }

    footer {
      margin-top: 80px;
      text-align: center;
      font-size: 0.7rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--red);
    }

    @media (max-width: 640px) {
      .inner { padding: 40px 22px 60px; }
      .paint-flow { width: 90%; right: -25%; }
    }
  </style>
</head>
<body>

  <div class="panel">
    <div class="corner corner-tl"></div>
    <div class="corner corner-br"></div>

    <div class="inner">

      <div class="hero">
        <svg class="paint-flow" viewBox="0 0 300 600" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
          <defs>
            <linearGradient id="paint" x1="10%" y1="0%" x2="90%" y2="100%">
              <stop offset="0%" stop-color="#9b5cff"/>
              <stop offset="18%" stop-color="#2f5fff"/>
              <stop offset="40%" stop-color="#5be9ff"/>
              <stop offset="55%" stop-color="#2f5fff"/>
              <stop offset="75%" stop-color="#ff6ec7"/>
              <stop offset="100%" stop-color="#2f5fff"/>
            </linearGradient>
            <filter id="fluid">
              <feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="2" seed="7" result="noise"/>
              <feDisplacementMap in="SourceGraphic" in2="noise" scale="35"/>
            </filter>
          </defs>
          <g filter="url(#fluid)">
            <path fill="url(#paint)" d="M230,-20 C150,40 260,120 190,180
              C120,240 40,230 60,300
              C80,370 200,360 170,440
              C150,500 70,520 90,600
              L300,600 L300,-20 Z" opacity="0.92"/>
            <path fill="url(#paint)" d="M260,-20 C210,30 280,90 250,140
              C220,190 170,200 185,260
              L300,260 L300,-20 Z" opacity="0.5"/>
          </g>
        </svg>

        <div class="hero-content">
          <div class="specimen-box">01 &middot; SS &middot; PERSONAL CV</div>
          <h1>Stefan<br>Sendyk</h1>
          <p class="tagline">Editor. Presenter. Pitch builder.</p>
        </div>
      </div>

      <section>
        <div class="section-head">
          <span class="section-num">01</span>
          <h2>Interests</h2>
        </div>
        <ul class="chips">
          <li class="chip">Drama</li>
          <li class="chip">Editing</li>
          <li class="chip">Swimming</li>
          <li class="chip on-hold">Padel<span class="status">on hold — back after Feb 1</span></li>
          <li class="chip on-hold">Running<span class="status">on hold — back after Feb 1</span></li>
          <li class="chip on-hold">Hiking<span class="status">on hold — back after Feb 1</span></li>
        </ul>
      </section>

      <svg class="flow-divider" viewBox="0 0 800 20" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="div1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#2f5fff"/>
            <stop offset="30%" stop-color="#5be9ff"/>
            <stop offset="60%" stop-color="#9b5cff"/>
            <stop offset="100%" stop-color="#ff6ec7"/>
          </linearGradient>
        </defs>
        <path d="M0,10 C100,2 200,18 300,10 C400,2 500,18 600,10 C700,2 750,14 800,8" stroke="url(#div1)" stroke-width="4" fill="none"/>
      </svg>

      <section>
        <div class="section-head">
          <span class="section-num">02</span>
          <h2>Skills</h2>
        </div>
        <ul class="chips">
          <li class="chip">Basic programming</li>
          <li class="chip">Russian (fluent)</li>
          <li class="chip">English (fluent)</li>
          <li class="chip">Spanish (fluent)</li>
          <li class="chip">French (partial)</li>
          <li class="chip">Advanced editing</li>
          <li class="chip on-hold">High running speed<span class="status">currently unavailable</span></li>
          <li class="chip">Navigation skills</li>
          <li class="chip">Pitching</li>
          <li class="chip">Presentation making</li>
        </ul>
      </section>

      <section>
        <div class="section-head">
          <span class="section-num">03</span>
          <h2>Projects</h2>
        </div>
        <div class="card">
          <span class="tag">Pitch</span>
          <h3>EPlantic Pitch</h3>
          <p>A pitch project by Stefan Sendyk.</p>
        </div>
      </section>

      <section>
        <div class="section-head">
          <span class="section-num">04</span>
          <h2>Contact</h2>
        </div>
        <div class="contact-grid">
          <a class="contact-btn" href="mailto:spsendyk@gmail.com">
            <span class="contact-icon">@</span>
            spsendyk@gmail.com
          </a>
          <a class="contact-btn" href="mailto:spsendyk@icloud.com">
            <span class="contact-icon">@</span>
            spsendyk@icloud.com
          </a>
        </div>
      </section>

      <footer>&copy; Stefan Sendyk — No. 05 — Est. 2026</footer>
    </div>
  </div>

</body>
</html>