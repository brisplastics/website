"""Build v7 of the BPC site from v6. Run: python3 -I build.py <v6_dir> <out_dir>"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import *
import hospital, printing

V6, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))

def v6(name):
    t = open(os.path.join(V6, name), encoding="utf-8").read()
    title = html.unescape(re.search(r"<title>(.*?)</title>", t, re.S).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', t, re.S).group(1))
    main = re.search(r'<main id="main">\n?(.*?)\n?</main>', t, re.S).group(1)
    return title, desc, main

def fix(s):
    s = s.replace("<li><strong>Factory</strong><br>Tingalpa QLD 4173</li>", f"<li><strong>Phone</strong><br><a href=\"tel:{TEL_07}\">{PHONE_07}</a> or <a href=\"tel:{TEL_1300}\">{PHONE_1300}</a></li>\n<li><strong>Factory</strong><br>{ADDRESS}</li>")
    s = s.replace("Same factory in Tingalpa and the same product range.", "Same factory at 45a Millennium Place, Tingalpa, the same phone numbers and the same product range.")
    s = s.replace("From 12 October 2026", "From 26 October 2026")
    s = s.replace("from 12 October 2026", "from 26 October 2026")
    s = s.replace("Owner of Plastics Unique and Sov Services from 12 October 2026", "Owner of Plastics Unique and Sov Services")
    s = s.replace("Orders placed before 12 October 2026 are passed to the Plastics Unique team to fulfil. ", "")
    return s

pages = {}

# ---- Home: v6 content plus links into the two new sections ----
t, d, m = v6("index.html")
m = fix(m)
m = m.replace('<li class="t-green"><h3>Hospital products</h3><p>Patient chart holders, bed chart folders and ward stationery, supplied through our Sov Services division.</p></li>',
              '<li class="t-green"><h3><a href="/hospital/" style="color:inherit">Hospital products</a></h3><p>Patient chart folders, chart holders, dividers and glove box holders from our Sov Services range. <a href="/hospital/order">Order online</a>.</p></li>')
m = m.replace('<li class="t-ink"><h3>Printing and branding</h3><p>Screen printing, flatbed UV printing and foil blocking, applied in-house so your job stays under one roof.</p></li>',
              '<li class="t-ink"><h3><a href="/uv-printing/" style="color:inherit">Printing and branding</a></h3><p>Screen printing, foil blocking and full-colour UV flatbed printing up to 1250 × 2500 mm. <a href="/uv-printing/trade">Trade printing</a> for sign shops and printers.</p></li>')
m = m.replace('<li><strong>Medical and hospital</strong><span>Chart holders and ward products through Sov Services.</span></li>',
              '<li><strong><a href="/hospital/">Medical and hospital</a></strong><span>Chart folders, holders and ward products through Sov Services.</span></li>')
feature = '''<section class="block"><div class="wrap">
<div class="section-head"><h2>Two ways in</h2><p class="lede">Ordering for a hospital ward, or need something printed? Go straight there.</p></div>
<ul class="cards">
<li style="--tab:var(--pvc-green)"><h3><a href="/hospital/">Sov Services hospital range</a></h3><p>Patient chart folders, chart holders, dividers and glove box holders. Same item codes, now ordered online.</p><a class="more" href="/hospital/order">Order or reorder</a></li>
<li style="--tab:var(--ink)"><h3><a href="/uv-printing/">UV flatbed printing</a></h3><p>Full colour and white on acrylic, PVC, ACM, wood and glass up to 1250 × 2500 mm. Trade and direct.</p><a class="more" href="/uv-printing/">Printing services</a></li>
</ul>
</div></section>
'''
m = m.replace('<section class="block"><div class="wrap">\n<div class="section-head"><h2>Who we make it for</h2>', feature + '<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>Who we make it for</h2>', 1)
m = m.replace('<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>How ordering works</h2>', gallery([
    ("hospital-chart-folder-ward-bed.jpg", "Green hospital patient chart folder with ward and bed print", "Sov Services chart folders"),
    ("safety-data-sheet-binder.jpg", "Safety data sheet ring binder", "Safety data sheet binders"),
    ("noren-tags-sizes.jpg", "Clear PVC noren tag holders", "Noren tag holders"),
    ("pvc-polypropylene-colour-range.jpg", "Stock PVC and polypropylene colour range", "Our stock colours"),
], "Made in Tingalpa") + '\n<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>How ordering works</h2>', 1)
pages["/"] = page("/", "Custom PVC & Polypropylene Products, Brisbane | Brisbane Plastics Company",
                  "Brisbane manufacturer of custom PVC and polypropylene products, Sov Services hospital chart folders and holders, and trade UV flatbed printing. Tingalpa.", m)

# ---- What we make ----
t, d, m = v6("products.html")
m = fix(m)
m = m.replace('<li class="t-green"><h3>Hospital products</h3>', '<li class="t-green"><h3><a href="/hospital/" style="color:inherit">Hospital products</a></h3>')
m = m.replace('<li class="t-ink"><h3>Printing and branding</h3>', '<li class="t-ink"><h3><a href="/uv-printing/" style="color:inherit">Printing and branding</a></h3>')
m = m.replace('<li><strong>Screen printing and UV flatbed printing.</strong> Your logo and artwork printed directly onto the product.</li>',
              '<li><strong>Screen printing and <a href="/uv-printing/">UV flatbed printing</a>.</strong> Spot colours by screen, full colour and white by UV flatbed up to 1250 × 2500 mm.</li>')
prod_gal = gallery([
    ("pvc-polypropylene-colour-range.jpg", "Fan of stock PVC and polypropylene colour swatches with colour names", "Stock PVC and polypropylene colours"),
    ("safety-data-sheet-binder.jpg", "Yellow and black striped safety data sheet ring binder", "Safety data sheet binder"),
    ("embossed-pvc-cover.jpg", "Navy PVC cover embossed with Guest Information", "Embossed PVC cover"),
    ("noren-tags-sizes.jpg", "Clear PVC noren tag holders in large, standard and small sizes", "Clear noren tag holders, three sizes"),
    ("pvc-luggage-tags.jpg", "Orange PVC luggage tags with strap", "PVC luggage tags"),
    ("clipboard-fitting-detail.jpg", "Close-up of a riveted metal clipboard fitting on a PVC cover", "Fittings riveted in house"),
    ("tally-book.jpg", "Spiral tally book shown against a ruler", "Tally books"),
    ("screen-printing-press.jpg", "Screen printing press in the Tingalpa factory", "Screen printing in Tingalpa"),
], "From our factory", "A few of the products and processes we run every week in Tingalpa.")
m = m.replace('<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>Industries we supply</h2>', prod_gal + '\n<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>Industries we supply</h2>', 1)
pages["/products"] = page("/products", t, d, m, [("/", "Home"), ("/products", "What we make")])

# ---- About ----
t, d, m = v6("about.html")
pages["/about"] = page("/about", t, fix(d), fix(m), [("/", "Home"), ("/about", "About us")])

# ---- Contact ----
t, d, m = v6("contact.html")
m = fix(m)
m = m.replace('<div class="wrap split" style="grid-template-columns:1.6fr 1fr">','<div class="wrap split contact-split">')
m = m.replace('<option>Hospital product (Sov Services)</option>', '<option>Hospital product (Sov Services)</option><option>UV flatbed printing</option>')
m = m.replace('<li><strong>Live chat</strong>', f'<li><strong>Hospital orders</strong><br>Use the <a href="/hospital/order">hospital order form</a> or email <a href="mailto:{SOV_EMAIL}">{SOV_EMAIL}</a></li>\n<li><strong>Printing</strong><br>Use the <a href="/uv-printing/#quote">print quote form</a> for UV printing jobs.</li>\n<li><strong>Live chat</strong>')
pages["/contact"] = page("/contact", t, d, m, [("/", "Home"), ("/contact", "Request a quote")])

# ---- Privacy, thanks, 404 ----
t, d, m = v6("privacy.html"); pages["/privacy"] = page("/privacy", t, d, fix(m))
t, d, m = v6("thanks.html"); pages["/thanks"] = page("/thanks", t, d, fix(m), noindex=True)
t, d, m = v6("404.html"); pages["/404"] = page("/404", t, d, fix(m), noindex=True)

pages.update(hospital.build())
pages.update(printing.build())

# ---- write pages ----
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
def outfile(path):
    if path == "/":
        return "index.html"
    if path.endswith("/"):
        return path.strip("/") + "/index.html"
    return path.strip("/") + ".html"
for path, body in pages.items():
    f = os.path.join(OUT, outfile(path))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, "w", encoding="utf-8").write(body)

# ---- assets ----
shutil.copytree(os.path.join(V6, "assets"), os.path.join(OUT, "assets"))
shutil.copytree(os.path.join(HERE, "photos"), os.path.join(OUT, "assets/img/products"))
css = open(os.path.join(V6, "assets/css/site.css"), encoding="utf-8").read() + open(os.path.join(HERE, "extra.css"), encoding="utf-8").read()
open(os.path.join(OUT, "assets/css/site.css"), "w", encoding="utf-8").write(css)
js = open(os.path.join(V6, "assets/js/site.js"), encoding="utf-8").read()
js = js.replace("var TAWK_PROPERTY_ID='', TAWK_WIDGET_ID='default';", "var TAWK_PROPERTY_ID='6adc80751b93b634803314f9', TAWK_WIDGET_ID='1k5mlbjah';")
js += '''
// Google Analytics 4. Paste the Measurement ID (G-XXXXXXX). Blank = nothing loads.
// Thank-you pages (/thanks, /hospital/thanks, /uv-printing/thanks) are the conversion events for Google Ads.
(function(){
  var GA4_ID='';
  if(!GA4_ID)return;
  var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA4_ID;document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
  gtag('js',new Date());gtag('config',GA4_ID);
})();
'''
open(os.path.join(OUT, "assets/js/site.js"), "w", encoding="utf-8").write(js)
shutil.copy(os.path.join(HERE, "brand/logo.svg"), os.path.join(OUT, "favicon.svg"))
shutil.copy(os.path.join(HERE, "brand/logo.svg"), os.path.join(OUT, "assets/img/logo.svg"))
shutil.copy(os.path.join(HERE, "brand/og-image.png"), os.path.join(OUT, "assets/img/og-image.png"))

# ---- sitemap, robots, netlify ----
locs = [p for p in pages if p not in ("/thanks", "/404", "/hospital/thanks", "/uv-printing/thanks")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{url(p)}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for p in locs)
sm += "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thanks\nDisallow: /hospital/thanks\nDisallow: /uv-printing/thanks\n\nSitemap: {SITE}/sitemap.xml\n")
nt=open(os.path.join(V6, "netlify.toml")).read()
nt+="\n# Keep the page generator source private\n[[redirects]]\n  from = \"/_src/*\"\n  to = \"/404\"\n  status = 404\n  force = true\n"
open(os.path.join(OUT, "netlify.toml"),"w").write(nt)
for extra in ("README.md", "sovservices-redirects-PENDING.toml"):
    shutil.copy(os.path.join(HERE, extra), OUT)
shutil.copytree(HERE, os.path.join(OUT, "_src"), ignore=shutil.ignore_patterns("__pycache__", "README.md", "sovservices-redirects-PENDING.toml"))
print(len(pages), "pages")
