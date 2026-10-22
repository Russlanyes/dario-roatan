#!/usr/bin/env python3
"""Static generator for the merged Darío Reyes site (DR Lawn & Landscape + Island Pest Control).

Run:  python3 build.py   -> writes index.html, es/index.html, lawn/, pest/, es/jardineria/, es/plagas/,
      privacy/, terms/, legal/, es/privacidad/, es/terminos/, es/aviso-legal/, 404.html, sitemap.xml, robots.txt,
      vercel.json (security headers; CSP hashes for the inline scripts are computed here). All copy lives in this file (EN + ES side by side).
To move to a custom domain: change BASE below, rebuild, add the domain in Vercel (or a CNAME file for Pages).
"""
import os
from urllib.parse import quote
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://dario-roatan.vercel.app/"
LAWN = "50498350265"
PEST = "50488695915"
LAWN_TEL, LAWN_SHOW = "+50498350265", "+504 9835-0265"
PEST_TEL, PEST_SHOW = "+50488695915", "+504 8869-5915"
YEAR = "2026"
ASSET_V = "20261022b"  # bump when styles.css / site.js change (assets are cached for 7 days)

PATHS = {
    ("home", "en"): "", ("home", "es"): "es/",
    ("lawn", "en"): "lawn/", ("lawn", "es"): "es/jardineria/",
    ("pest", "en"): "pest/", ("pest", "es"): "es/plagas/",
    ("privacy", "en"): "privacy/", ("privacy", "es"): "es/privacidad/",
    ("terms", "en"): "terms/", ("terms", "es"): "es/terminos/",
    ("legal", "en"): "legal/", ("legal", "es"): "es/aviso-legal/",
}
LEGAL_PAGES = ("privacy", "terms", "legal")
ANALYTICS = """<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "138e7115485747debf387de6c91d4e39"}'></script><!-- End Cloudflare Web Analytics -->"""
LEGAL_UPDATED = ("October 22, 2026", "22 de octubre de 2026", "2026-10-22")
JS_FLAG = 'document.documentElement.classList.add("js")'  # only inline script on the pages; its hash is in the CSP
SPRITE = open(os.path.join(ROOT, "src", "sprite.svg")).read().strip()


def rel(frm, to):
    r = "../" * frm.count("/") + to
    return r or "./"


def wa(num, text):
    return f"https://wa.me/{num}?text={quote(text, safe='')}"


def ic(name, fill=False):
    cls = "icon icon-fill" if fill else "icon"
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def T(lang, en, es):
    return en if lang == "en" else es


def lawn_msg(lang, what=None):
    if what is None:
        return T(lang, "Hi DR Lawn & Landscape, I'd like a free quote for my property.",
                 "Hola DR Lawn & Landscape, me gustaría una cotización gratis para mi propiedad.")
    return T(lang, f"Hi DR Lawn & Landscape, I'd like a free quote for {what}.",
             f"Hola DR Lawn & Landscape, me gustaría una cotización gratis para {what}.")


def pest_msg(lang, tail=None):
    if tail is None:
        return T(lang, "Hi Island Pest Control, I'd like to book an inspection.",
                 "Hola Island Pest Control, quiero agendar una inspección.")
    return T(lang, f"Hi Island Pest Control, I'd like to book an inspection {tail}.",
             f"Hola Island Pest Control, quiero agendar una inspección {tail}.")


def a_wa(num, text, label, cls="btn btn-wa", sr=""):
    srs = f'<span class="sr-only">{sr}</span>' if sr else ""
    return (f'<a class="{cls}" href="{escape(wa(num, text))}" target="_blank" rel="noopener">'
            f'{ic("wa", True)}{label}{srs}</a>')


def a_tel(tel, show, label=None, cls="btn btn-ghost"):
    return f'<a class="{cls}" href="tel:{tel}">{ic("phone")}{label or show}</a>'


# ---------------------------------------------------------------- structured data
def jsonld(page, lang):
    import json
    person = {"@type": "Person", "@id": BASE + "#dario", "name": "Darío Reyes",
              "jobTitle": T(lang, "Agricultural engineer", "Ingeniero agrónomo"),
              "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universidad Nacional de Agricultura (UNAG)"}}
    addr = {"@type": "PostalAddress", "addressLocality": "Roatán", "addressRegion": "Islas de la Bahía", "addressCountry": "HN"}
    lawn = {"@type": "LocalBusiness", "@id": BASE + "#lawn", "name": "DR Lawn & Landscape Maintenance",
            "slogan": "Beautiful Outdoors, Well Maintained", "url": BASE + PATHS[("lawn", lang)],
            "telephone": LAWN_TEL, "logo": BASE + "assets/logo-dr-lawn.jpg", "image": BASE + "assets/og-lawn-en.jpg",
            "address": addr, "areaServed": "Roatán, Bay Islands, Honduras", "founder": {"@id": BASE + "#dario"},
            "knowsLanguage": ["en", "es"]}
    pest = {"@type": "LocalBusiness", "@id": BASE + "#pest", "name": "Island Pest Control & Garden Care",
            "slogan": "Your peace of mind is our mission", "url": BASE + PATHS[("pest", lang)],
            "telephone": PEST_TEL, "logo": BASE + "assets/ipc-wordmark.png", "image": BASE + "assets/og-pest-en.jpg",
            "address": addr, "areaServed": "Roatán, Bay Islands, Honduras", "founder": {"@id": BASE + "#dario"},
            "knowsLanguage": ["en", "es"]}
    if page in LEGAL_PAGES:
        graph = [person, lawn, pest, {"@type": "WebPage", "@id": BASE + PATHS[(page, lang)], "url": BASE + PATHS[(page, lang)],
                                      "name": LEGAL[page][lang]["title"], "inLanguage": lang, "dateModified": LEGAL_UPDATED[2],
                                      "about": [{"@id": BASE + "#lawn"}, {"@id": BASE + "#pest"}]}]
    else:
        graph = {"home": [person, lawn, pest], "lawn": [person, lawn], "pest": [person, pest]}[page]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- shell
def head(page, lang, title, desc):
    path = PATHS[(page, lang)]
    en_url, es_url = BASE + PATHS[(page, "en")], BASE + PATHS[(page, "es")]
    a = rel(path, "assets/")
    og_key = "home" if page in LEGAL_PAGES else page  # legal pages reuse the home share image
    og_img = BASE + "assets/" + ("og-image.jpg" if og_key == "home" else f"og-{page}-{lang}.jpg")
    og_alt = {"home": T(lang, "DR Lawn & Landscape Maintenance and Island Pest Control & Garden Care logos. Darío Reyes, Roatán.",
                        "Logos de DR Lawn & Landscape Maintenance e Island Pest Control & Garden Care. Darío Reyes, Roatán."),
              "lawn": T(lang, "DR Lawn & Landscape Maintenance logo: lawn and landscape maintenance in Roatán, free quote on WhatsApp.",
                        "Logo de DR Lawn & Landscape Maintenance: jardinería y paisajismo en Roatán, cotización gratis por WhatsApp."),
              "pest": T(lang, "Island Pest Control & Garden Care ladybug mascot: pest control in Roatán, inspections on WhatsApp.",
                        "Mascota mariquita de Island Pest Control & Garden Care: control de plagas en Roatán, inspecciones por WhatsApp.")}[og_key]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{BASE + path}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="es" href="{es_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="theme-color" content="#234f17">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DR Lawn &amp; Landscape · Island Pest Control">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{BASE + path}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(og_alt)}">
<meta property="og:locale" content="{T(lang, 'en_US', 'es_HN')}">
<meta property="og:locale:alternate" content="{T(lang, 'es_HN', 'en_US')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="twitter:image:alt" content="{escape(og_alt)}">
<link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{a}favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{a}apple-touch-icon.png">
<link rel="preload" href="{a}fonts/dm-serif-display-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a}fonts/work-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}styles.css?v={ASSET_V}">
<script type="application/ld+json">
{jsonld(page, lang)}
</script>
<script>{JS_FLAG}</script>
</head>
<body>
{SPRITE}
<a class="skip" href="#main">{T(lang, "Skip to content", "Saltar al contenido")}</a>
"""


def header(page, lang):
    path = PATHS[(page, lang)]
    home = rel(path, PATHS[("home", lang)])
    other = "es" if lang == "en" else "en"
    other_href = rel(path, PATHS[(page, other)])
    a = rel(path, "assets/")
    if page == "home":
        links = [("#lawn", T(lang, "Lawn & Landscape", "Jardinería"), False),
                 ("#pest", T(lang, "Pest Control", "Control de plagas"), False),
                 ("#how", T(lang, "How we work", "Cómo trabajamos"), False),
                 ("#about", T(lang, "About", "Nosotros"), False),
                 ("#contact", T(lang, "Contact", "Contacto"), False)]
        cta = f'<a class="btn btn-terra btn-sm" href="#contact">{ic("wa", True)}{T(lang, "Contact us", "Contáctanos")}</a>'
    else:
        links = [(rel(path, PATHS[("lawn", lang)]), T(lang, "Lawn & Landscape", "Jardinería"), page == "lawn"),
                 (rel(path, PATHS[("pest", lang)]), T(lang, "Pest Control", "Control de plagas"), page == "pest"),
                 (home + "#how", T(lang, "How we work", "Cómo trabajamos"), False),
                 (home + "#about", T(lang, "About", "Nosotros"), False),
                 ((home if page in LEGAL_PAGES else "") + "#contact", T(lang, "Contact", "Contacto"), False)]
        if page in LEGAL_PAGES:  # no contact block on legal pages: send people to the home contact section
            cta = f'<a class="btn btn-terra btn-sm" href="{home}#contact">{ic("wa", True)}{T(lang, "Contact us", "Contáctanos")}</a>'
        elif page == "lawn":
            cta = a_wa(LAWN, lawn_msg(lang), T(lang, "Free quote", "Cotiza gratis"), "btn btn-wa btn-sm")
        else:
            cta = a_wa(PEST, pest_msg(lang), T(lang, "Book inspection", "Agenda inspección"), "btn btn-red btn-sm")
    cur_attr = ' aria-current="page"'
    lis = "".join(f'<li><a href="{h}"{cur_attr if cur else ""}>{t}</a></li>' for h, t, cur in links)
    if lang == "en":
        toggle = f'<span aria-current="true" lang="en">EN</span><a href="{other_href}" lang="es" hreflang="es" aria-label="Español">ES</a>'
    else:
        toggle = f'<a href="{other_href}" lang="en" hreflang="en" aria-label="English">EN</a><span aria-current="true" lang="es">ES</span>'
    return f"""<header class="site-header">
  <div class="wrap nav" id="nav">
    <a class="brand" href="{home}" aria-label="DR Lawn &amp; Landscape · Island Pest Control, {T(lang, 'home', 'inicio')}">
      <span class="brand-marks"><img class="m-dr" src="{a}logo-dr-lawn.jpg" width="50" height="50" alt=""><img class="m-ipc" src="{a}ipc-mark.png" width="30" height="39" alt=""></span>
      <span class="brand-name" aria-hidden="true"><span class="l1">DR Lawn &amp; Landscape</span><span class="sep">·</span><span class="l2">Island Pest Control</span><small>Darío Reyes · Roatán</small></span>
    </a>
    <div class="lang" role="group" aria-label="{T(lang, 'Language', 'Idioma')}">{toggle}</div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="{T(lang, 'Menu', 'Menú')}">{ic("menu")}</button>
    <nav class="nav-menu" id="nav-menu" aria-label="{T(lang, 'Menu', 'Menú')}">
      <ul class="nav-links">{lis}</ul>
      {cta}
    </nav>
  </div>
