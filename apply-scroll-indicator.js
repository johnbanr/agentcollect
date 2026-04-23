#!/usr/bin/env node
// Inject scroll-indicator into all AgentCollect blog articles. Idempotent.
const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const MARKER = 'scroll-indicator-section';

const CSS_BLOCK = `
        .reading-progress{position:fixed;top:64px;left:0;right:0;height:3px;background:rgba(67,49,150,.07);z-index:999;pointer-events:none}
        .reading-progress-bar{height:100%;width:0;background:linear-gradient(90deg,var(--purple,#433196),var(--indigo,#4F46E5));transition:width .08s linear;box-shadow:0 0 8px rgba(79,70,229,.3)}
        .scroll-indicator{position:fixed;right:24px;top:50%;transform:translateY(-50%) translateX(20px);z-index:940;width:210px;background:rgba(255,255,255,.94);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border,#E8ECF2);border-radius:18px;padding:18px;box-shadow:0 10px 30px rgba(11,27,61,.08);opacity:0;transition:opacity .3s ease, transform .3s ease;pointer-events:none}
        .scroll-indicator.visible{opacity:1;transform:translateY(-50%) translateX(0);pointer-events:auto}
        .scroll-indicator-bar{height:4px;background:#F1EDF9;border-radius:100px;overflow:hidden;margin-bottom:14px}
        .scroll-indicator-fill{height:100%;width:0;background:linear-gradient(90deg,var(--purple,#433196),var(--indigo,#4F46E5));border-radius:100px;transition:width .1s linear}
        .scroll-indicator-section{font-family:var(--display,'Plus Jakarta Sans',sans-serif);min-height:44px}
        .scroll-indicator-cat{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:var(--purple,#433196);margin-bottom:3px}
        .scroll-indicator-title{font-size:13px;color:var(--text-mid,#374151);line-height:1.35;font-weight:500;font-family:var(--sans,'Inter',sans-serif)}
        .scroll-indicator-top{margin-top:12px;padding-top:12px;border-top:1px solid var(--border,#E8ECF2);width:100%;display:flex;align-items:center;justify-content:center;gap:6px;background:none;border-left:none;border-right:none;border-bottom:none;cursor:pointer;font-family:var(--sans,'Inter',sans-serif);font-size:11px;color:var(--text-dim,#94A3B8);transition:color .2s;padding-bottom:0}
        .scroll-indicator-top:hover{color:var(--purple,#433196)}
        .scroll-indicator-top svg{width:10px;height:10px}
        .scroll-indicator-mobile{position:fixed;left:0;right:0;bottom:0;z-index:940;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-top:1px solid var(--border,#E8ECF2);opacity:0;transform:translateY(100%);transition:opacity .3s ease, transform .3s ease;display:none}
        .scroll-indicator-mobile.visible{opacity:1;transform:translateY(0)}
        .scroll-indicator-mobile-bar{height:3px;background:#F1EDF9}
        .scroll-indicator-mobile-fill{height:100%;width:0;background:linear-gradient(90deg,var(--purple,#433196),var(--indigo,#4F46E5));transition:width .1s linear}
        .scroll-indicator-mobile-inner{display:flex;align-items:center;gap:12px;padding:10px 16px;max-width:720px;margin:0 auto}
        .scroll-indicator-mobile-text{flex:1;min-width:0}
        .scroll-indicator-mobile-cat{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--purple,#433196);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
        .scroll-indicator-mobile-title{font-size:12px;color:var(--text-muted,#64748B);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}
        .scroll-indicator-mobile-top{width:36px;height:36px;border-radius:50%;background:var(--purple,#433196);color:#fff;display:flex;align-items:center;justify-content:center;border:none;cursor:pointer;flex-shrink:0}
        .scroll-indicator-mobile-top svg{width:16px;height:16px}
        @media(max-width:1080px){.scroll-indicator{display:none}.scroll-indicator-mobile{display:block}}
`;

const HTML_BLOCK = `
<div class="reading-progress" aria-hidden="true"><div class="reading-progress-bar"></div></div>
<aside class="scroll-indicator" id="scrollIndicator" aria-hidden="true">
    <div class="scroll-indicator-bar"><div class="scroll-indicator-fill" id="siBar"></div></div>
    <div class="scroll-indicator-section">
        <div class="scroll-indicator-cat" id="siCat">&nbsp;</div>
        <div class="scroll-indicator-title" id="siTitle">&nbsp;</div>
    </div>
    <button class="scroll-indicator-top" id="siTop" aria-label="Back to top">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>
        Back to top
    </button>
</aside>
<div class="scroll-indicator-mobile" id="scrollIndicatorMobile" aria-hidden="true">
    <div class="scroll-indicator-mobile-bar"><div class="scroll-indicator-mobile-fill" id="siMobBar"></div></div>
    <div class="scroll-indicator-mobile-inner">
        <div class="scroll-indicator-mobile-text">
            <div class="scroll-indicator-mobile-cat" id="siMobCat">&nbsp;</div>
            <div class="scroll-indicator-mobile-title" id="siMobTitle">&nbsp;</div>
        </div>
        <button class="scroll-indicator-mobile-top" id="siMobTop" aria-label="Back to top">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 15l-6-6-6 6"/></svg>
        </button>
    </div>
</div>
`;

