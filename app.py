import streamlit as st
import json
from pathlib import Path
import base64
from streamlit_lottie import st_lottie
from html import escape

ASSETS = Path(__file__).parent / "assets"
COVER_URL = "https://linkstorage.linkfire.com/medialinks/images/3595ab1c-9d2e-4f78-9a92-775e7a7e65d9/artwork-440x440.jpg"

st.set_page_config(page_title='Dear Santa, I Got Carried Away.', page_icon='🎅', layout='centered')
PURCHASE_URL = 'https://www.fnac.com/a14073727/Pomme-Les-failles-cachees-Vinyle-album'
CLUES = [
    ('My first is a plant on which grapes grow.', 'vine', '🍇', 'It starts with a V and rhymes with "fine".', "Of course you'd know that one. It's wine-related."),
    ("My second is what you are when you're unwell.", 'ill', '🤒', 'Three letters. Starts with an I.', "Good to see your 364 days off haven't affected your cognitive abilities."),
    ('My third is what you say when you leave.', 'bye', '👋', 'Three letters. An informal way of saying goodbye.', "Coincidentally, that's also what you'll be saying to your money."),
    ('My fourth is an apple, but make it French.', 'pomme', '🍎', "Five letters. It's a fruit, not a tech company.", 'At least that Duolingo subscription is paying off.'),
]
ERRORS = ['Unfortunately, enthusiasm is not a substitute for accuracy.', 'The elves are starting to question your qualifications.', 'Should we involve an adult?', 'This is becoming a Christmas miracle in reverse.', 'For legal reasons, the Department of Gift Procurement refuses to comment.']
for key, value in dict(step=0, attempts=0, hint=False, started=False, celebrated=False).items():
    if key not in st.session_state:
        st.session_state[key] = value