</header>
"""


def footer(page, lang):
    path = PATHS[(page, lang)]
    a = rel(path, "assets/")
    home = rel(path, PATHS[("home", lang)])
    lawnp, pestp = rel(path, PATHS[("lawn", lang)]), rel(path, PATHS[("pest", lang)])
    cur = ' aria-current="page"'
    legal_links = '<span aria-hidden="true">·</span>'.join(
        f'<a href="{rel(path, PATHS[(k, lang)])}"{cur if k == page else ""}>{LEGAL[k][lang]["short"]}</a>' for k in LEGAL_PAGES)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <span class="fm"><img src="{a}logo-dr-lawn.jpg" width="54" height="54" alt="" loading="lazy"></span>
          <span class="fm"><img src="{a}ipc-mark.png" width="40" height="52" alt="" loading="lazy"></span>
        </div>
        <p style="margin-top:14px"><strong style="font-family:var(--serif);font-weight:400;font-size:1.2rem;color:#fff">DR Lawn &amp; Landscape Maintenance<br>Island Pest Control &amp; Garden Care</strong></p>
        <p>Darío Reyes · {T(lang, "Agricultural engineer (UNAG)", "Ingeniero agrónomo (UNAG)")}</p>
        <span class="footer-tag">{T(lang, "Your property, our passion, your peace of mind.", "Tu propiedad, nuestra pasión, tu tranquilidad.")}</span>
      </div>
      <nav aria-labelledby="f-lawn-{lang}"><h2 id="f-lawn-{lang}">{T(lang, "Lawn & Landscape", "Jardinería y paisajismo")}</h2><ul>
        <li><a href="{lawnp}">{T(lang, "Mowing", "Corte de césped")}</a></li>
        <li><a href="{lawnp}">{T(lang, "Trimming", "Recorte y bordes")}</a></li>
        <li><a href="{lawnp}">{T(lang, "Clean Up", "Limpieza de jardín")}</a></li>
        <li><a href="{lawnp}">{T(lang, "Landscaping", "Jardinería y paisajismo")}</a></li>
        <li><a href="{lawnp}">{T(lang, "Irrigation Maintenance", "Mantenimiento de riego")}</a></li></ul></nav>
      <nav aria-labelledby="f-pest-{lang}"><h2 id="f-pest-{lang}">{T(lang, "Pest Control & Garden Care", "Control de plagas y jardines")}</h2><ul>
        <li><a href="{pestp}">{T(lang, "Residential pest control", "Control de plagas residencial")}</a></li>
        <li><a href="{pestp}">{T(lang, "Commercial pest control", "Control de plagas comercial")}</a></li>
        <li><a href="{pestp}">{T(lang, "Vacation rentals & Airbnb", "Rentas vacacionales y Airbnb")}</a></li>
        <li><a href="{pestp}">{T(lang, "Mosquito & rodent control", "Control de mosquitos y roedores")}</a></li>
        <li><a href="{pestp}">{T(lang, "Garden care", "Cuidado de jardines")}</a></li></ul></nav>
      <div><h2>{T(lang, "Contact", "Contacto")}</h2>
        <ul>
          <li>{T(lang, "Lawn", "Jardinería")}: <a href="{escape(wa(LAWN, lawn_msg(lang)))}" target="_blank" rel="noopener">WhatsApp {LAWN_SHOW}</a></li>
          <li>{T(lang, "Pest", "Plagas")}: <a href="{escape(wa(PEST, pest_msg(lang)))}" target="_blank" rel="noopener">WhatsApp {PEST_SHOW}</a></li>
          <li>{T(lang, "Roatán, Bay Islands, Honduras", "Roatán, Islas de la Bahía, Honduras")}</li>
          <li><a href="{home}#about">{T(lang, "About Darío", "Sobre Darío")}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {YEAR} DR Lawn &amp; Landscape Maintenance · Island Pest Control &amp; Garden Care. {T(lang, "All rights reserved.", "Todos los derechos reservados.")}</span>
      <nav class="footer-legal" aria-label="{T(lang, 'Legal', 'Legal')}">{legal_links}</nav>
      <span>{T(lang, "Roatán, Bay Islands, Honduras", "Roatán, Islas de la Bahía, Honduras")}</span>
    </div>
  </div>
</footer>

<div class="wa-bar">
  <a class="btn btn-wa" href="{escape(wa(LAWN, lawn_msg(lang)))}" target="_blank" rel="noopener">{ic("wa", True)}<span>{T(lang, "Lawn quote", "Jardinería")}<small>{LAWN_SHOW}</small></span></a>
  <a class="btn btn-red" href="{escape(wa(PEST, pest_msg(lang)))}" target="_blank" rel="noopener">{ic("wa", True)}<span>{T(lang, "Pest inspection", "Plagas")}<small>{PEST_SHOW}</small></span></a>
</div>

<script src="{a}site.js?v={ASSET_V}" defer></script>
{ANALYTICS}
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks
# Photo slots: designed placeholder panels (line-art in the site palette) with an honest caption that
# says which photo goes where. Swap each <figure class="ph"> for an <img> once Darío sends the photos.
G = '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
SOFT = 'fill="currentColor" fill-opacity=".13"'


def _leaf(x, y, rot=0, s=1.0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="M0 0C6-9 18-9 24 0C18 9 6 9 0 0Z" {SOFT}/><path d="M0 0H21"/></g>')


def _palm(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0C2-26 7-48 16-70"/>'
            '<path d="M16-70C-2-80-18-76-30-64"/><path d="M16-70C4-88-10-92-22-90"/><path d="M16-70C22-90 36-98 50-96"/>'
            '<path d="M16-70C34-76 50-70 58-56"/><path d="M16-70C16-84 10-96 2-104"/></g>')


def _bug(x, y, s=1.0):  # the IPC ladybug, as a small brand stamp
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="none"><circle cy="-12" r="6" fill="#1f2a1c"/>'
            '<circle r="12" fill="#b02a1f"/><path d="M0-12V12" stroke="#1f2a1c" stroke-width="1.6"/>'
            '<circle cx="-5" cy="-3" r="2.2" fill="#1f2a1c"/><circle cx="5" cy="-3" r="2.2" fill="#1f2a1c"/>'
            '<circle cx="-5" cy="5" r="2.2" fill="#1f2a1c"/><circle cx="5" cy="5" r="2.2" fill="#1f2a1c"/></g>')


def _waves(y, op=".45"):
    return (f'<path stroke-opacity="{op}" d="M-10 {y}c20-8 40-8 60 0s40 8 60 0 40-8 60 0 40 8 60 0 40-8 60 0 40 8 60 0 40-8 60 0"/>'
            f'<path stroke-opacity=".25" d="M10 {y + 14}c20-8 40-8 60 0s40 8 60 0 40-8 60 0 40 8 60 0 40-8 60 0 40 8 60 0"/>')


def _stripes(x0, x1, top, bottom, n, vp=(200, 40)):
    out, step = [], (x1 - x0) / n
    t = (top - vp[1]) / (bottom - vp[1])
    for i in range(0, n, 2):
        b0, b1 = x0 + i * step, x0 + (i + 1) * step
        a0, a1 = vp[0] + (b0 - vp[0]) * t, vp[0] + (b1 - vp[0]) * t
        out.append(f'<path d="M{a0:.0f} {top}L{a1:.0f} {top}L{b1:.0f} {bottom}L{b0:.0f} {bottom}Z" fill="currentColor" fill-opacity=".11" stroke="none"/>')
    return "".join(out)


def _scene(name):
    if name == "mow":
        art = (_stripes(-300, 700, 172, 300, 16) + G +
               '<circle cx="92" cy="80" r="17" stroke-opacity=".55"/><circle cx="92" cy="80" r="30" stroke-opacity=".18"/>'
               '<path stroke-opacity=".5" d="M0 172C70 160 130 166 200 158S330 150 400 164"/>' + _palm(300, 170) +
               "".join(f'<path stroke-opacity=".55" stroke-width="1.6" d="M{x} {y}q-2-7-5-9M{x} {y}q0-8 1-11M{x} {y}q3-7 6-8"/>' for x, y in [(44, 190), (128, 200), (236, 192), (356, 204), (90, 236), (300, 246)]) + '</g>')
    elif name == "hedge":
        bushes = [(36, 150, 128), (164, 266, 108), (280, 372, 140)]
        def bush(a, b, t):
            n = max(3, round((b - a) / 24)); w = (b - a) / n
            return f'<path d="M{a} 230V{t + 12}' + "".join(f'a{w / 2:.1f} {w / 2.4:.1f} 0 0 1 {w:.1f} 0' for _ in range(n)) + f'V230Z" {SOFT}/>'
        art = G + "".join(bush(a, b, t) for a, b, t in bushes)
        art += "".join(f'<path stroke-opacity=".45" d="M{x} {y}q4-5 8 0"/>' for x, y in
                       [(60, 160), (96, 178), (120, 150), (70, 205), (190, 140), (226, 160), (204, 196), (244, 210), (300, 170), (336, 158), (318, 206), (350, 196)])
        art += ('<path d="M20 232H380"/><path stroke-dasharray="1 9" stroke-width="2.4" d="M24 248H376"/>'
                '<g transform="translate(330 88) rotate(-30)" stroke-opacity=".7"><circle cx="-14" cy="18" r="7"/><circle cx="14" cy="18" r="7"/>'
                '<path d="M-9 13L10-24M9 13L-10-24"/></g></g>')
    elif name == "cleanup":
        art = (G + '<path d="M16 222H186M214 222H384"/>' +
               "".join(_leaf(x, y, r, .9) for x, y, r in [(34, 206, -20), (78, 214, 25), (120, 200, -60), (60, 186, 70), (150, 212, 10), (104, 176, 140), (160, 184, -35)]) +
               '<path stroke-opacity=".6" d="M40 160l26 10M48 168l6-10M132 150l22 16"/></g>' +
               _stripes(214, 384, 150, 222, 6, vp=(300, 60)) + G +
               '<path d="M300 222V196"/><circle cx="300" cy="186" r="14" ' + SOFT + '/><circle cx="286" cy="196" r="9" ' + SOFT + '/><circle cx="314" cy="196" r="9" ' + SOFT + '/>'
               '<path stroke-dasharray="6 8" stroke-opacity=".55" d="M200 18V282"/></g>'
               '<circle cx="200" cy="120" r="17" fill="#fffdf8" stroke="currentColor" stroke-width="2"/>'
               + G + '<path d="M194 114l-6 6 6 6M206 114l6 6-6 6"/></g>')
    elif name == "bed":
        art = (G + '<path d="M24 258C90 206 310 206 376 258" ' + SOFT + '/>'
               '<path stroke-dasharray="10 6" stroke-opacity=".6" d="M24 266C90 214 310 214 376 266"/>'
               '<path d="M130 236C128 200 120 170 98 146C122 150 140 172 142 204M142 236C150 196 170 168 198 156C188 182 166 206 150 236"/>'
               '<path d="M98 146C110 164 126 196 134 230" stroke-opacity=".5"/>'
               '<path d="M220 238V168M262 238V186"/>' +
               "".join(f'<g transform="translate({x} {y})"><circle r="6" {SOFT}/>' + "".join(
                   f'<ellipse rx="5" ry="9" transform="rotate({a}) translate(0 -13)" {SOFT}/>' for a in range(0, 360, 72)) + '</g>'
                       for x, y in [(220, 160), (262, 178)]) +
               '<path d="M300 238L286 182M306 238L306 172M312 238L330 184M318 238L346 200M294 238L272 204"/>'
               '<path d="M70 236V214M70 220C62 212 56 212 52 214M70 214C78 206 84 206 88 208"/></g>')
    elif name == "kitchen":
        tiles = "".join(f'<path d="M0 {y}H400"/>' for y in range(40, 170, 32)) + "".join(f'<path d="M{x} 30V170"/>' for x in range(30, 400, 46))
        art = (f'<g fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity=".22">{tiles}</g>' + G +
               '<path d="M0 170H400V186H0Z" ' + SOFT + '/><path d="M20 186V290M140 186V290M260 186V290M380 186V290"/>'
               '<path d="M118 214V236M162 214V236M238 214V236M282 214V236"/>'
               '<circle cx="232" cy="118" r="46" fill="#fffdf8" fill-opacity=".75" stroke-width="3"/>'
               '<path d="M265 151L298 184" stroke-width="9"/>'
               '<path stroke-dasharray="0 11" stroke-width="5" stroke-opacity=".7" d="M200 128C214 116 232 112 256 106"/></g>' + _bug(72, 80, 1.05))
    elif name == "rental":
        art = (G + _waves(258) + '<path d="M96 156L182 104L268 156"/><path d="M110 152V228H254V152" ' + SOFT + '/>'
               '<path d="M168 228V188H196V228M126 172H152V196H126ZM212 172H238V196H212Z"/>'
               '<path d="M90 228H276"/>' + _palm(306, 230, 1.05) +
               '<path d="M352 200L332 186M332 186L320 192"/>'
               '<path stroke-dasharray="0 10" stroke-width="4" stroke-opacity=".6" d="M318 190C300 176 288 170 272 172M318 196C298 196 286 202 276 210"/></g>' + _bug(60, 108))
    elif name == "prune":
        art = (G + '<circle cx="320" cy="72" r="18" stroke-opacity=".5"/>'
               '<path d="M20 270C90 226 150 186 230 150C270 132 310 122 360 120"/><path d="M150 188C160 160 176 140 196 128"/>' +
               "".join(_leaf(x, y, r, 1.05) for x, y, r in [(70, 246, -70), (110, 222, 20), (176, 176, -80), (196, 128, -40), (250, 142, 15), (300, 126, -60), (340, 121, 10)]) +
               '<path stroke-width="3" stroke-opacity=".8" d="M230 150l6-12"/>'
               '<g transform="translate(112 92) rotate(-10)"><path d="M0 0C10-10 26-18 44-18C32-8 16-2 0 0Z" ' + SOFT + '/>'
               '<path d="M0 0C12 0 28-4 40-12" stroke-opacity=".7"/>'
               '<path stroke-width="7" d="M-4 4C-18 14-28 28-32 44M2 6C-2 22-2 38 4 52"/><circle r="4.5" fill="#fffdf8"/></g></g>')
    else:  # portrait
        return ('<svg viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">' + G +
                '<path d="M80 440V214A120 120 0 0 1 320 214V440" stroke-opacity=".35" fill="currentColor" fill-opacity=".06"/>'
                '<circle cx="200" cy="214" r="50" ' + SOFT + '/><path d="M108 440C108 344 148 300 200 300S292 344 292 440" ' + SOFT + '/>'
                + _waves(456, ".35") + _leaf(316, 134, -60, 1.3) + _leaf(334, 160, -20, 1.1) + '<path d="M300 176C320 150 330 130 332 110"/></g></svg>')
    lift = {"hedge": 26, "cleanup": 24, "bed": 18, "rental": 40, "kitchen": 0, "mow": 0, "prune": 20}[name]
    if lift:
        art = f'<g transform="translate(0 -{lift})">{art}</g>'
    return f'<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{art}</svg>'


def ph(lang, scene, caption, cls=""):
    return (f'<figure class="ph {cls}">{_scene(scene)}<figcaption><span class="ph-k">{ic("camera")}'
            f'{T(lang, "Your photo here", "Tu foto aquí")}<span class="sr-only">:</span></span>'
            f'<span class="ph-d">{escape(caption)}</span></figcaption></figure>')


def reviews(lang, tags):
    items = "".join(
        f'<li class="review-ph">{ic("quote")}<span class="tag">{t}</span>'
        f'<strong>{T(lang, "Client review coming soon", "Reseña de cliente próximamente")}</strong>'
        f'<span>{T(lang, "Real reviews from our customers will appear here.", "Aquí aparecerán reseñas reales de nuestros clientes.")}</span></li>'
        for t in tags)
    return f"""  <section id="reviews" aria-labelledby="rev-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">{T(lang, "Customer reviews", "Reseñas")}</p>
        <h2 class="h2" id="rev-title">{T(lang, "What our customers say", "Lo que dicen nuestros clientes")}</h2>
      </div>
      <ul class="reviews-grid">{items}</ul>
    </div>
  </section>
