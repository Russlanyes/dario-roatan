#!/usr/bin/env python3
"""Static generator for the merged Darío Reyes site (DR Lawn & Landscape + Island Pest Control).

Run:  python3 build.py   -> writes index.html, es/index.html, lawn/, pest/, es/jardineria/, es/plagas/,
      404.html, sitemap.xml, robots.txt. All copy lives in this file (EN + ES side by side).
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

PATHS = {
    ("home", "en"): "", ("home", "es"): "es/",
    ("lawn", "en"): "lawn/", ("lawn", "es"): "es/jardineria/",
    ("pest", "en"): "pest/", ("pest", "es"): "es/plagas/",
}
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
            "telephone": LAWN_TEL, "logo": BASE + "assets/logo-dr-lawn.jpg", "image": BASE + "assets/og-image.jpg",
            "address": addr, "areaServed": "Roatán, Bay Islands, Honduras", "founder": {"@id": BASE + "#dario"},
            "knowsLanguage": ["en", "es"]}
    pest = {"@type": "LocalBusiness", "@id": BASE + "#pest", "name": "Island Pest Control & Garden Care",
            "slogan": "Your peace of mind is our mission", "url": BASE + PATHS[("pest", lang)],
            "telephone": PEST_TEL, "logo": BASE + "assets/ipc-wordmark.png", "image": BASE + "assets/og-image.jpg",
            "address": addr, "areaServed": "Roatán, Bay Islands, Honduras", "founder": {"@id": BASE + "#dario"},
            "knowsLanguage": ["en", "es"]}
    graph = {"home": [person, lawn, pest], "lawn": [person, lawn], "pest": [person, pest]}[page]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- shell
def head(page, lang, title, desc):
    path = PATHS[(page, lang)]
    en_url, es_url = BASE + PATHS[(page, "en")], BASE + PATHS[(page, "es")]
    a = rel(path, "assets/")
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
<meta property="og:image" content="{BASE}assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="DR Lawn &amp; Landscape Maintenance and Island Pest Control &amp; Garden Care logos">
<meta property="og:locale" content="{T(lang, 'en_US', 'es_HN')}">
<meta property="og:locale:alternate" content="{T(lang, 'es_HN', 'en_US')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{a}favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{a}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=DM+Serif+Display&family=Work+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{a}styles.css">
<script type="application/ld+json">
{jsonld(page, lang)}
</script>
<!-- Analytics placeholder: none installed yet. Add a privacy-friendly snippet here once the client approves. -->
<script>document.documentElement.classList.add("js")</script>
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
                 ("#contact", T(lang, "Contact", "Contacto"), False)]
        if page == "lawn":
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
      <span>{T(lang, "Roatán, Bay Islands, Honduras", "Roatán, Islas de la Bahía, Honduras")}</span>
    </div>
  </div>
</footer>

<div class="wa-bar">
  <a class="btn btn-wa" href="{escape(wa(LAWN, lawn_msg(lang)))}" target="_blank" rel="noopener">{ic("wa", True)}<span>{T(lang, "Lawn quote", "Jardinería")}<small>{LAWN_SHOW}</small></span></a>
  <a class="btn btn-red" href="{escape(wa(PEST, pest_msg(lang)))}" target="_blank" rel="noopener">{ic("wa", True)}<span>{T(lang, "Pest inspection", "Plagas")}<small>{PEST_SHOW}</small></span></a>
</div>

<script src="{a}site.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks
def ph(caption, cls="", icon="leaf"):
    return (f'<figure class="ph {cls}" role="img" aria-label="[photo] {escape(caption)}">{ic(icon)}'
            f'<figcaption aria-hidden="true">[photo] {escape(caption)}</figcaption></figure>')


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
      {ph(T(lang, "Portrait of Darío Reyes", "Retrato de Darío Reyes"), "portrait")}
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
        <p class="form-note">{T(lang, "Opens WhatsApp with your message ready to send. Nothing is stored on this site.", "Abre WhatsApp con tu mensaje listo para enviar. Este sitio no guarda ningún dato.")}</p>
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
      <div class="gallery">{ph(T(lang, "Freshly mowed lawn in Roatán", "Césped recién cortado en Roatán"))}{ph(T(lang, "Trimmed hedges and clean edges", "Setos y bordes recortados"), "alt")}{ph(T(lang, "Yard clean up, before and after", "Limpieza de jardín, antes y después"), "alt")}{ph(T(lang, "Landscaped garden bed", "Jardín paisajístico"))}</div>
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
      <div class="cards">{cards}</div>
    </div>
  </section>

  <section class="band-paper" id="work" aria-labelledby="work-title">
    <div class="wrap">
      <div class="section-head"><p class="kicker">{T(lang, "Our work", "Nuestro trabajo")}</p><h2 class="h2" id="work-title">{T(lang, "On the job in Roatán", "Trabajando en Roatán")}</h2></div>
      <div class="gallery g3">{ph(T(lang, "Inspection in a restaurant kitchen", "Inspección en la cocina de un restaurante"), "pest", "bug")}{ph(T(lang, "Preventive treatment at a vacation rental", "Tratamiento preventivo en una renta vacacional"), "pest", "spray")}{ph(T(lang, "Garden maintenance and pruning", "Mantenimiento y poda de jardín"), "alt")}</div>
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


# ---------------------------------------------------------------- 404 (self-contained, works at any path)
NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | DR Lawn &amp; Landscape · Island Pest Control</title>
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%23234f17'/%3E%3Ctext x='32' y='42' font-family='Georgia' font-size='28' fill='%23fffdf8' text-anchor='middle'%3EDR%3C/text%3E%3C/svg%3E">
<style>
:root{--cream:#f6f2ea;--ink:#1f2a1c;--muted:#4c5747;--green:#2f6b1f;--green-deep:#234f17;--terra:#a8471f;--red:#b02a1f;--wa:#1e7a46}
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--cream);color:var(--ink);font:400 1rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:24px 16px}
main{max-width:620px}.k{font:600 .75rem/1.4 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--terra)}
h1{font:400 clamp(2.2rem,7vw,3.4rem)/1.1 Georgia,serif;margin:10px 0 14px}p{color:var(--muted)}
.b{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.b a{display:inline-flex;align-items:center;min-height:46px;padding:10px 20px;border-radius:999px;font-weight:600;text-decoration:none;color:#fff}
.h{background:var(--green-deep)}.l{background:var(--wa)}.p{background:var(--red)}
</style>
</head>
<body>
<main>
<p class="k">404 · DR Lawn &amp; Landscape · Island Pest Control</p>
<h1>This page doesn't exist. <span lang="es">Esta página no existe.</span></h1>
<p>The link may be old or mistyped. Go back to the home page, or write to us on WhatsApp.<br><span lang="es">Puede que el enlace sea antiguo o tenga un error. Vuelve al inicio o escríbenos por WhatsApp.</span></p>
<div class="b">
<a class="h" id="home-en" href="/">Home</a>
<a class="h" id="home-es" href="/es/" lang="es">Inicio</a>
<a class="l" href="https://wa.me/50498350265" target="_blank" rel="noopener">WhatsApp lawn · +504 9835-0265</a>
<a class="p" href="https://wa.me/50488695915" target="_blank" rel="noopener">WhatsApp pest · +504 8869-5915</a>
</div>
</main>
<script>
// Works on a custom domain, on Vercel and on a GitHub Pages project path (/dario-roatan/).
(function(){var base=location.pathname.indexOf('/dario-roatan/')===0?'/dario-roatan/':'/';
document.getElementById('home-en').href=base;document.getElementById('home-es').href=base+'es/';})();
</script>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path, len(content))


def main():
    for lang in ("en", "es"):
        write(PATHS[("home", lang)] + "index.html", home(lang))
        write(PATHS[("lawn", lang)] + "index.html", lawn_page(lang))
        write(PATHS[("pest", lang)] + "index.html", pest_page(lang))
    write("404.html", NOT_FOUND)
    urls = []
    for page in ("home", "lawn", "pest"):
        for lang in ("en", "es"):
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE + PATHS[(page, l)]}"/>' for l in ("en", "es"))
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE + PATHS[(page, "en")]}"/>'
            urls.append(f"  <url>\n    <loc>{BASE + PATHS[(page, lang)]}</loc>\n    <lastmod>2026-10-17</lastmod>{alts}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")


if __name__ == "__main__":
    main()