s = st.session_state
st.markdown(r'''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
.stApp {background:radial-gradient(ellipse at 50% 0%,#a52c3b 0%,#781c29 55%,#430b17 100%);color:#fff4db;}
.block-container {max-width:760px;padding:2rem 1.35rem 3rem;}
[data-testid="stHeader"] {background:transparent;}
html,body,[class*="st-"] {font-family:'DM Sans',sans-serif;}
h1,h2,h3 {font-family:'Playfair Display',Georgia,serif!important;}
.hero {position:relative;overflow:hidden;border:1px solid #a88d55;border-radius:24px;background:linear-gradient(155deg,#922536,#641321);text-align:center;padding:0 20px 28px;box-shadow:0 18px 55px #37081180;}
.hero .eyebrow {font-size:10px;letter-spacing:.18em;color:#dfc58a;text-transform:uppercase;}
.hero h1 {font-size:clamp(2rem,6vw,3.1rem);line-height:1.1;margin:12px 0;color:#fff0d0;}
.hero .tagline {font-size:.88rem;color:#d8ccb3;margin:8px 0 0;}
.hero svg {display:block;width:100%;height:auto;max-height:160px;}
.sleigh {animation:flight 15s linear infinite;}
.bob {animation:bob 2.5s ease-in-out infinite;}
.flake {animation:twinkle 3s ease-in-out infinite alternate;}
@keyframes flight {0%{transform:translate(-250px,8px)} 100%{transform:translate(740px,-12px)}}
@keyframes bob {50%{transform:translateY(-7px)}}
@keyframes twinkle {0%{opacity:.15}100%{opacity:.95}}
.letter {background:#fff1d6;color:#4b302b;border-radius:16px;padding:25px 27px;margin-top:8px;box-shadow:0 12px 32px #37081140;border:1px solid #d8bf8b;}
.letter p {line-height:1.65;margin:0 0 14px;font-size:1rem;}.letter p:last-child {margin:0;}
.letter .salutation {font:700 1.45rem 'Playfair Display',Georgia,serif;color:#781c29;}
.tile {border:1px solid #aa7359;border-radius:14px;padding:13px 2px;text-align:center;background:#681622;min-height:94px;}.tile.active {border-color:#e0c38a;background:#922536;}.tile.done {border-color:#e4c17a;}.tile span{display:block;font-size:1.45rem;}.tile b{font-size:.85rem;letter-spacing:.05em;}.tile small{display:block;color:#d0c6af;font-size:.65rem;margin-top:4px;}
.stButton button,.stLinkButton a,[data-testid="stFormSubmitButton"] button {border-radius:12px;min-height:48px;font-weight:700;transition:transform .2s,box-shadow .2s;}
.stButton button:hover,.stLinkButton a:hover {transform:translateY(-2px);box-shadow:0 5px 18px #0003;}
button[kind="primary"],a[kind="primary"] {background:#e3c48b!important;color:#781c29!important;border:1px solid #e3c48b!important;}
[data-testid="stForm"] {border:1px solid #b8924f;border-radius:16px;background:#681622;padding:18px;}
[data-testid="stTextInput"] input {background:#53141d;}
[data-testid="stAlert"] {border-radius:12px;}
 .progress-label {padding-top:24px;display:flex;justify-content:space-between;color:#E4C17A;font-size:.85rem;margin-bottom:8px;}
.progress-track {margin-bottom:24px;width:100%;height:8px;background:#53141D;border-radius:20px;overflow:hidden;}
.progress-fill {height:100%;background:#E4C17A;border-radius:20px;transition:width .3s ease;}
.feedback {color:#E4C17A;font-size:.85rem;font-style:italic;margin:8px 0 16px;background:transparent;border:0;padding:0;}
.feedback:not(.failure):not(.hint) {margin-top:18px!important;margin-bottom:2px!important;}
.feedback.failure {color:#ffc1c1;}
.feedback.hint {color:#E4C17A;}
.final-heading,.final-heading h2,.final-heading h3,.final-heading p,.final-note {text-align:center!important;}
.final-heading h2 {color:#E4C17A;}
.final-heading p.rebus {font-size:.85rem;color:#E4C17A;}
.final-note {color:#fff4df;margin:28px 0 12px!important;}
.final-notes {text-align:center;margin:28px 0 16px;color:#fff4df;}
.final-notes p {text-align:center!important;font-family:"DM Sans",sans-serif;font-size:1rem;font-style:normal;font-weight:400;color:#fff4df;margin:0 0 8px!important;}
.final-notes p:last-child {margin-bottom:0!important;}
[data-testid="stLinkButton"] a,[data-testid="stLinkButton"] a p {font-size:18px!important;font-weight:700!important;}
[data-testid="stLinkButton"] a {padding:12px 20px!important;}
.gift {text-align:center;border:1px solid #a88d55;border-radius:20px;background:#641321;padding:24px 15px;}.gift svg{width:230px;max-width:100%;}.gift .gift-title{display:block;width:100%;padding:0!important;margin:18px auto 6px!important;text-align:center!important;color:#fff1d6;font:700 clamp(1.5rem,5vw,2rem)/1.25 Playfair Display,Georgia,serif;box-sizing:border-box;}.gift p{text-align:center!important;}.gift p{color:#d8c9aa;}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.sleigh{transform:translate(225px,0)}}
@media(max-width:500px){.block-container{padding:1rem .85rem 2rem}.letter{padding:20px}.tile{padding:8px 0;min-height:80px}.tile b{font-size:.7rem}}

.cover-frame {display:inline-block;padding:7px;border:1px solid #e4c17a;background:#53141d;box-shadow:0 16px 34px #30081180;max-width:85%;animation:reveal .85s ease-out both;position:relative;}
.cover-frame img {display:block;width:280px;max-width:100%;height:auto;}
.gift .gift-title,.gift p {animation:reveal .7s .25s both;}
@keyframes reveal {from{opacity:0;transform:translateY(12px) scale(.94)}to{opacity:1;transform:translateY(0) scale(1)}}
.hero::before {content:'✦   ·   ✧   ·   ✦';display:block;color:#e4c17a;letter-spacing:1em;font-size:15px;animation:twinkle 3s infinite alternate;margin-bottom:12px;}
@media(prefers-reduced-motion:reduce){.cover-frame,.gift .gift-title,.gift p,.hero::before{animation:none!important}}
</style>''', unsafe_allow_html=True)
# Original artwork only: download the Lottie JSON from Rocío's page.
if (ASSETS / "santa_sleigh.json").is_file():
    try:
        animation = json.loads((ASSETS / "santa_sleigh.json").read_text(encoding="utf-8"))
        # Use a centered 130px-high composition, regardless of which previous
        # crop is currently installed. Preserve the horizontal motion.
        old_height = animation["h"]
        if old_height != 130:
            shift = (old_height - 130) / 2
            for frame in animation["layers"][0]["ks"]["p"]["k"]:
                frame["s"][1] -= shift
            animation["h"] = 130
        st_lottie(animation, height=95, loop=True, quality="high", key="sleigh")
    except (ValueError, OSError):
        pass