"""


PESTS = [("cockroaches", "Cockroaches", "cucarachas", "Cucarachas"),
         ("ants", "Ants", "hormigas", "Hormigas"),
         ("rodents", "Rodents", "roedores", "Roedores"),
         ("termites", "Termites", "termitas", "Termitas"),
         ("mosquitoes", "Mosquitoes", "mosquitos", "Mosquitos"),
         ("bed bugs", "Bed bugs", "chinches", "Chinches")]


def pest_chips(lang):
    out = []
    for en_q, en_l, es_q, es_l in PESTS:
        msg = pest_msg(lang, T(lang, f"for {en_q}", f"por {es_q}"))
        out.append(f'<li><a href="{escape(wa(PEST, msg))}" target="_blank" rel="noopener">{T(lang, en_l, es_l)}<span class="sr-only"> (WhatsApp)</span></a></li>')
    more = T(lang, "Hi Island Pest Control, I'd like to book an inspection. The problem is: ",
             "Hola Island Pest Control, quiero agendar una inspección. El problema es: ")
    out.append(f'<li><a href="{escape(wa(PEST, more))}" target="_blank" rel="noopener">{T(lang, "And more…", "Y más…")}<span class="sr-only"> (WhatsApp)</span></a></li>')
    return f'<ul class="pest-chips">{"".join(out)}</ul>'


LAWN_SVCS = [  # icon, en name, en desc, en quote-target, es name, es desc, es quote-target
    ("mower", "Mowing", "Regular professional mowing to keep your grass healthy, clean, and looking its best.", "lawn mowing",
     "Corte de césped", "Corte profesional y regular para mantener tu césped saludable, limpio y luciendo su mejor cara.", "corte de césped"),
    ("scissors", "Trimming", "We trim grass, edges, plants, and landscape areas to create a clean and finished appearance.", "trimming",
     "Recorte y bordes", "Recortamos césped, bordes, plantas y áreas verdes para lograr un acabado limpio y prolijo.", "recorte y bordes"),
    ("rake", "Clean Up", "We remove leaves, grass clippings, branches, and yard debris to keep your property clean and presentable.", "a yard clean up",
     "Limpieza de jardín", "Retiramos hojas, recortes de césped, ramas y otros desechos para mantener tu propiedad limpia y presentable.", "limpieza de jardín"),
    ("sprout", "Landscaping", "We help maintain and improve outdoor spaces with professional landscaping and careful attention to detail.", "landscaping",
     "Jardinería y paisajismo", "Ayudamos a mantener y mejorar espacios exteriores con jardinería profesional y cuidado en cada detalle.", "jardinería y paisajismo"),
]
LAWN_ALSO = [("Landscape Design & Installation", "landscape design and installation", "Diseño e instalación de paisajismo", "diseño e instalación de paisajismo"),
             ("Irrigation Maintenance", "irrigation maintenance", "Mantenimiento de riego", "mantenimiento de riego"),
             ("And more", "another outdoor service", "Y más", "otro servicio de exteriores")]

PEST_SVCS = [  # icon, en name, en desc, en bullets, en msg tail, es name, es desc, es bullets, es msg tail
    ("bug", "Residential pest control", "General fumigation and targeted treatments for your home, inside and out.",
     ["Cockroaches, ants, spiders, flies", "Fleas and ticks", "Fogging and thermal fogging"], "for my home in Roatán",
     "Control de plagas residencial", "Fumigación general y tratamientos específicos para tu casa, por dentro y por fuera.",
     ["Cucarachas, hormigas, arañas, moscas", "Pulgas y garrapatas", "Nebulización y termonebulización"], "para mi casa en Roatán"),
    ("building", "Commercial pest control", "Scheduled service for businesses that can't afford a pest problem.",
     ["Restaurants, bars and kitchens", "Hotels and beach clubs", "Warehouses and condominiums"], "for my business in Roatán",
     "Control de plagas comercial", "Servicio programado para negocios que no pueden darse el lujo de tener plagas.",
     ["Restaurantes, bares y cocinas", "Hoteles y beach clubs", "Bodegas y condominios"], "para mi negocio en Roatán"),
    ("key", "Vacation rentals & Airbnb", "Preventive programs that keep villas and rentals guest-ready.",
     ["Monthly preventive programs", "Inspections between seasons", "Rainy-season treatments"], "for my vacation rental / Airbnb in Roatán",
     "Rentas vacacionales y Airbnb", "Programas preventivos para que villas y rentas estén listas para cada huésped.",
     ["Programas preventivos mensuales", "Inspecciones entre temporadas", "Tratamientos para la temporada de lluvia"], "para mi renta vacacional / Airbnb en Roatán"),
    ("wing", "Mosquito & rodent control", "Island life means mosquitoes and rodents. We find where they come from and deal with it.",
     ["Mosquito treatments for yards and outdoor areas", "Rodent control and prevention", "Beachfront and tropical properties"], "for mosquito / rodent control",
     "Control de mosquitos y roedores", "En la isla hay mosquitos y roedores. Encontramos de dónde vienen y los controlamos.",
     ["Tratamientos contra mosquitos en patios y áreas exteriores", "Control y prevención de roedores", "Propiedades frente al mar y jardines tropicales"], "para control de mosquitos / roedores"),
    ("leaf", "Garden care", "Led by an agricultural engineer: healthy gardens, not just tidy ones.",
     ["Maintenance and pruning", "Fertilization and weed control", "Plant health treatments"], "for garden care",
     "Cuidado de jardines", "Dirigido por un ingeniero agrónomo: jardines sanos, no solo ordenados.",
     ["Mantenimiento y poda", "Fertilización y control de malezas", "Control fitosanitario"], "para el cuidado de mi jardín"),
]


def lawn_also_line(lang):
    links = ", ".join(
        f'<a href="{escape(wa(LAWN, lawn_msg(lang, T(lang, q_en, q_es))))}" target="_blank" rel="noopener">{T(lang, n_en, n_es)}</a>'
        for n_en, q_en, n_es, q_es in LAWN_ALSO)
    return f'<p class="also"><strong>{T(lang, "We also do:", "También hacemos:")}</strong> {links}.</p>'


# ---------------------------------------------------------------- HOME
def home(lang):
    p = PATHS[("home", lang)]
    a = rel(p, "assets/")
    lawnp, pestp = rel(p, PATHS[("lawn", lang)]), rel(p, PATHS[("pest", lang)])
    title = T(lang, "DR Lawn & Landscape · Island Pest Control | Darío Reyes, Roatán",
              "DR Lawn & Landscape · Island Pest Control | Darío Reyes, Roatán")
    desc = T(lang, "Lawn and landscape maintenance plus pest control and garden care in Roatán, Bay Islands, Honduras. Led by agricultural engineer Darío Reyes (UNAG). Quotes and inspections on WhatsApp.",
             "Mantenimiento de jardines y áreas verdes, control de plagas y cuidado de jardines en Roatán, Islas de la Bahía, Honduras. Dirigido por el ingeniero agrónomo Darío Reyes (UNAG). Cotizaciones e inspecciones por WhatsApp.")
    lawn_items = "".join(
        f'<li><span class="icon-dot">{ic(i)}</span><h3>{T(lang, ne, ns)}</h3><p>{T(lang, de, ds)}</p></li>'
        for i, ne, de, qe, ns, ds, qs in LAWN_SVCS)
    pest_items = "".join(
        f'<li><span class="icon-dot">{ic(i)}</span><h3>{T(lang, ne, ns)}</h3><p>{T(lang, de, ds)}</p></li>'
        for i, ne, de, be, me, ns, ds, bs, ms in PEST_SVCS)
    how_rows = [
        (T(lang, "You write to us", "Nos escribes"),
         T(lang, f"<strong>WhatsApp {LAWN_SHOW}.</strong> Tell us about your property and the type of maintenance you need.",
           f"<strong>WhatsApp {LAWN_SHOW}.</strong> Cuéntanos sobre tu propiedad y el tipo de mantenimiento que necesitas."),
         T(lang, f"<strong>WhatsApp {PEST_SHOW}.</strong> Tell us what you're seeing and where.",
           f"<strong>WhatsApp {PEST_SHOW}.</strong> Cuéntanos qué estás viendo y dónde.")),
        (T(lang, "We take a look", "Revisamos"),
         T(lang, "We review the work at your property.", "Revisamos el trabajo en tu propiedad."),
         T(lang, "We visit, find the source and tell you what we found. <strong>We detect today.</strong>",
           "Te visitamos, encontramos el origen y te explicamos lo que hallamos. <strong>Detectamos hoy.</strong>")),
        (T(lang, "You get", "Recibes"),
         T(lang, "A clear estimate. The quote is free.", "Un presupuesto claro. La cotización es gratis."),
         T(lang, "A clear treatment plan.", "Un plan de tratamiento claro.")),
        (T(lang, "Then", "Después"),
         T(lang, "We take care of the work so you can enjoy a clean, beautiful, and well-maintained outdoor space.",
           "Nos encargamos del trabajo para que disfrutes de un espacio exterior limpio, hermoso y bien cuidado."),
         T(lang, "The treatment and follow-up visits. <strong>We solve tomorrow.</strong>",
           "El tratamiento y visitas de seguimiento. <strong>Solucionamos mañana.</strong>")),
    ]
    lab_l, lab_p = T(lang, "Lawn & Landscape", "Jardinería y paisajismo"), T(lang, "Pest Control & Garden Care", "Control de plagas y jardines")
    rows = "".join(f'<tr><th scope="row">{r}</th><td class="c-lawn" data-label="{lab_l}">{l}</td><td class="c-pest" data-label="{lab_p}">{pp}</td></tr>'
                   for r, l, pp in how_rows)
    area_msg = T(lang, "Hi Darío, do you cover my area in Roatán? I'm located in: ", "Hola Darío, ¿llegan a mi zona en Roatán? Estoy en: ")
    body = f"""<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="wrap">
      <div class="hero-top">
        <p class="kicker">{T(lang, "Roatán · Bay Islands · Honduras", "Roatán · Islas de la Bahía · Honduras")}</p>
        <h1 id="hero-title">{T(lang, "Your property, our passion, your peace of mind.", "Tu propiedad, nuestra pasión, tu tranquilidad.")}</h1>
        <p class="lead">{T(lang, "Lawn and landscape maintenance, and pest control and garden care, from one local team in Roatán, led by agricultural engineer Darío Reyes (UNAG). Pick what you need:",
                           "Mantenimiento de jardines y áreas verdes, y control de plagas y cuidado de jardines, de un mismo equipo local en Roatán, dirigido por el ingeniero agrónomo Darío Reyes (UNAG). Elige lo que necesitas:")}</p>
      </div>
      <div class="entries">
        <article class="entry">
          <div class="entry-head"><img class="lg-dr" src="{a}logo-dr-lawn.jpg" width="64" height="64" alt="DR Lawn &amp; Landscape Maintenance logo"><div><p class="entry-name">DR Lawn &amp; Landscape Maintenance</p><p class="tags">{T(lang, "Mowing • Trimming • Clean Up • Landscaping", "Corte • Recorte • Limpieza • Jardinería")}</p></div></div>
          <h2>{T(lang, "Beautiful outdoor spaces, well maintained.", "Espacios exteriores hermosos, bien cuidados.")}</h2>
          <p class="lead">{T(lang, "For homes, Airbnb & rentals and commercial properties.", "Para casas, Airbnb y alquileres, y propiedades comerciales.")}</p>
          <div class="entry-cta">{a_wa(LAWN, lawn_msg(lang), T(lang, "Free quote on WhatsApp", "Cotiza gratis por WhatsApp"))}<a class="text-link" href="{lawnp}">{T(lang, "Lawn & landscape services", "Servicios de jardinería")}{ic("arrow")}</a></div>
        </article>
        <article class="entry line-pest">
          <div class="entry-head"><img class="lg-ipc" src="{a}ipc-mark.png" width="46" height="60" alt="Island Pest Control &amp; Garden Care ladybug mark"><div><p class="entry-name">Island Pest Control &amp; Garden Care</p><p class="tags">{T(lang, "Cockroaches • Ants • Rodents • Termites • Mosquitoes", "Cucarachas • Hormigas • Roedores • Termitas • Mosquitos")}</p></div></div>
          <h2>{T(lang, "Your local pest control experts.", "Ya llegamos, venimos para cuidarte.")}</h2>
          <p class="lead">{T(lang, "Effective, safe, and long-lasting solutions for a pest-free place.", "Soluciones efectivas, seguras y duraderas para un hogar o negocio libre de plagas.")}</p>
          <div class="entry-cta">{a_wa(PEST, pest_msg(lang), T(lang, "Book your inspection", "Agenda tu inspección"), "btn btn-red")}<a class="text-link" href="{pestp}">{T(lang, "Pest control services", "Servicios de control de plagas")}{ic("arrow")}</a></div>
        </article>
      </div>
    </div>
  </section>

  <div class="facts" role="region" aria-label="{T(lang, 'Key facts', 'Datos clave')}">
    <div class="wrap">
      <dl>
        <div><dt>{T(lang, "Led by", "Dirigido por")}</dt><dd>{T(lang, "Darío Reyes, agricultural engineer (UNAG)", "Darío Reyes, ingeniero agrónomo (UNAG)")}</dd></div>
        <div><dt>{T(lang, "Where", "Dónde")}</dt><dd>{T(lang, "Roatán and surrounding areas", "Roatán y sus alrededores")}</dd></div>
        <div><dt>{T(lang, "For", "Para")}</dt><dd>{T(lang, "Homes, rentals and businesses", "Casas, alquileres y negocios")}</dd></div>
        <div><dt>{T(lang, "How to reach us", "Cómo contactarnos")}</dt><dd>{T(lang, "WhatsApp first, in English or Spanish", "Primero por WhatsApp, en español o inglés")}</dd></div>
      </dl>
    </div>
  </div>

  <section id="lawn" aria-labelledby="lawn-title">
    <div class="wrap split">
      <div class="line-intro">
        <p class="kicker">DR Lawn &amp; Landscape Maintenance</p>
        <h2 class="h2" id="lawn-title">{T(lang, "Everything your yard needs to stay well maintained.", "Todo lo que tu jardín necesita para mantenerse en su mejor estado.")}</h2>
        <span class="script">{T(lang, "Beautiful outdoors, well maintained.", "Exteriores bonitos, bien cuidados.")}</span>
        <p class="lead">{T(lang, "Whether you need regular lawn maintenance or a one-time cleanup, we keep outdoor spaces clean, attractive, and well maintained through reliable service and attention to detail.",
                           "Ya sea que necesites mantenimiento regular o una limpieza puntual, mantenemos los espacios exteriores limpios, atractivos y bien cuidados, con un servicio confiable y atención al detalle.")}</p>
        <div class="btns">{a_wa(LAWN, lawn_msg(lang), T(lang, "Get a free quote", "Cotización gratis"))}<a class="btn btn-ghost" href="{lawnp}">{T(lang, "See all lawn services", "Ver servicios de jardinería")}</a></div>
      </div>
      <div>
        <ul class="svc-list">{lawn_items}</ul>
        {lawn_also_line(lang)}
      </div>
    </div>
  </section>

  <section id="pest" class="band-paper line-pest" aria-labelledby="pest-title">
    <div class="wrap split">
      <div class="line-intro">
        <p class="kicker">Island Pest Control &amp; Garden Care</p>
        <h2 class="h2" id="pest-title">{T(lang, "Effective, safe, and long-lasting solutions for a pest-free place.", "Soluciones efectivas, seguras y duraderas para un lugar libre de plagas.")}</h2>
        <span class="script">{T(lang, "Your peace of mind is our mission.", "Tu tranquilidad es nuestra misión.")}</span>
        <p class="lead">{T(lang, "Homes, businesses and gardens across Roatán, residential and commercial. We care about what matters most with responsibility and commitment.",
                           "Casas, negocios y jardines en todo Roatán, residencial y comercial. Cuidamos lo que más te importa con responsabilidad y compromiso.")}</p>
        <div class="btns">{a_wa(PEST, pest_msg(lang), T(lang, "Book your inspection", "Agenda tu inspección"), "btn btn-red")}<a class="btn btn-ghost" href="{pestp}">{T(lang, "See all pest services", "Ver servicios de plagas")}</a></div>
      </div>
      <div>
        <p class="chips-note">{T(lang, "We inspect and control. Tap a pest to message us about it on WhatsApp.", "Inspeccionamos y controlamos. Toca una plaga para escribirnos por WhatsApp.")}</p>
        {pest_chips(lang)}
        <ul class="svc-list">{pest_items}</ul>
      </div>
    </div>
  </section>

  <section class="how" id="how" aria-labelledby="how-title">
    <div class="wrap">
      <p class="kicker">{T(lang, "How we work", "Cómo trabajamos")}</p>
      <h2 class="h2" id="how-title">{T(lang, "Same team, same way of working. No surprises.", "Mismo equipo, misma forma de trabajar. Sin sorpresas.")}</h2>
      <p class="lead" style="margin-top:14px">{T(lang, "Both service lines work the same way: you send a WhatsApp, we look at your property, and you get a clear answer before any work starts. The only difference is the number you write to.",
                                                 "Las dos líneas trabajan igual: nos escribes por WhatsApp, revisamos tu propiedad y recibes una respuesta clara antes de empezar cualquier trabajo. Solo cambia el número al que escribes.")}</p>
      <table class="how-table">
        <caption class="sr-only">{T(lang, "How each service line works", "Cómo funciona cada línea de servicio")}</caption>
        <colgroup><col class="col-h"><col><col></colgroup>
        <thead><tr><td></td><th scope="col" class="c-lawn">{lab_l}</th><th scope="col" class="c-pest">{lab_p}</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <div class="btns">{a_wa(LAWN, lawn_msg(lang), T(lang, "Lawn quote", "Cotizar jardinería"))}{a_wa(PEST, pest_msg(lang), T(lang, "Pest inspection", "Inspección de plagas"), "btn btn-red")}</div>
    </div>
  </section>

  <section id="area" aria-labelledby="area-title">
    <div class="wrap">
      <div class="area-card">
        <div>
          <h2 class="h2" id="area-title">{T(lang, "Proudly serving Roatán and surrounding areas.", "Sirviendo con orgullo a Roatán y sus alrededores.")}</h2>
          <p>{T(lang, "Homes, villas, vacation rentals, restaurants, hotels and businesses on Roatán, Bay Islands, Honduras. Lawn and landscape maintenance and pest control from the same local team.",
                "Casas, villas, rentas vacacionales, restaurantes, hoteles y negocios en Roatán, Islas de la Bahía, Honduras. Mantenimiento de jardines y control de plagas del mismo equipo local.")}</p>
          <span class="place">{ic("pin")}{T(lang, "Roatán, Bay Islands, Honduras", "Roatán, Islas de la Bahía, Honduras")}</span>
        </div>
        <div class="area-actions">
          <p style="margin:0">{T(lang, "Not sure we reach your area? Message us and ask.", "¿No sabes si llegamos a tu zona? Escríbenos y pregunta.")}</p>
          {a_wa(LAWN, area_msg, T(lang, "Ask about your area", "Pregunta por tu zona"), "btn btn-light")}
        </div>
      </div>
    </div>
  </section>

  <section id="about" class="band-paper" aria-labelledby="about-title">
    <div class="wrap about-grid">
      {ph(lang, "portrait", T(lang, "Portrait of Darío Reyes", "Retrato de Darío Reyes"), "portrait")}
      <div>
        <p class="kicker">{T(lang, "About", "Nosotros")}</p>
        <h2 class="h2" id="about-title">{T(lang, "Meet Darío Reyes", "Conoce a Darío Reyes")}</h2>
        <p class="role">{T(lang, "Founder · Agricultural engineer (UNAG)", "Fundador · Ingeniero agrónomo (UNAG)")}</p>
        <div class="about-body">
          <p>{T(lang, "DR Lawn &amp; Landscape Maintenance and Island Pest Control &amp; Garden Care are both led by Darío Reyes, an agricultural engineer trained at UNAG, Honduras' National University of Agriculture.",
                "DR Lawn &amp; Landscape Maintenance e Island Pest Control &amp; Garden Care están dirigidos por Darío Reyes, ingeniero agrónomo egresado de la UNAG, la Universidad Nacional de Agricultura de Honduras.")}</p>
          <p>{T(lang, "That background is the difference: lawn care, garden care and integrated pest management built on knowing how insects, plants and soil work. The goal is safe, efficient methods and long-lasting results, for your home, your business and your garden.",
                "Esa formación marca la diferencia: cuidado de jardines y manejo integral de plagas basados en entender cómo funcionan los insectos, las plantas y el suelo. El objetivo: métodos seguros y eficientes con resultados duraderos, para tu casa, tu negocio y tu jardín.")}</p>
          <p><strong>{T(lang, "We treat your property like our own.", "Cuidamos tu propiedad como si fuera nuestra.")}</strong></p>
        </div>
      </div>
    </div>
  </section>