const JS_BLOCK = `
<script>
(function(){
    var topBar = document.querySelector('.reading-progress-bar');
    var articleBody = document.querySelector('.article-body') || document.querySelector('article');
    if (!articleBody) return;
    var headings = articleBody.querySelectorAll('h2[id]');
    var sections = [];
    headings.forEach(function(h){
        var cloned = h.cloneNode(true);
        var numSpan = cloned.querySelector('.num');
        if (numSpan) numSpan.remove();
        sections.push({ id: h.id, title: (cloned.textContent||'').trim() });
    });
    if (sections.length === 0) return;
    var indicator = document.getElementById('scrollIndicator');
    var indicatorMob = document.getElementById('scrollIndicatorMobile');
    var siBar = document.getElementById('siBar');
    var siMobBar = document.getElementById('siMobBar');
    var siCat = document.getElementById('siCat');
    var siTitle = document.getElementById('siTitle');
    var siMobCat = document.getElementById('siMobCat');
    var siMobTitle = document.getElementById('siMobTitle');
    var siTop = document.getElementById('siTop');
    var siMobTop = document.getElementById('siMobTop');
    function scrollToTop(){ window.scrollTo({top:0, behavior:'smooth'}); }
    if (siTop) siTop.addEventListener('click', scrollToTop);
    if (siMobTop) siMobTop.addEventListener('click', scrollToTop);
    function update() {
        var rect = articleBody.getBoundingClientRect();
        var total = Math.max(1, articleBody.offsetHeight - window.innerHeight + 240);
        var scrolled = Math.max(0, -rect.top);
        var pct = Math.min(100, Math.max(0, (scrolled / total) * 100));
        if (topBar) topBar.style.width = pct + '%';
        if (siBar) siBar.style.width = pct + '%';
        if (siMobBar) siMobBar.style.width = pct + '%';
        var show = window.scrollY > 400;
        if (indicator) indicator.classList.toggle('visible', show);
        if (indicatorMob) indicatorMob.classList.toggle('visible', show);
        var current = null, idx = 0;
        for (var i=0;i<sections.length;i++){
            var el = document.getElementById(sections[i].id);
            if (el) { var r = el.getBoundingClientRect(); if (r.top <= 200){ current = sections[i]; idx = i; } }
        }
        if (current) {
            var cat = 'Section ' + (idx+1) + ' of ' + sections.length;
            if (siCat) siCat.textContent = cat;
            if (siTitle) siTitle.textContent = current.title;
            if (siMobCat) siMobCat.textContent = cat;
            if (siMobTitle) siMobTitle.textContent = current.title;
        }
    }
    window.addEventListener('scroll', update, {passive:true});
    window.addEventListener('resize', update, {passive:true});
    update();
})();
</script>
`;

function inject(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    if (content.includes(MARKER)) return 'skipped (already has)';
    if (!/class="article-body"|<article/.test(content)) return 'skipped (no article body)';
    const styleClose = content.indexOf('</style>');
    if (styleClose === -1) return 'failed (no </style>)';
    content = content.slice(0, styleClose) + CSS_BLOCK + content.slice(styleClose);
    const bodyOpen = content.match(/<body[^>]*>/);
    if (!bodyOpen) return 'failed (no <body>)';
    const bodyEnd = bodyOpen.index + bodyOpen[0].length;
    content = content.slice(0, bodyEnd) + '\n' + HTML_BLOCK + content.slice(bodyEnd);
    const bodyClose = content.lastIndexOf('</body>');
    if (bodyClose === -1) return 'failed (no </body>)';
    content = content.slice(0, bodyClose) + JS_BLOCK + '\n' + content.slice(bodyClose);
    fs.writeFileSync(filePath, content, 'utf8');
    return '✅ injected';
}

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html') && f !== 'index.html');
console.log('Found ' + files.length + ' articles');
const stats = { injected: 0, skipped: 0, failed: 0 };
for (const f of files) {
    const result = inject(path.join(BLOG_DIR, f));
    const key = result.includes('✅') ? 'injected' : result.includes('skipped') ? 'skipped' : 'failed';
    stats[key]++;
    console.log('  ' + f.padEnd(60) + ' ' + result);
}
console.log('\nSummary:', stats);
