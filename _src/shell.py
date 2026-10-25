"""Shared page shell for the Brisbane Plastics Company static site.

Output is plain HTML, so Netlify needs no build step. Change SITE at cutover
(for example to https://plasticsunique.com.au) and re-run build.py.
"""
import json, html, os

SITE = "https://brisplastics.com.au"
NAME = "Brisbane Plastics Company"
LEGAL = "Brisbane Plastics Company Pty Ltd"
ACN = "699 248 658"
ABN = "14 699 248 658"
SALES = "sales@brisplastics.com.au"
SOV_EMAIL = "support@sovservices.net.au"
PHONE_07 = "(07) 3396 3744"
TEL_07 = "+61733963744"
PHONE_1300 = "1300 744 104"
TEL_1300 = "1300744104"
STREET = "45a Millennium Place"
ADDRESS = "45a Millennium Place, Tingalpa QLD 4173"
LASTMOD = "2026-10-25"

# Solar and recyclable badges in the footer. Claims are being checked with Chris (25/10/2026).
# Set to False and rebuild to remove them. The Australian Made logo is NOT used until the licence transfers.
SHOW_ECO_BADGES = True
BRAND = "/assets/img/brand/"

NAV = [
    ("/", "Home", ""),
    ("/products", "Products", "/products"),
    ("/hospital/", "Hospital", "/hospital"),
    ("/uv-printing/", "UV printing", "/uv-printing"),
    ("/about", "About us", "/about"),
]

LOGO = ('<svg width="40" height="44" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 44">'
        '<path d="M20 1.5 38 11.75v20.5L20 42.5 2 32.25v-20.5z" fill="#122B4A"/>'
        '<path d="M20 7.5 32.5 14.6v14.8L20 36.5 7.5 29.4V14.6z" fill="#1E5FD9"/>'
        '<path d="M14.5 15.5h6.6c2.8 0 4.5 1.4 4.5 3.6 0 1.3-.7 2.3-1.9 2.8 1.5.4 2.4 1.6 2.4 3.1 0 2.4-1.8 3.8-4.8 3.8h-6.8zm3.1 2.5v2.8h3.1c1 0 1.6-.5 1.6-1.4s-.6-1.4-1.6-1.4zm0 5.2v3h3.5c1 0 1.7-.6 1.7-1.5s-.7-1.5-1.7-1.5z" fill="#fff"/></svg>')

BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness",
    "@id": SITE + "/#business", "name": NAME, "legalName": LEGAL,
    "url": SITE + "/", "logo": SITE + "/assets/img/brand/icon-512.png",
    "image": SITE + "/assets/img/og-image.png", "email": SALES,
    "description": "Brisbane manufacturer of custom PVC and polypropylene products, hospital chart folders and holders (Sov Services), and trade UV flatbed printing up to 1250 x 2500 mm.",
    "telephone": "+61733963744",
    "address": {"@type": "PostalAddress", "streetAddress": "45a Millennium Place", "addressLocality": "Tingalpa", "addressRegion": "QLD", "postalCode": "4173", "addressCountry": "AU"},
    "areaServed": "Australia",
    "parentOrganization": {"@type": "Organization", "name": "FormFill Group", "url": "https://www.formfill.com.au/"},
    "brand": [{"@type": "Brand", "name": "Plastics Unique"}, {"@type": "Brand", "name": "Sov Services"}],
    "founder": [{"@type": "Person", "name": "Bruce Bairstow", "jobTitle": "Director"},
                {"@type": "Person", "name": "Mathew Bowden", "jobTitle": "Managing Director"}],
}

def esc(s):
    return html.escape(s, quote=True)

def url(path):
    return SITE + path

def crumbs_html(crumbs):
    """crumbs: list of (path, label); last item is the current page."""
    if not crumbs:
        return ""
    items = []
    for i, (p, label) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{esc(label)}</li>')
        else:
            items.append(f'<li><a href="{p}">{esc(label)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"

def crumbs_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": label, "item": url(p)}
                                for i, (p, label) in enumerate(crumbs)]}

def faq_block(faqs, heading="Questions we get asked"):
    body = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faqs)
    return f'<div class="faq"><h2>{esc(heading)}</h2>{body}</div>'

def faq_schema(faqs):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]}