{reviews(lang, [T(lang, "Lawn & Landscape", "Jardinería"), T(lang, "Pest Control", "Control de plagas"), T(lang, "Garden Care", "Cuidado de jardines")])}
  <section id="contact" class="band-paper" aria-labelledby="contact-title">
    <div class="wrap contact-grid">
      <div>
        <p class="kicker">{T(lang, "Contact", "Contacto")}</p>
        <h2 class="h2" id="contact-title">{T(lang, "Ready for a better-looking yard, or a pest-free place?", "¿Listo para un jardín que luzca mejor, o un lugar libre de plagas?")}</h2>
        <p class="lead" style="margin-top:14px">{T(lang, "The fastest way to reach us is WhatsApp. Write to the line you need, or use the form and it goes to the right number.",
                                                   "La forma más rápida de contactarnos es WhatsApp. Escribe a la línea que necesitas, o usa el formulario y llegará al número correcto.")}</p>
        <div class="lines">
          <div class="line-card">
            <span class="lc-name">{T(lang, "Lawn & Landscape · DR", "Jardinería y paisajismo · DR")}</span>
            <a class="lc-num" href="tel:{LAWN_TEL}">{LAWN_SHOW}</a>
            <div class="lc-btns">{a_wa(LAWN, lawn_msg(lang), "WhatsApp", "btn btn-wa btn-sm")}{a_tel(LAWN_TEL, LAWN_SHOW, T(lang, "Call", "Llamar"), "btn btn-ghost btn-sm")}</div>
          </div>
          <div class="line-card line-pest">
            <span class="lc-name">{T(lang, "Pest Control & Garden Care · Island", "Control de plagas y jardines · Island")}</span>
            <a class="lc-num" href="tel:{PEST_TEL}">{PEST_SHOW}</a>
            <div class="lc-btns">{a_wa(PEST, pest_msg(lang), "WhatsApp", "btn btn-red btn-sm")}{a_tel(PEST_TEL, PEST_SHOW, T(lang, "Call", "Llamar"), "btn btn-ghost btn-sm")}</div>
          </div>
        </div>
        <p class="contact-meta">{ic("pin")}{T(lang, "Roatán, Bay Islands, Honduras", "Roatán, Islas de la Bahía, Honduras")}</p>
      </div>
      <form class="quote-form" action="https://wa.me/{LAWN}" method="get" target="_blank" data-lang="{lang}" data-lawn="{LAWN}" data-pest="{PEST}">
        <h3>{T(lang, "Send us a message", "Envíanos un mensaje")}</h3>
        <p class="hint">{T(lang, "We'll answer on WhatsApp.", "Te respondemos por WhatsApp.")}</p>
        <div class="field-row">
          <div class="field"><label for="f-name">{T(lang, "Your name", "Tu nombre")}</label><input id="f-name" type="text" autocomplete="name"></div>
          <div class="field"><label for="f-line">{T(lang, "Service", "Servicio")}</label>
            <select id="f-line">
              <option value="lawn">{lab_l}</option>
              <option value="pest">{lab_p}</option>
              <option value="both">{T(lang, "Both", "Ambos")}</option>
            </select></div>
        </div>
        <div class="field"><label for="f-area">{T(lang, "Area in Roatán", "Zona en Roatán")}</label><input id="f-area" type="text" placeholder="{T(lang, 'e.g. West Bay, French Harbour', 'ej. West Bay, French Harbour')}"></div>
        <div class="field"><label for="f-msg">{T(lang, "What do you need?", "¿Qué necesitas?")}</label><textarea id="f-msg" name="text" required></textarea></div>
        <button class="btn btn-wa" type="submit">{ic("wa", True)}{T(lang, "Send on WhatsApp", "Enviar por WhatsApp")}</button>
        <p class="form-note">{T(lang, "Opens WhatsApp with your message ready to send. Nothing is stored on this site.", "Abre WhatsApp con tu mensaje listo para enviar. Este sitio no guarda ningún dato.")} <a href="{rel(p, PATHS[("privacy", lang)])}">{T(lang, "Privacy policy", "Política de privacidad")}</a></p>
      </form>
    </div>
  </section>