st.markdown('''<div class="hero" style="padding-top:25px"><div class="eyebrow">✦ North Pole · Department of Gift Procurement ✦</div><h1>Dear Santa, I Got Carried Away.</h1><p class="tagline">Making Christmas unnecessarily complicated since 2026.</p></div>''', unsafe_allow_html=True)
if not s.started:
    st.markdown('''<div class="letter"><p class="salutation">Dear Santa,</p><p>Apparently, submitting a Christmas wish without creating an entire web application was an option. Unfortunately, I have free time and questionable priorities.</p><p>Please complete the following assessment to unlock the privilege of spending your own money.</p><p>Best of luck. 😇</p></div>''', unsafe_allow_html=True)
    st.divider()
    if st.button('Report for duty, Santa →', type='primary', use_container_width=True):
        s.started = True
        st.rerun()
    st.stop()
progress = s.step * 25
st.markdown(f'''<div class="progress-label"><span>Gift procurement progress</span><span>{progress}%</span></div><div class="progress-track" role="progressbar" aria-label="Gift procurement progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{progress}"><div class="progress-fill" style="width:{progress}%"></div></div>''', unsafe_allow_html=True)
for i, col in enumerate(st.columns(4)):
    with col:
        solved = i < s.step
        status = 'Solved' if solved else 'Current' if i == s.step else 'Locked'
        style = 'done' if solved else 'active' if i == s.step else ''
        st.markdown(f'<div class="tile {style}"><span>{CLUES[i][2] if solved else "🔒"}</span><b>{CLUES[i][1].upper() if solved else "???"}</b><small>{status}</small></div>', unsafe_allow_html=True)
if s.step:
    st.markdown(f'<p class="feedback">✓ {escape(CLUES[s.step-1][4])}</p>', unsafe_allow_html=True)
if not s.step or s.step == 4:
    st.divider()
if s.step < 4:
    question, correct, emoji, hint, feedback = CLUES[s.step]
    st.caption(f'CHALLENGE {s.step+1} OF 4')
    st.subheader(question)
    with st.form(f'clue_{s.step}'):
        answer = st.text_input('Your highly educated guess...')
        submit = st.form_submit_button('Submit answer', type='primary', use_container_width=True)
    if submit:
        if answer.strip().casefold() == correct:
            s.step += 1
            s.attempts = 0
            s.hint = False
            st.rerun()
        elif answer.strip():
            s.attempts += 1
    if s.attempts:
        st.markdown(f'<p class="feedback failure">✗ {escape(ERRORS[min(s.attempts-1, len(ERRORS)-1)])}</p>', unsafe_allow_html=True)
    if st.button('Dismiss elf assistance' if s.hint else '💡 Request elf assistance', use_container_width=True):
        s.hint = not s.hint
        st.rerun()
    if s.hint:
        st.markdown(f'<p class="feedback hint">💡 {escape(hint)}</p>', unsafe_allow_html=True)
    st.caption('The elves are monitoring your performance.')
else:
    if not s.celebrated:
        st.snow()
        s.celebrated = True
    st.markdown('''<div class="final-heading"><h2>🎉 Congratulations, Santa!</h2><p>Against all odds, you've successfully completed the assessment.</p><h3>🍇 + 🤒 + 👋 + 🍎</h3><p class="rebus">VINE + ILL + BYE + POMME</p></div>''', unsafe_allow_html=True)
    cover = ASSETS / "cover.jpg"
    image_url = "data:image/jpeg;base64," + base64.b64encode(cover.read_bytes()).decode() if cover.is_file() else COVER_URL
    st.markdown(f'''<div class="gift"><div class="cover-frame"><img src="{image_url}" alt="Pomme — Les failles cachées, original album cover" /></div><div class="gift-title" role="heading" aria-level="2">A vinyl by Pomme</div><p>Les failles cachées</p></div>''', unsafe_allow_html=True)
    st.markdown("""<div class="final-notes"><p>I hope you enjoyed this entirely avoidable experience.</p><p>You've wasted your time. Now it's time to waste your money. Merry Christmas!</p></div>""", unsafe_allow_html=True)
    st.link_button('🛒 Proceed to financial damage', PURCHASE_URL, use_container_width=True, type='primary')
st.divider()
if st.button('↺ Restart mission'):
    for key in list(s.keys()):
        del s[key]
    st.rerun()