def header(path):
    lis = []
    for href, label, prefix in NAV:
        current = (path == "/") if href == "/" else (prefix and path.startswith(prefix))
        cur = ' aria-current="page"' if current else ""
        lis.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    lis.append('<li><a class="btn" href="/contact">Request a quote</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>{ADDRESS}</span><span><a href="tel:{TEL_07}">{PHONE_07}</a> · <a href="tel:{TEL_1300}">{PHONE_1300}</a></span></div></div>
<header class="site-head">
<div class="wrap">
<a class="brand" href="/" aria-label="Brisbane Plastics Company home"><img src="{BRAND}BPC_Logo_Fan_Stacked_v1_CAI.svg" alt="Brisbane Plastics Company" width="193" height="52"></a>
<nav aria-label="Main">
<button class="nav-toggle" aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu">{"".join(lis)}</ul>
</nav>
</div>
</header>'''

def eco_badges():
    if not SHOW_ECO_BADGES:
        return ""
    return (f'<div class="eco-badges" data-removable="eco">'
            f'<img src="{BRAND}Icon_SolarPowered_White_on_Navy_v1_CAI.svg" alt="Solar powered factory" width="52" height="52" loading="lazy">'
            f'<img src="{BRAND}Icon_Recyclable_White_on_Navy_v1_CAI.svg" alt="Recyclable materials" width="55" height="52" loading="lazy"></div>')

def footer():
    return f'''<footer class="site-foot">
<div class="wrap">
<div>
<img class="foot-logo" src="{BRAND}BPC_Logo_Fan_Stacked_White_v1_CAI.svg" alt="Brisbane Plastics Company" width="223" height="60" loading="lazy">
<p>Custom PVC and polypropylene products, hospital products and UV flatbed printing, made in Tingalpa, Brisbane.</p>
<p>Part of <a href="https://www.formfill.com.au/" rel="noopener">FormFill Group</a>, a South East Queensland plastics manufacturing group.</p>
<div class="foot-brands"><span>Our brands</span>
<a href="/products" aria-label="Plastics Unique products"><img src="{BRAND}PU_Logo_Endorsed_White_v2_CAI.svg" alt="Plastics Unique, a Brisbane Plastics Company" width="131" height="60" loading="lazy"></a>
<a href="/hospital/" aria-label="Sov Services hospital range"><img src="{BRAND}Sov_Logo_Endorsed_White_v2_CAI.svg" alt="Sov Services, a Brisbane Plastics Company" width="163" height="60" loading="lazy"></a></div>
{eco_badges()}
</div>
<div>
<h2>Contact</h2>
<ul><li>Phone: <a href="tel:{TEL_07}">{PHONE_07}</a></li><li>Phone: <a href="tel:{TEL_1300}">{PHONE_1300}</a></li><li>Sales: <a href="mailto:{SALES}">{SALES}</a></li><li>Hospital orders: <a href="mailto:{SOV_EMAIL}">{SOV_EMAIL}</a></li><li>{ADDRESS}</li></ul>
</div>
<div>
<h2>Site</h2>
<ul><li><a href="/products">Products</a></li><li><a href="/hospital/">Hospital products</a></li><li><a href="/hospital/order">Hospital order form</a></li><li><a href="/uv-printing/">UV flatbed printing</a></li><li><a href="/uv-printing/trade">Trade printing</a></li><li><a href="/about">About us</a></li><li><a href="/contact">Request a quote</a></li><li><a href="/privacy">Privacy</a></li></ul>
</div>
<p class="legal">© 2026 {LEGAL} · ACN {ACN} · ABN {ABN}</p>
</div>
</footer>
<script src="/assets/js/site.js" defer></script>'''

def page(path, title, desc, main, crumbs=None, schema=None, noindex=False, og_type="website"):
    schemas = [BUSINESS]
    if crumbs:
        schemas.append(crumbs_schema(crumbs))
    schemas += schema or []
    ld = "\n".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schemas)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    canon = url(path)
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{canon}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#122B4A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/brand/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=IBM+Plex+Mono:wght@500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{ld}
</head>
<body>
{header(path)}
<main id="main">
{main}
</main>
{footer()}
</body>
</html>
'''

def cta(heading="Need a quote or a repeat order?", primary=("/contact", "Request a quote"), secondary=("/contact?type=repeat", "Reorder a past job")):
    return f'''<section class="cta"><div class="wrap">
<h2>{heading}</h2>
<div class="btn-row" style="margin:0"><a class="btn" href="{primary[0]}">{primary[1]}</a><a class="btn ghost" href="{secondary[0]}">{secondary[1]}</a></div>
</div></section>'''

def hero(crumbs, h1, lede, kicker=None, buttons=None):
    k = f'<span class="kicker">{kicker}</span>' if kicker else ""
    b = ""
    if buttons:
        b = '<div class="btn-row">' + "".join(
            f'<a class="btn{" ghost" if i else ""}" href="{h}">{t}</a>' for i, (h, t) in enumerate(buttons)) + "</div>"
    return f'''<section class="page-hero"><div class="wrap">
{crumbs_html(crumbs)}
{k}<h1>{h1}</h1>
<p class="lede">{lede}</p>
{b}
</div></section>'''


PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")

def gallery(items, heading=None, lede=None, alt_bg=False):
    """items: list of (file, alt, caption). Photos from the Plastics Unique product photo library."""
    from PIL import Image
    figs = []
    for f, alt, cap in items:
        w, h = Image.open(os.path.join(PHOTO_DIR, f)).size
        figs.append(f'<figure><img src="/assets/img/products/{f}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>')
    head = ""
    if heading:
        head = f'<div class="section-head"><h2>{heading}</h2>' + (f'<p class="lede">{lede}</p>' if lede else "") + "</div>"
    cls = "block alt" if alt_bg else "block"
    return f'<section class="{cls}"><div class="wrap">{head}<div class="gallery">{"".join(figs)}</div></div></section>'