</main>
"""
    return head("home", lang, title, desc) + header("home", lang) + body + footer("home", lang)


# ---------------------------------------------------------------- LAWN PAGE
def lawn_page(lang):
    p = PATHS[("lawn", lang)]
    a = rel(p, "assets/")
    home_ = rel(p, PATHS[("home", lang)])
    pestp = rel(p, PATHS[("pest", lang)])
    title = T(lang, "Lawn & Landscape Maintenance in Roatán | DR Lawn & Landscape", "Jardinería y paisajismo en Roatán | DR Lawn & Landscape")
    desc = T(lang, "Professional lawn and landscape maintenance in Roatán, Bay Islands, Honduras. Mowing, trimming, clean up and landscaping for homes, Airbnb rentals and commercial properties. Free quote on WhatsApp.",
             "Mantenimiento profesional de jardines y áreas verdes en Roatán, Islas de la Bahía, Honduras. Corte de césped, recorte, limpieza y paisajismo para casas, alquileres Airbnb y comercios. Cotización gratis por WhatsApp.")
    cards = "".join(
        f'<article class="card"><div class="card-icon">{ic(i)}</div><h3>{T(lang, ne, ns)}</h3><p class="grow">{T(lang, de, ds)}</p>'
        f'{a_wa(LAWN, lawn_msg(lang, T(lang, qe, qs)), T(lang, "Get a quote", "Cotizar"), "text-link", ": " + T(lang, ne, ns) + " (WhatsApp)")}</article>'
        for i, ne, de, qe, ns, ds, qs in LAWN_SVCS)
    segs = [("home", T(lang, "Residential", "Residencial"), T(lang, "Beautiful lawns and landscapes you'll love coming home to.", "Jardines y áreas verdes hermosos que te encantará ver al llegar a casa.")),
            ("key", T(lang, "Airbnb & Rentals", "Airbnb y alquileres"), T(lang, "Impress your guests with flawless outdoor spaces.", "Impresiona a tus huéspedes con exteriores impecables.")),
            ("building", T(lang, "Commercial", "Comercial"), T(lang, "Well-maintained properties create a lasting impression.", "Una propiedad bien cuidada deja una impresión duradera."))]
    seg_html = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for _, t, d in segs)
    chips = "".join(f'<span class="chip">{ic(i)}{t}</span>' for i, t, _ in segs)
    why = [(T(lang, "Reliable & Trusted", "Confiables"), T(lang, "We treat your property like our own.", "Cuidamos tu propiedad como si fuera nuestra.")),
           (T(lang, "Local Experts", "Expertos locales"), T(lang, "Proudly serving Roatán and surrounding areas.", "Sirviendo con orgullo a Roatán y sus alrededores.")),
           (T(lang, "Quality Service", "Servicio de calidad"), T(lang, "Attention to detail and commitment to excellence.", "Atención al detalle y compromiso con la excelencia.")),
           (T(lang, "On Time, Every Time", "Puntuales, siempre"), T(lang, "Count on us to be there when you need us.", "Cuenta con nosotros cuando nos necesites."))]
    why_html = "".join(f"<li><h3>{h}</h3><p>{d}</p></li>" for h, d in why)
    steps = [(T(lang, "Tell us what you need", "Cuéntanos qué necesitas"), T(lang, "Contact us and tell us about your property and the type of maintenance you need.", "Contáctanos y cuéntanos sobre tu propiedad y el tipo de mantenimiento que necesitas.")),
             (T(lang, "Get your free quote", "Recibe tu cotización gratis"), T(lang, "We'll review the work and provide you with a clear estimate.", "Revisamos el trabajo y te damos un presupuesto claro.")),
             (T(lang, "Enjoy your yard", "Disfruta tu jardín"), T(lang, "We take care of the work so you can enjoy a clean, beautiful, and well-maintained outdoor space.", "Nosotros nos encargamos del trabajo para que disfrutes de un espacio exterior limpio, hermoso y bien cuidado."))]
    steps_html = "".join(f"<div><dt>{h}</dt><dd>{d}</dd></div>" for h, d in steps)
    body = f"""<main id="main">
  <div class="wrap crumbs"><a href="{home_}">{T(lang, "Home", "Inicio")}</a> / {T(lang, "Lawn &amp; Landscape", "Jardinería y paisajismo")}</div>
  <section class="page-hero" aria-labelledby="hero-title">
    <div class="wrap page-hero-grid">
      <div>
        <p class="kicker">{T(lang, "Mowing • Trimming • Clean Up • Landscaping", "Corte • Recorte • Limpieza • Jardinería")}</p>
        <h1 id="hero-title">{T(lang, "Beautiful outdoor spaces, well maintained.", "Espacios exteriores hermosos, bien cuidados.")}</h1>
        <span class="script">{T(lang, "Your property, our passion, your peace of mind.", "Tu propiedad, nuestra pasión, tu tranquilidad.")}</span>
        <p class="lead">{T(lang, "Professional lawn and landscape maintenance in Roatán, Bay Islands.", "Mantenimiento profesional de jardines y áreas verdes en Roatán, Islas de la Bahía.")}</p>
        <div class="btns">{a_wa(LAWN, lawn_msg(lang), T(lang, "Get a free quote on WhatsApp", "Cotiza gratis por WhatsApp"))}{a_tel(LAWN_TEL, LAWN_SHOW)}</div>
        <div class="seg-line">{chips}</div>
      </div>
      <div class="hero-logo"><img src="{a}logo-dr-lawn.jpg" width="480" height="480" alt="DR Lawn &amp; Landscape Maintenance logo: Mowing, Trimming, Clean Up, Landscaping. Beautiful Outdoors, Well Maintained." fetchpriority="high"></div>
    </div>
  </section>

  <section class="band-paper" aria-labelledby="about-title">
    <div class="wrap split">
      <div>
        <p class="kicker">{T(lang, "About us", "Sobre nosotros")}</p>
        <h2 class="h2" id="about-title">{T(lang, "Keeping Roatán's outdoor spaces looking their best.", "Manteniendo los exteriores de Roatán en su mejor estado.")}</h2>
      </div>
      <div class="about-body">
        <p>{T(lang, "At DR Lawn &amp; Landscape Maintenance, we provide professional lawn and landscape maintenance in Roatán, Bay Islands.", "En DR Lawn &amp; Landscape Maintenance, ofrecemos mantenimiento profesional de jardines y áreas verdes en Roatán, Islas de la Bahía.")}</p>
        <p>{T(lang, "We take pride in keeping outdoor spaces clean, attractive, and well maintained through reliable service and attention to detail.", "Nos enorgullece mantener los espacios exteriores limpios, atractivos y bien cuidados, con un servicio confiable y atención al detalle.")}</p>
        <p>{T(lang, "Whether you need regular lawn maintenance or a one-time cleanup, our goal is simple: beautiful outdoors, well maintained.", "Ya sea que necesites mantenimiento regular o una limpieza puntual, nuestra meta es simple: exteriores bonitos, bien cuidados.")}</p>
      </div>
    </div>
  </section>

  <section id="services" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">{T(lang, "What we take care of", "De qué nos encargamos")}</p>
        <h2 class="h2" id="svc-title">{T(lang, "Everything your yard needs to stay well maintained.", "Todo lo que tu jardín necesita para mantenerse en su mejor estado.")}</h2>
      </div>
      <div class="cards cards-4">{cards}</div>
      {lawn_also_line(lang)}
    </div>
  </section>

  <section class="band-paper" aria-labelledby="seg-title">
    <div class="wrap split">
      <div>
        <p class="kicker">{T(lang, "Who we serve", "Con quiénes trabajamos")}</p>
        <h2 class="h2" id="seg-title">{T(lang, "Homes, rentals and businesses across the island.", "Casas, alquileres y negocios en toda la isla.")}</h2>
        <p class="lead" style="margin-top:14px">{T(lang, "From residential properties to vacation homes and commercial spaces, we're here to help keep your outdoor areas looking their best.", "Desde propiedades residenciales hasta casas de vacaciones y espacios comerciales, estamos aquí para ayudarte a mantener tus áreas exteriores luciendo su mejor cara.")}</p>
      </div>
      <ul class="why-list" style="grid-template-columns:1fr">{seg_html}</ul>
    </div>
  </section>

  <section id="work" aria-labelledby="work-title">
    <div class="wrap">
      <div class="split section-head" style="max-width:none">
        <div>
          <p class="kicker">{T(lang, "Our work", "Nuestro trabajo")}</p>
          <h2 class="h2" id="work-title">{T(lang, "Clean work. Beautiful results.", "Trabajo limpio. Resultados hermosos.")}</h2>
        </div>
        <div class="lead"><p>{T(lang, "Every property is different, and we approach each project with the same commitment to quality.", "Cada propiedad es distinta, y abordamos cada proyecto con el mismo compromiso con la calidad.")}</p><p>{T(lang, "From routine lawn maintenance to detailed yard cleanups, we work to leave every outdoor space looking fresh, clean, and well cared for.", "Desde el mantenimiento regular hasta limpiezas detalladas, trabajamos para dejar cada espacio exterior fresco, limpio y bien cuidado.")}</p></div>
      </div>
      <div class="gallery">{ph(lang, "mow", T(lang, "Freshly mowed lawn in Roatán", "Césped recién cortado en Roatán"))}{ph(lang, "hedge", T(lang, "Trimmed hedges and clean edges", "Setos y bordes recortados"), "alt")}{ph(lang, "cleanup", T(lang, "Yard clean up, before and after", "Limpieza de jardín, antes y después"), "alt")}{ph(lang, "bed", T(lang, "Landscaped garden bed", "Jardín paisajístico"))}</div>
    </div>
  </section>

  <section class="band-paper" aria-labelledby="why-title">
    <div class="wrap split">
      <div>
        <p class="kicker">{T(lang, "Why DR", "Por qué DR")}</p>
        <h2 class="h2" id="why-title">{T(lang, "Reliable care for your outdoor space.", "Cuidado confiable para tu espacio exterior.")}</h2>
        <p class="lead" style="margin-top:14px"><strong>{T(lang, "A well-maintained property makes a difference.", "Una propiedad bien cuidada marca la diferencia.")}</strong> {T(lang, "We focus on dependable service, quality work, and attention to detail.", "Nos enfocamos en un servicio confiable, trabajo de calidad y atención al detalle.")}</p>
      </div>
      <ul class="why-list">{why_html}</ul>
    </div>
  </section>

  <section id="how" aria-labelledby="how-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">{T(lang, "How it works", "Cómo funciona")}</p>
        <h2 class="h2" id="how-title">{T(lang, "Simple, and no surprises.", "Simple y sin sorpresas.")}</h2>
      </div>
      <dl class="prose-steps">{steps_html}</dl>
    </div>
  </section>

{reviews(lang, [T(lang, "Lawn & Landscape", "Jardinería")] * 3)}
  <section class="cross line-pest" aria-labelledby="cross-title">
    <div class="wrap cross-inner">
      <div>
        <p class="kicker">{T(lang, "Also from Darío Reyes", "También de Darío Reyes")}</p>
        <h2 id="cross-title">{T(lang, "Island Pest Control &amp; Garden Care", "Island Pest Control &amp; Garden Care")}</h2>
        <p class="lead" style="margin-top:8px">{T(lang, "Pest control for homes, rentals and businesses, plus garden care. Same owner, same standard.", "Control de plagas para casas, rentas y negocios, y cuidado de jardines. Mismo dueño, mismo estándar.")}</p>
      </div>
      <a class="btn btn-ghost" href="{pestp}">{T(lang, "Pest control services", "Servicios de control de plagas")}{ic("arrow")}</a>
    </div>
  </section>

  <section class="cta-band" id="contact" aria-labelledby="contact-title">
    <div class="wrap">
      <h2 class="h2" id="contact-title">{T(lang, "Ready for a better-looking yard?", "¿Listo para un jardín que luzca mejor?")}</h2>
      <p class="lead">{T(lang, "Let DR Lawn &amp; Landscape Maintenance take care of your outdoor space. Contact us today for a free quote and let us know how we can help.", "Deja que DR Lawn &amp; Landscape Maintenance cuide tu espacio exterior. Contáctanos hoy para una cotización gratis y cuéntanos cómo podemos ayudarte.")}</p>
      <div class="btns">{a_wa(LAWN, lawn_msg(lang), T(lang, "Book your service today", "Reserva tu servicio hoy"))}{a_tel(LAWN_TEL, LAWN_SHOW, T(lang, "Call ", "Llamar ") + LAWN_SHOW)}</div>
    </div>
  </section>
</main>
"""
    return head("lawn", lang, title, desc) + header("lawn", lang) + body + footer("lawn", lang)


# ---------------------------------------------------------------- PEST PAGE
def pest_page(lang):
    p = PATHS[("pest", lang)]
    a = rel(p, "assets/")
    home_ = rel(p, PATHS[("home", lang)])
    lawnp = rel(p, PATHS[("lawn", lang)])
    title = T(lang, "Pest Control & Garden Care in Roatán | Island Pest Control", "Control de plagas y jardines en Roatán | Island Pest Control")
    desc = T(lang, "Your local pest control experts in Roatán, Bay Islands: cockroaches, ants, rodents, termites, mosquitoes, bed bugs and more. Residential, commercial and vacation rentals. Book your inspection on WhatsApp.",
             "Control de plagas en Roatán, Islas de la Bahía: cucarachas, hormigas, roedores, termitas, mosquitos, chinches y más. Residencial, comercial y rentas vacacionales. Agenda tu inspección por WhatsApp.")
    cards = "".join(
        f'<article class="card"><div class="card-icon">{ic(i)}</div><h3>{T(lang, ne, ns)}</h3><p>{T(lang, de, ds)}</p>'
        f'<ul>{"".join(f"<li>{x}</li>" for x in T(lang, be, bs))}</ul>'
        f'{a_wa(PEST, pest_msg(lang, T(lang, me, ms)), T(lang, "Book this inspection", "Agendar esta inspección"), "text-link", ": " + T(lang, ne, ns) + " (WhatsApp)")}</article>'
        for i, ne, de, be, me, ns, ds, bs, ms in PEST_SVCS)
    steps = [(T(lang, "Message us", "Escríbenos"), T(lang, "Send us a WhatsApp or call. Tell us what you're seeing and where.", "Mándanos un WhatsApp o llámanos. Cuéntanos qué estás viendo y dónde.")),
             (T(lang, "Inspection &amp; diagnosis", "Inspección y diagnóstico"), T(lang, "We visit, find the source and tell you what we found. We detect today.", "Te visitamos, encontramos el origen y te explicamos lo que hallamos. Detectamos hoy.")),
             (T(lang, "Treatment plan &amp; follow-up", "Plan de tratamiento y seguimiento"), T(lang, "You get a clear plan, the treatment and follow-up visits. We solve tomorrow.", "Recibes un plan claro, el tratamiento y visitas de seguimiento. Solucionamos mañana."))]
    steps_html = "".join(f"<div><dt>{h}</dt><dd>{d}</dd></div>" for h, d in steps)
    why = [(T(lang, "We protect your family", "Protegemos tu familia"), T(lang, "Safer, healthier environments.", "Ambientes más seguros y saludables.")),
           (T(lang, "Residential &amp; commercial", "Atención residencial y comercial"), T(lang, "Located in Roatán.", "Ubicados en Roatán.")),
           (T(lang, "Professional services", "Servicio profesional"), T(lang, "Trained technicians you can trust.", "Técnicos capacitados y de confianza.")),
           (T(lang, "Fast inspections", "Inspección rápida"), T(lang, "We detect today, we solve tomorrow.", "Detectamos hoy, solucionamos mañana."))]
    why_html = "".join(f"<li><h3>{h}</h3><p>{d}</p></li>" for h, d in why)
    area_msg = T(lang, "Hi Island Pest Control, do you cover my area in Roatán? I'm located in: ", "Hola Island Pest Control, ¿llegan a mi zona en Roatán? Estoy en: ")
    body = f"""<main id="main" class="line-pest">
  <div class="wrap crumbs"><a href="{home_}">{T(lang, "Home", "Inicio")}</a> / {T(lang, "Pest Control &amp; Garden Care", "Control de plagas y jardines")}</div>
  <section class="page-hero" aria-labelledby="hero-title">
    <div class="wrap page-hero-grid">
      <div>
        <p class="kicker">{T(lang, "Island Pest Control &amp; Garden Care", "Island Pest Control &amp; Garden Care")}</p>
        <h1 id="hero-title">{T(lang, "Your local pest control experts in Roatán, Bay Islands.", "Ya llegamos, venimos para cuidarte.")}</h1>
        <p class="lead">{T(lang, "<strong>Effective, safe, and long-lasting</strong> solutions for a pest-free place. <strong>We care about what matters most</strong> with responsibility and commitment.",
                           "<strong>Soluciones efectivas, seguras y duraderas</strong> para un hogar o negocio libre de plagas. <strong>Cuidamos lo que más te importa</strong> con responsabilidad y compromiso. Control de plagas y jardines en Roatán.")}</p>
        <div class="btns">{a_wa(PEST, pest_msg(lang), T(lang, "Book your inspection", "Agenda tu inspección"), "btn btn-red")}{a_tel(PEST_TEL, PEST_SHOW)}</div>
        <p class="badge-note">{ic("leaf")}{T(lang, "Effective solutions · Environmentally friendly", "Soluciones efectivas · Amigables con el medio ambiente")}</p>
      </div>
      <div class="hero-mascot"><img src="{a}ipc-mascot.webp" width="448" height="700" alt="{T(lang, 'IPC mascot: a ladybug technician in a black cap carrying an IPC sprayer and toolbox at the front door of a Roatán home', 'Mascota de IPC: una mariquita técnica con gorra negra, fumigadora IPC y caja de herramientas frente a la puerta de una casa en Roatán')}" fetchpriority="high"></div>
    </div>
  </section>

  <section class="band-paper" aria-labelledby="pests-title">
    <div class="wrap">
      <div class="section-head">
        <h2 class="h2" id="pests-title">{T(lang, "We inspect and control", "Inspeccionamos y controlamos")}</h2>
        <p class="lead">{T(lang, "Tap a pest to message us about it on WhatsApp.", "Toca una plaga para escribirnos por WhatsApp.")}</p>
      </div>
      {pest_chips(lang)}
    </div>
  </section>

  <section id="services" aria-labelledby="svc-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">{T(lang, "Our services", "Nuestros servicios")}</p>
        <h2 class="h2" id="svc-title">{T(lang, "Homes, businesses and gardens across Roatán.", "Casas, negocios y jardines en todo Roatán.")}</h2>
        <p class="lead">{T(lang, "Residential and commercial.", "Residencial y comercial.")}</p>
      </div>
      <div class="cards cards-5">{cards}</div>
    </div>
  </section>

  <section class="band-paper" id="work" aria-labelledby="work-title">
    <div class="wrap">
      <div class="section-head"><p class="kicker">{T(lang, "Our work", "Nuestro trabajo")}</p><h2 class="h2" id="work-title">{T(lang, "On the job in Roatán", "Trabajando en Roatán")}</h2></div>
      <div class="gallery g3">{ph(lang, "kitchen", T(lang, "Inspection in a restaurant kitchen", "Inspección en la cocina de un restaurante"), "pest")}{ph(lang, "rental", T(lang, "Preventive treatment at a vacation rental", "Tratamiento preventivo en una renta vacacional"), "pest")}{ph(lang, "prune", T(lang, "Garden maintenance and pruning", "Mantenimiento y poda de jardín"), "alt")}</div>
    </div>
  </section>

  <section id="how" aria-labelledby="how-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">{T(lang, "How it works", "Cómo funciona")}</p>
        <h2 class="h2" id="how-title">{T(lang, "How an inspection works", "Cómo funciona la inspección")}</h2>
      </div>
      <dl class="prose-steps">{steps_html}</dl>
    </div>
  </section>

  <section class="band-paper" aria-labelledby="why-title">
    <div class="wrap split">
      <div>
        <p class="kicker">{T(lang, "Why us", "Por qué nosotros")}</p>
        <h2 class="h2" id="why-title">{T(lang, "Why Island Pest Control", "Por qué Island Pest Control")}</h2>
        <p class="lead" style="margin-top:14px">{T(lang, "Led by Darío Reyes, agricultural engineer (UNAG): integrated pest management built on knowing how insects, plants and soil work.", "Dirigido por Darío Reyes, ingeniero agrónomo (UNAG): manejo integral de plagas basado en entender cómo funcionan los insectos, las plantas y el suelo.")} <a href="{home_}#about">{T(lang, "Meet Darío", "Conoce a Darío")}</a></p>
      </div>
      <ul class="why-list">{why_html}</ul>
    </div>
  </section>

  <section aria-labelledby="area-title">
    <div class="wrap">
      <div class="area-card">
        <div>
          <h2 class="h2" id="area-title">{T(lang, "Serving Roatán", "Atendemos Roatán")}</h2>
          <p>{T(lang, "Homes, villas, vacation rentals, restaurants, hotels and businesses on Roatán, Bay Islands, Honduras.", "Casas, villas, rentas vacacionales, restaurantes, hoteles y negocios en Roatán, Islas de la Bahía, Honduras.")}</p>
          <p>{T(lang, "Not sure we reach your area? Message us and ask.", "¿No sabes si llegamos a tu zona? Escríbenos y pregunta.")}</p>
        </div>
        <div class="area-actions">{a_wa(PEST, area_msg, T(lang, "Ask about your area", "Pregunta por tu zona"), "btn btn-light")}</div>
      </div>
    </div>
  </section>

{reviews(lang, [T(lang, "Pest Control", "Control de plagas")] * 2 + [T(lang, "Garden Care", "Cuidado de jardines")])}
  <section class="cross" aria-labelledby="cross-title" style="--accent:var(--green);--accent-deep:var(--green-deep)">
    <div class="wrap cross-inner">
      <div>
        <p class="kicker" style="color:var(--terra)">{T(lang, "Also from Darío Reyes", "También de Darío Reyes")}</p>
        <h2 id="cross-title">DR Lawn &amp; Landscape Maintenance</h2>
        <p class="lead" style="margin-top:8px">{T(lang, "Mowing, trimming, clean up and landscaping for homes, rentals and businesses. Same owner, same standard.", "Corte de césped, recorte, limpieza y paisajismo para casas, alquileres y negocios. Mismo dueño, mismo estándar.")}</p>
      </div>
      <a class="btn btn-ghost" href="{lawnp}">{T(lang, "Lawn &amp; landscape services", "Servicios de jardinería")}{ic("arrow")}</a>
    </div>
  </section>

  <section class="cta-band" id="contact" aria-labelledby="contact-title">
    <div class="wrap">
      <h2 class="h2" id="contact-title">{T(lang, "Book your inspection", "Agenda tu inspección")}</h2>
      <p class="lead">{T(lang, "The fastest way to reach us is WhatsApp. Tell us what you're seeing and where, and we'll set up your inspection.", "La forma más rápida de contactarnos es WhatsApp. Cuéntanos qué estás viendo y dónde, y coordinamos tu inspección.")}</p>
      <div class="btns">{a_wa(PEST, pest_msg(lang), T(lang, "Message us on WhatsApp", "Escríbenos por WhatsApp"), "btn btn-red")}{a_tel(PEST_TEL, PEST_SHOW, T(lang, "Call ", "Llamar ") + PEST_SHOW)}</div>
    </div>
  </section>
</main>
"""
    return head("pest", lang, title, desc) + header("pest", lang) + body + footer("pest", lang)


# ---------------------------------------------------------------- LEGAL PAGES (privacy, terms, legal notice)
# Plain-language, GDPR-style. Rules marked "needs Darío's confirmation" in MERGED-SITE-NOTES.md were assumed.
WA_PRIVACY = "https://www.whatsapp.com/legal/privacy-policy"
VERCEL_PRIVACY = "https://vercel.com/legal/privacy-policy"


def ext(url, label):
    return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'


LAWN_WA = f'<a href="https://wa.me/{LAWN}" target="_blank" rel="noopener">WhatsApp {LAWN_SHOW}</a>'
PEST_WA = f'<a href="https://wa.me/{PEST}" target="_blank" rel="noopener">WhatsApp {PEST_SHOW}</a>'

LEGAL = {
    "privacy": {
        "en": {
            "short": "Privacy", "kicker": "Privacy",
            "title": "Privacy Policy | DR Lawn & Landscape · Island Pest Control",
            "desc": "How DR Lawn & Landscape and Island Pest Control in Roatán handle your information: WhatsApp only, nothing stored on this website, no cookies and only cookieless visit counts.",
            "h1": "Privacy policy",
            "intro": "This website belongs to two service lines run by the same person. This page explains, in plain language, what information we receive, why we use it and what you can ask us to do with it.",
            "sections": [
                ("Who is responsible", [f"Darío Reyes, owner of DR Lawn &amp; Landscape Maintenance and Island Pest Control &amp; Garden Care, in Roatán, Bay Islands, Honduras. He is responsible for the information you send us. For any privacy question, write to {LAWN_WA}."]),
                ("What we collect", ["Only what you choose to send us when you write on WhatsApp or use the contact form: your name, your phone number (WhatsApp shows it to us), where your property is, the service you need, and anything else you include in your message, such as photos of the problem."]),
                ("How the contact form works", ["The form does not send anything to us or to this website. When you press “Send on WhatsApp”, your browser opens WhatsApp with your message already written, and you decide whether to send it. Nothing you type in the form is saved or stored on this website."]),
                ("WhatsApp", [f"Our conversations happen on WhatsApp, a service run by Meta. WhatsApp handles your messages under its own rules: {ext(WA_PRIVACY, 'WhatsApp Privacy Policy')}."]),
                ("Why we use your information", ["To answer your questions, prepare quotes, schedule visits, do the work and follow up afterwards. We do not sell or rent your information, and we do not use it for advertising."]),
                ("How long we keep it", ["We keep your messages and job details while we work together and for up to two years after your last service, so we can handle follow-up visits and keep our own records. If you ask, we delete them sooner, unless the law requires us to keep something, such as a record of a payment."]),
                ("Your rights", [f"You can ask us to show you the information we have about you, to correct it, or to delete it. Write to {LAWN_WA} and we will answer within 30 days. You can also delete our chat from your own WhatsApp at any time."]),
                ("No cookies, and cookieless visit counts", ["This website sets no cookies and uses no advertising tags. To learn how many people visit, it uses Cloudflare Web Analytics, a cookieless tool that sets no identifiers, does not track individual visitors and only gives aggregate counts (page views, country and device type). It sets no cookies. Apart from that script, which loads from Cloudflare, the site loads nothing from third parties: fonts and images are served from this website itself, so your visit is not shared with Google, Facebook or anyone else. We checked this on the date shown at the top of this page."]),
                ("Hosting", [f"The website is hosted by Vercel. Like any web host, Vercel's servers process technical data such as your IP address to deliver the pages and keep them secure. We do not use that data to identify visitors. See the {ext(VERCEL_PRIVACY, 'Vercel Privacy Policy')}."]),
                ("Photos of properties", ["We only publish photos of a customer's property, on this website or anywhere else, with that customer's permission."]),
                ("Changes", ["If we change this policy, we update this page and the date at the top."]),
            ],
        },
        "es": {
            "short": "Privacidad", "kicker": "Privacidad",
            "title": "Política de privacidad | DR Lawn & Landscape · Island Pest Control",
            "desc": "Cómo DR Lawn & Landscape e Island Pest Control en Roatán tratan tus datos: solo por WhatsApp, este sitio no guarda nada, sin cookies y solo conteo de visitas sin cookies.",
            "h1": "Política de privacidad",
            "intro": "Este sitio pertenece a dos líneas de servicio dirigidas por la misma persona. Aquí te explicamos, en palabras sencillas, qué datos recibimos, para qué los usamos y qué puedes pedirnos que hagamos con ellos.",
            "sections": [
                ("Quién es el responsable", [f"Darío Reyes, dueño de DR Lawn &amp; Landscape Maintenance e Island Pest Control &amp; Garden Care, en Roatán, Islas de la Bahía, Honduras. Él es el responsable de los datos que nos envías. Para cualquier consulta sobre privacidad, escribe al {LAWN_WA}."]),
                ("Qué datos recibimos", ["Solo lo que tú decides enviarnos cuando nos escribes por WhatsApp o usas el formulario de contacto: tu nombre, tu número de teléfono (WhatsApp nos lo muestra), la ubicación de tu propiedad, el servicio que necesitas y cualquier otra cosa que incluyas en tu mensaje, como fotos del problema."]),
                ("Cómo funciona el formulario", ["El formulario no nos envía nada ni a nosotros ni a este sitio. Cuando tocas “Enviar por WhatsApp”, tu navegador abre WhatsApp con tu mensaje ya escrito y tú decides si lo envías. Nada de lo que escribes en el formulario se guarda en este sitio."]),
                ("WhatsApp", [f"Nuestras conversaciones ocurren en WhatsApp, un servicio de Meta. WhatsApp trata tus mensajes según sus propias reglas: {ext(WA_PRIVACY, 'Política de privacidad de WhatsApp')}."]),
                ("Para qué usamos tus datos", ["Para responder tus preguntas, preparar cotizaciones, agendar visitas, hacer el trabajo y darle seguimiento. No vendemos ni alquilamos tus datos, y no los usamos para publicidad."]),
                ("Cuánto tiempo los guardamos", ["Guardamos tus mensajes y los datos del trabajo mientras trabajamos juntos y hasta dos años después de tu último servicio, para poder hacer visitas de seguimiento y llevar nuestros registros. Si nos lo pides, los borramos antes, salvo lo que la ley nos obligue a conservar, como el registro de un pago."]),
                ("Tus derechos", [f"Puedes pedirnos que te mostremos los datos que tenemos sobre ti, que los corrijamos o que los borremos. Escríbenos al {LAWN_WA} y te respondemos en un plazo máximo de 30 días. También puedes borrar nuestro chat de tu WhatsApp cuando quieras."]),
                ("Sin cookies y con conteo de visitas sin cookies", ["Este sitio no usa cookies ni etiquetas de publicidad. Para saber cuántas personas lo visitan, usa Cloudflare Web Analytics, una herramienta sin cookies que no establece identificadores, no rastrea a visitantes individuales y solo ofrece conteos agregados (visitas por página, país y tipo de dispositivo). No establece ninguna cookie. Aparte de ese script, que se carga desde Cloudflare, el sitio no carga nada de terceros: las fuentes y las imágenes se sirven desde este mismo sitio, así que tu visita no se comparte con Google, Facebook ni nadie más. Lo comprobamos en la fecha que aparece arriba."]),
                ("Alojamiento", [f"El sitio está alojado en Vercel. Como cualquier servicio de alojamiento, los servidores de Vercel procesan datos técnicos, como tu dirección IP, para mostrarte las páginas y mantenerlas seguras. No usamos esos datos para identificar a nadie. Consulta la {ext(VERCEL_PRIVACY, 'Política de privacidad de Vercel')}."]),
                ("Fotos de propiedades", ["Solo publicamos fotos de la propiedad de un cliente, en este sitio o en cualquier otro lugar, con su permiso."]),
                ("Cambios", ["Si cambiamos esta política, actualizamos esta página y la fecha que aparece arriba."]),
            ],
        },
    },
    "terms": {
        "en": {
            "short": "Terms", "kicker": "Terms",
            "title": "Terms of Use and Service | DR Lawn & Landscape · Island Pest Control",
            "desc": "Terms for this website and for lawn, landscape and pest control services by Darío Reyes in Roatán: free quotes, prices, scheduling, weather and treatment safety.",
            "h1": "Terms of use and service",
            "intro": "These terms cover this website and the services of DR Lawn &amp; Landscape Maintenance and Island Pest Control &amp; Garden Care, both run by Darío Reyes in Roatán. By using the website or booking a service, you accept them.",
            "sections": [
                ("This website", ["The website is for information only. It describes our services, but it is not an offer or a contract. We try to keep it accurate, and details such as services and availability can change."]),
                ("Quotes", ["Quotes are free. A quote is an estimate and is not binding until we both confirm the work, the price and the date on WhatsApp. If the job turns out to be different from what was described, for example a larger area or a bigger infestation, we tell you before continuing and agree on the new price with you."]),
                ("Prices and payment", ["Prices are in lempiras (HNL) or US dollars, as stated in your quote. How and when you pay is also agreed in the quote."]),
                ("Service area", ["We work in Roatán and surrounding areas. If you are not sure we reach your area, ask us on WhatsApp."]),
                ("Scheduling and weather", ["We agree the date and time with you on WhatsApp. Heavy rain or storms can make outdoor work or treatments unsafe or ineffective; when that happens we reschedule to the next available date at no extra cost. If you need to change a date, please tell us as early as possible."]),
                ("Pest treatments and safety", ["Treatments are applied following the instructions on the product label. Before each treatment we give you safety instructions, and you agree to follow them, including:",
                                                ["keeping children, pets and anyone not involved away from treated areas for the time we tell you;",
                                                 "any preparation we ask for, such as storing food or covering surfaces;",
                                                 "telling us beforehand about allergies, pregnancy, pets, fish tanks or vegetable gardens near the area, so we can adapt the treatment."]]),
                ("Your property", ["Please tell us about anything we should avoid, such as buried irrigation lines, cables or plants you want to keep. If something about our work is not right, tell us on WhatsApp as soon as possible and we will look at it."]),
                ("Liability", ["As far as Honduran law allows, our liability for any claim related to a service is limited to the price you paid for that service. We are not responsible for damage caused by safety instructions not being followed, or by events outside our control, such as storms. Nothing in these terms limits liability that the law does not allow us to limit."]),
                ("Governing law", ["These terms are governed by the laws of Honduras. If there is a disagreement, we will first try to solve it directly with you. If that is not possible, it will go to the competent courts of Roatán, Bay Islands."]),
                ("Contact", [f"Lawn &amp; landscape: {LAWN_WA}. Pest control &amp; garden care: {PEST_WA}."]),
            ],
        },
        "es": {
            "short": "Términos", "kicker": "Términos",
            "title": "Términos de uso y servicio | DR Lawn & Landscape · Island Pest Control",
            "desc": "Términos de este sitio y de los servicios de jardinería y control de plagas de Darío Reyes en Roatán: cotizaciones gratis, precios, agenda, clima y seguridad.",
            "h1": "Términos de uso y servicio",
            "intro": "Estos términos aplican a este sitio y a los servicios de DR Lawn &amp; Landscape Maintenance e Island Pest Control &amp; Garden Care, ambos dirigidos por Darío Reyes en Roatán. Al usar el sitio o reservar un servicio, los aceptas.",
            "sections": [
                ("Este sitio", ["El sitio es solo informativo. Describe nuestros servicios, pero no es una oferta ni un contrato. Procuramos que esté al día, y detalles como los servicios y la disponibilidad pueden cambiar."]),
                ("Cotizaciones", ["Las cotizaciones son gratis. Una cotización es un estimado y no es definitiva hasta que ambos confirmamos por WhatsApp el trabajo, el precio y la fecha. Si el trabajo resulta distinto de lo que nos describiste, por ejemplo un área más grande o una plaga más extendida, te avisamos antes de seguir y acordamos contigo el nuevo precio."]),
                ("Precios y pago", ["Los precios son en lempiras (HNL) o en dólares, según lo indique tu cotización. La forma y el momento del pago también se acuerdan en la cotización."]),
                ("Zona de servicio", ["Trabajamos en Roatán y sus alrededores. Si no sabes si llegamos a tu zona, pregúntanos por WhatsApp."]),
                ("Agenda y clima", ["La fecha y la hora las acordamos contigo por WhatsApp. Las lluvias fuertes o las tormentas pueden hacer que el trabajo al aire libre o los tratamientos no sean seguros o no funcionen; en ese caso reprogramamos para la siguiente fecha disponible sin costo adicional. Si necesitas cambiar una fecha, avísanos lo antes posible."]),
                ("Tratamientos contra plagas y seguridad", ["Los tratamientos se aplican siguiendo las instrucciones de la etiqueta del producto. Antes de cada tratamiento te damos instrucciones de seguridad, y te comprometes a seguirlas, entre ellas:",
                                                            ["mantener a niños, mascotas y personas ajenas lejos de las áreas tratadas durante el tiempo que te indiquemos;",
                                                             "hacer la preparación que te pidamos, como guardar alimentos o cubrir superficies;",
                                                             "avisarnos antes si hay alergias, embarazo, mascotas, peceras o huertos cerca del área, para adaptar el tratamiento."]]),
                ("Tu propiedad", ["Cuéntanos de cualquier cosa que debamos evitar, como tuberías de riego enterradas, cables o plantas que quieras conservar. Si algo de nuestro trabajo no quedó bien, avísanos por WhatsApp lo antes posible y lo revisamos."]),
                ("Responsabilidad", ["En la medida en que lo permita la ley hondureña, nuestra responsabilidad por cualquier reclamo relacionado con un servicio se limita al precio que pagaste por ese servicio. No respondemos por daños causados por no seguir las instrucciones de seguridad, ni por hechos fuera de nuestro control, como tormentas. Nada en estos términos limita la responsabilidad que la ley no permite limitar."]),
                ("Ley aplicable", ["Estos términos se rigen por las leyes de Honduras. Si surge un desacuerdo, primero intentaremos resolverlo directamente contigo. Si no es posible, se someterá a los tribunales competentes de Roatán, Islas de la Bahía."]),
                ("Contacto", [f"Jardinería y paisajismo: {LAWN_WA}. Control de plagas y jardines: {PEST_WA}."]),
            ],
        },
    },
    "legal": {
        "en": {
            "short": "Legal notice", "kicker": "Legal notice",
            "title": "Legal Notice | DR Lawn & Landscape · Island Pest Control",
            "desc": "Who runs this website: Darío Reyes, agricultural engineer, owner of DR Lawn & Landscape Maintenance and Island Pest Control & Garden Care in Roatán, Honduras.",
            "h1": "Legal notice",
            "intro": "Who runs this website and how to reach us.",
            "sections": [
                ("Owner", ["Darío Reyes, agricultural engineer (ingeniero agrónomo) trained at UNAG, Honduras' National University of Agriculture."]),
                ("Trade names", ["This website presents two businesses with the same owner:",
                                 ["<strong>DR Lawn &amp; Landscape Maintenance</strong>: lawn and landscape maintenance.",
                                  "<strong>Island Pest Control &amp; Garden Care</strong>: pest control and garden care."]]),
                ("Location", ["Roatán, Islas de la Bahía (Bay Islands), Honduras."]),
                ("Contact", ["We are reached by WhatsApp:",
                             [f"Lawn &amp; landscape: {LAWN_WA}", f"Pest control &amp; garden care: {PEST_WA}"],
                             "Privacy requests go to the lawn number."]),
                ("Hosting", [f"This website is hosted by Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, United States ({ext('https://vercel.com', 'vercel.com')})."]),
                ("Copyright", [f"© {YEAR} Darío Reyes. The texts, the DR Lawn &amp; Landscape and Island Pest Control logos, the ladybug mascot and the design of this website belong to their owner. Please do not copy or reuse them without written permission. Sharing a link to any page is always welcome."]),
                ("Photos", ["Photos of our work published on this website belong to Darío Reyes. Photos of a customer's property are only published with that customer's permission. If you see a photo of your property and want it removed, write to us and we will take it down."]),
                ("External links", ["Links to WhatsApp open a service run by Meta, which has its own terms and privacy policy."]),
            ],
        },
        "es": {
            "short": "Aviso legal", "kicker": "Aviso legal",
            "title": "Aviso legal | DR Lawn & Landscape · Island Pest Control",
            "desc": "Quién está detrás de este sitio: Darío Reyes, ingeniero agrónomo, dueño de DR Lawn & Landscape Maintenance e Island Pest Control & Garden Care en Roatán, Honduras.",
            "h1": "Aviso legal",
            "intro": "Quién está detrás de este sitio y cómo contactarnos.",
            "sections": [
                ("Titular", ["Darío Reyes, ingeniero agrónomo egresado de la UNAG, la Universidad Nacional de Agricultura de Honduras."]),
                ("Nombres comerciales", ["Este sitio presenta dos negocios con el mismo dueño:",
                                         ["<strong>DR Lawn &amp; Landscape Maintenance</strong>: mantenimiento de jardines y áreas verdes.",
                                          "<strong>Island Pest Control &amp; Garden Care</strong>: control de plagas y cuidado de jardines."]]),
                ("Ubicación", ["Roatán, Islas de la Bahía, Honduras."]),
                ("Contacto", ["Nos contactas por WhatsApp:",
                              [f"Jardinería y paisajismo: {LAWN_WA}", f"Control de plagas y jardines: {PEST_WA}"],
                              "Las consultas sobre privacidad van al número de jardinería."]),
                ("Alojamiento", [f"Este sitio está alojado en Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, Estados Unidos ({ext('https://vercel.com', 'vercel.com')})."]),
                ("Derechos de autor", [f"© {YEAR} Darío Reyes. Los textos, los logos de DR Lawn &amp; Landscape e Island Pest Control, la mascota mariquita y el diseño de este sitio pertenecen a su titular. No los copies ni los reutilices sin permiso por escrito. Compartir el enlace a cualquier página siempre es bienvenido."]),
                ("Fotos", ["Las fotos de nuestro trabajo publicadas en este sitio pertenecen a Darío Reyes. Las fotos de la propiedad de un cliente solo se publican con su permiso. Si ves una foto de tu propiedad y quieres que la quitemos, escríbenos y la retiramos."]),
                ("Enlaces externos", ["Los enlaces a WhatsApp abren un servicio de Meta, que tiene sus propios términos y su propia política de privacidad."]),
            ],
        },
    },
}


def _legal_block(item):
    if isinstance(item, list):
        return "<ul>" + "".join(f"<li>{x}</li>" for x in item) + "</ul>"
    return f"<p>{item}</p>"


def legal_page(kind, lang):
    p = PATHS[(kind, lang)]
    home_ = rel(p, PATHS[("home", lang)])
    d = LEGAL[kind][lang]
    secs = "".join(f'<section aria-labelledby="s{i}"><h2 id="s{i}">{h}</h2>{"".join(_legal_block(x) for x in items)}</section>'
                   for i, (h, items) in enumerate(d["sections"], 1))
    others = " · ".join(f'<a href="{rel(p, PATHS[(k, lang)])}">{LEGAL[k][lang]["h1"]}</a>' for k in LEGAL_PAGES if k != kind)
    upd = T(lang, f"Last updated: {LEGAL_UPDATED[0]}", f"Última actualización: {LEGAL_UPDATED[1]}")
    body = f"""<main id="main" class="legal">
  <div class="wrap crumbs"><a href="{home_}">{T(lang, "Home", "Inicio")}</a> / {d["short"]}</div>
  <div class="wrap">
    <article class="legal-card" aria-labelledby="hero-title">
      <p class="kicker">DR Lawn &amp; Landscape · Island Pest Control</p>
      <h1 id="hero-title">{d["h1"]}</h1>
      <p class="legal-updated"><time datetime="{LEGAL_UPDATED[2]}">{upd}</time></p>
      <p class="lead">{d["intro"]}</p>
      <div class="legal-body">{secs}</div>
      <p class="legal-more">{T(lang, "See also", "Ver también")}: {others}</p>
    </article>
  </div>
</main>
"""
    return head(kind, lang, d["title"], d["desc"]) + header(kind, lang) + body + footer(kind, lang)


# ---------------------------------------------------------------- 404 (self-contained, works at any path)
NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | DR Lawn &amp; Landscape · Island Pest Control</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#234f17">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>
@font-face{font-family:"DM Serif Display";font-weight:400;font-display:swap;src:url("/assets/fonts/dm-serif-display-400.woff2") format("woff2")}
@font-face{font-family:"Work Sans";font-weight:400 600;font-display:swap;src:url("/assets/fonts/work-sans-var.woff2") format("woff2")}
@font-face{font-family:"Caveat";font-weight:600;font-display:swap;src:url("/assets/fonts/caveat-600.woff2") format("woff2")}
:root{--cream:#f6f2ea;--paper:#fffdf8;--ink:#1f2a1c;--muted:#4c5747;--line:#d9d0bd;--green:#2f6b1f;--green-deep:#234f17;--terra:#a8471f;--terra-soft:#f2c9a8;--red:#b02a1f;--red-deep:#8f2118;--wa:#1e7a46}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;min-height:100vh;display:grid;place-items:center;background:radial-gradient(circle at 1px 1px,rgba(35,79,23,.08) 1px,transparent 1.6px) 0 0/16px 16px,var(--cream);color:var(--ink);font:400 1rem/1.6 "Work Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:32px 16px}
main{width:100%;max-width:680px;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:38px 24px 32px;box-shadow:0 1px 2px rgba(31,42,28,.06),0 8px 24px rgba(31,42,28,.06);position:relative;overflow:hidden}
main::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:linear-gradient(90deg,var(--green) 50%,var(--red) 50%)}
.marks{display:flex;align-items:center;gap:10px;margin-bottom:22px}.marks img{mix-blend-mode:multiply;display:block}
.k{font:600 .75rem/1.4 "Work Sans",system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:0}
h1{font:400 clamp(2.1rem,7vw,3.2rem)/1.08 "DM Serif Display",Georgia,serif;margin:10px 0 6px;letter-spacing:-.01em}
.es{display:block;font-family:"Caveat",cursive;font-weight:600;color:var(--green);font-size:clamp(1.6rem,5vw,2rem);line-height:1.2;margin-bottom:14px}
p{color:var(--muted);margin:0 0 .8em}
.b{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.b a{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:10px 20px;border-radius:999px;font-weight:600;text-decoration:none;color:#fff;border:2px solid transparent}
.h{background:var(--green-deep)}.h.o{background:transparent;color:var(--green-deep);border-color:var(--green-deep)!important}.l{background:var(--wa)}.p{background:var(--red)}
.b a:hover{filter:brightness(.92)}
:focus-visible{outline:3px solid var(--terra);outline-offset:3px;border-radius:6px}
@media (max-width:559px){.b a{width:100%;padding:10px 14px;font-size:.95rem;white-space:nowrap}}
</style>
</head>
<body>
<main>
<div class="marks"><img id="m-dr" src="/assets/logo-dr-lawn.jpg" width="54" height="54" alt=""><img id="m-ipc" src="/assets/ipc-mark.png" width="34" height="44" alt=""></div>
<p class="k">404 · DR Lawn &amp; Landscape · Island Pest Control</p>
<h1>This page doesn't exist.</h1>
<span class="es" lang="es">Esta página no existe.</span>
<p>The link may be old or mistyped. Go back to the home page, or write to us on WhatsApp.</p>
<p lang="es">Puede que el enlace sea antiguo o tenga un error. Vuelve al inicio o escríbenos por WhatsApp.</p>
<div class="b">
<a class="h" id="home-en" href="/">Home</a>
<a class="h o" id="home-es" href="/es/" lang="es">Inicio</a>
<a class="l" href="https://wa.me/50498350265" target="_blank" rel="noopener">WhatsApp lawn · +504 9835-0265</a>
<a class="p" href="https://wa.me/50488695915" target="_blank" rel="noopener">WhatsApp pest · +504 8869-5915</a>
</div>
</main>
<script>
// Works on a custom domain, on Vercel and on a GitHub Pages project path (/dario-roatan/).
(function(){var base=location.pathname.indexOf('/dario-roatan/')===0?'/dario-roatan/':'/';
document.getElementById('home-en').href=base;document.getElementById('home-es').href=base+'es/';
document.getElementById('m-dr').src=base+'assets/logo-dr-lawn.jpg';document.getElementById('m-ipc').src=base+'assets/ipc-mark.png';})();
</script>
@@ANALYTICS@@
</body>
</html>
"""
NOT_FOUND = NOT_FOUND.replace("@@ANALYTICS@@", ANALYTICS)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path, len(content))


def csp_hash(src):
    import base64, hashlib
    return "'sha256-" + base64.b64encode(hashlib.sha256(src.encode()).digest()).decode() + "'"


def vercel_json():
    """vercel.json is generated so the CSP hashes always match the two inline scripts (JS flag + 404 base fix)."""
    import json, re
    inline_404 = re.search(r"<script>(.*?)</script>", NOT_FOUND, re.S).group(1)
    csp = ("default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
           f"script-src 'self' {csp_hash(JS_FLAG)} {csp_hash(inline_404)} https://static.cloudflareinsights.com; font-src 'self'; connect-src 'self' https://cloudflareinsights.com; "
           "frame-ancestors 'none'; base-uri 'self'; form-action 'self' https://wa.me https://api.whatsapp.com")
    sec = [{"key": "X-Content-Type-Options", "value": "nosniff"},
           {"key": "X-Frame-Options", "value": "DENY"},
           {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
           {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=()"},
           {"key": "Content-Security-Policy", "value": csp}]
    cfg = {"trailingSlash": True, "headers": [
        {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
        {"source": "/(.*)", "headers": sec}]}
    return json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"


def main():
    for lang in ("en", "es"):
        write(PATHS[("home", lang)] + "index.html", home(lang))
        write(PATHS[("lawn", lang)] + "index.html", lawn_page(lang))
        write(PATHS[("pest", lang)] + "index.html", pest_page(lang))
        for kind in LEGAL_PAGES:
            write(PATHS[(kind, lang)] + "index.html", legal_page(kind, lang))
    write("404.html", NOT_FOUND)
    write("vercel.json", vercel_json())
    urls = []
    for page in ("home", "lawn", "pest") + LEGAL_PAGES:
        for lang in ("en", "es"):
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE + PATHS[(page, l)]}"/>' for l in ("en", "es"))
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE + PATHS[(page, "en")]}"/>'
            urls.append(f"  <url>\n    <loc>{BASE + PATHS[(page, lang)]}</loc>\n    <lastmod>2026-10-22</lastmod>{alts}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")


if __name__ == "__main__":
    main()
