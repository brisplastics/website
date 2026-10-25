"""Build v7 of the BPC site from v6. Run: python3 -I build.py <v6_dir> <out_dir>"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import *
import hospital, printing, catalogue, json
from catalogue_data import PRODUCTS as CAT, PU_REDIRECTS

V6, OUT = sys.argv[1], sys.argv[2]
CAT_PHOTOS = sys.argv[3] if len(sys.argv) > 3 else None  # folder holding assets/img/products/<slug>/ from process_photos.py
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
    ("purple-pvc-ring-binder.jpg", "Purple PVC 2-ring binder", "PVC ring binders"),
    ("music-folder-inside.jpg", "Inside of a blue music folder", "Music and school folders"),
    ("glove-box-wallet-inside.jpg", "Inside of a red glove box wallet", "Glove box wallets"),
    ("safety-data-sheet-binder.jpg", "Safety data sheet ring binder", "Safety data sheet binders"),
    ("pvc-satchel-flap.jpg", "Blue PVC satchel with flap", "PVC satchels"),
    ("noren-tags-sizes.jpg", "Clear PVC noren tag holders", "Noren tag holders"),
    ("polypropylene-colour-swatch-fan.jpg", "Fan of polypropylene colour swatches", "Stock colours"),
], "Made in Tingalpa", "<a href=\"/products\">See more of what we make</a>") + '\n<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>How ordering works</h2>', 1)
strip = f'''<section class="brand-strip"><div class="wrap"><span>Our brands</span>
<a href="/products"><img src="{BRAND}PU_Logo_Endorsed_v2_CAI.svg" alt="Plastics Unique, a Brisbane Plastics Company" width="175" height="80"></a>
<a href="/hospital/"><img src="{BRAND}Sov_Logo_Endorsed_v2_CAI.svg" alt="Sov Services, a Brisbane Plastics Company" width="217" height="80"></a></div></section>'''
m = m.replace('<a class="btn ghost" style="color:#fff;border-color:#fff" href="/about#ownership">What this means for you</a>\n</div></div>', '<a class="btn ghost" style="color:#fff;border-color:#fff" href="/about#ownership">What this means for you</a>\n</div></div>\n' + strip, 1)
m = m.replace('<p style="margin-top:2rem"><a href="/products">See materials and processes</a></p>', '<p style="margin-top:2rem"><a class="btn" href="/products">See all products and photos</a></p>')
pages["/"] = page("/", "Custom PVC & Polypropylene Products, Brisbane | Brisbane Plastics Company",
                  "Brisbane manufacturer of custom PVC and polypropylene products, Sov Services hospital chart folders and holders, and trade UV flatbed printing. Tingalpa.", m)

# ---- Products: catalogue index plus one page per product ----
t, d, m = v6("products.html")
m = fix(m)
m = m.replace('<li><strong>Screen printing and UV flatbed printing.</strong> Your logo and artwork printed directly onto the product.</li>',
              '<li><strong>Screen printing and <a href="/uv-printing/">UV flatbed printing</a>.</strong> Spot colours by screen, full colour and white by UV flatbed up to 1250 × 2500 mm.</li>')
mat = re.search(r'(<section class="block"><div class="wrap split">\s*<div>\s*<h2>Materials</h2>.*?</div></section>)', m, re.S).group(1)
mat = mat.replace('<section class="block">', '<section class="block alt">', 1)
pages.update(catalogue.build(mat))

# ---- About ----
t, d, m = v6("about.html")
brands = f'''<section class="block"><div class="wrap"><div class="section-head"><h2>Our brands</h2><p class="lede">Plastics Unique and Sov Services keep their names, products and customers. Both are made and supplied by Brisbane Plastics Company.</p></div>
<div class="brand-row"><a href="/products"><img src="{BRAND}PU_Logo_Endorsed_v2_CAI.svg" alt="Plastics Unique, a Brisbane Plastics Company" width="262" height="120" loading="lazy"></a>
<a href="/hospital/"><img src="{BRAND}Sov_Logo_Endorsed_v2_CAI.svg" alt="Sov Services, a Brisbane Plastics Company" width="325" height="120" loading="lazy"></a></div></div></section>'''
m = fix(m)
m = m.replace('<section class="block"><div class="wrap">\n<div class="section-head"><h2>Our directors</h2>', brands.replace('<section class="block">','<section class="block alt">',1) + '\n<section class="block"><div class="wrap">\n<div class="section-head"><h2>Our directors</h2>', 1)
pages["/about"] = page("/about", t, fix(d), m, [("/", "Home"), ("/about", "About us")])

# ---- Contact ----
t, d, m = v6("contact.html")
m = fix(m)
m = m.replace('<div class="wrap split" style="grid-template-columns:1.6fr 1fr">','<div class="wrap split contact-split">')
m = m.replace('<option>Hospital product (Sov Services)</option>', '<option>Hospital product (Sov Services)</option><option>UV flatbed printing</option>')
m = m.replace('<li><strong>Live chat</strong>', f'<li><strong>Hospital orders</strong><br>Use the <a href="/hospital/order">hospital order form</a> or email <a href="mailto:{SOV_EMAIL}">{SOV_EMAIL}</a></li>\n<li><strong>Printing</strong><br>Use the <a href="/uv-printing/#quote">print quote form</a> for UV printing jobs.</li>\n<li><strong>Live chat</strong>')
pages["/contact"] = page("/contact", t, d, m, [("/", "Home"), ("/contact", "Request a quote")])

# ---- Privacy, thanks, 404 ----
t, d, m = v6("privacy.html")
m = fix(m).replace("Live chat is provided by Tawk.to.", "Live chat is provided by Tawk.to. We measure website visits with Google Analytics, which uses cookies to count visits and see which pages are used. It does not tell us who you are.").replace("Last updated 30/09/2026", "Last updated 24/10/2026")
pages["/privacy"] = page("/privacy", t, d, m)
t, d, m = v6("thanks.html"); pages["/thanks"] = page("/thanks", t, d, fix(m), noindex=True)
t, d, m = v6("404.html"); pages["/404"] = page("/404", t, d, fix(m), noindex=True)

hp = hospital.build()
hp["/hospital/"] = hp["/hospital/"].replace('<span class="kicker">Sov Services · Hospital range</span>',
    f'<img class="hero-brand" src="{BRAND}Sov_Logo_Endorsed_v2_CAI.svg" alt="Sov Services, a Brisbane Plastics Company" width="260" height="96"><span class="kicker">Hospital range</span>', 1)
hp["/hospital/"] = hp["/hospital/"].replace('<section class="block"><div class="wrap split">\n<div>\n<h2>Why wards keep reordering</h2>',
    '''<section class="block"><div class="wrap"><div class="section-head"><h2>Also for hospitals and clinics</h2><p class="lede">From the Plastics Unique range, made in the same factory.</p></div><ul class="cards">
<li style="--tab:var(--pvc-blue)"><h3><a href="/products/x-ray-sleeves">X-ray protective sleeves</a></h3><p>Clear 0.15 mm PVC sleeves for storing and transporting X-rays, boxed in 125s.</p><a class="more" href="/products/x-ray-sleeves">Sizes and ordering</a></li>
<li style="--tab:var(--pvc-yellow)"><h3><a href="/products/tab-dividers">Medical binders and tab dividers</a></h3><p>Custom ring binders and tabs for specialists, in polypropylene, reinforced or card.</p><a class="more" href="/products/tab-dividers">Options and photos</a></li>
<li style="--tab:var(--ink)"><h3><a href="/products/room-compendiums">Hospital room compendiums</a></h3><p>Patient information compendiums for private hospitals, A4, A5 or A3.</p><a class="more" href="/products/room-compendiums">Options and photos</a></li>
</ul></div></section>
<section class="block alt"><div class="wrap split">\n<div>\n<h2>Why wards keep reordering</h2>''', 1)
pages.update(hp)
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
if CAT_PHOTOS:
    shutil.copytree(os.path.join(CAT_PHOTOS, "assets/img/products"), os.path.join(OUT, "assets/img/products"), dirs_exist_ok=True)
else:
    print("WARNING: no catalogue photo folder given; product pages will have broken images")
shutil.copytree(os.path.join(HERE, "brand"), os.path.join(OUT, "assets/img/brand"), ignore=shutil.ignore_patterns("logo.svg", "og-image.png"))
shutil.copytree(os.path.join(HERE, "email"), os.path.join(OUT, "email"))
css = open(os.path.join(V6, "assets/css/site.css"), encoding="utf-8").read() + open(os.path.join(HERE, "extra.css"), encoding="utf-8").read()
open(os.path.join(OUT, "assets/css/site.css"), "w", encoding="utf-8").write(css)
js = open(os.path.join(V6, "assets/js/site.js"), encoding="utf-8").read()
js = js.replace("var TAWK_PROPERTY_ID='', TAWK_WIDGET_ID='default';", "var TAWK_PROPERTY_ID='6adc80751b93b634803314f9', TAWK_WIDGET_ID='1k5mlbjah';")
js += '''
// Google Analytics 4. Paste the Measurement ID (G-XXXXXXX). Blank = nothing loads.
// Thank-you pages (/thanks, /hospital/thanks, /uv-printing/thanks) are the conversion events for Google Ads.
(function(){
  var GA4_ID='G-DDRCCNERYX';
  if(!GA4_ID)return;
  var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA4_ID;document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
  gtag('js',new Date());gtag('config',GA4_ID);
  // Google Ads conversion 'Request quote': print quote form thank-you page only
  if(/^\/uv-printing\/thanks(\.html)?\/?$/.test(location.pathname)){gtag('event','manual_event_REQUEST_QUOTE',{form:'print-quote'});}
})();
'''
prod_names = json.dumps({p["slug"]: p["title"] for p in CAT})
js += '''
// Contact page: ?product=<slug> from a product page fills in the product
(function(){
  var NAMES=''' + prod_names + ''';
  var s=new URLSearchParams(location.search).get('product'); if(!s||!NAMES[s])return;
  var d=document.getElementById('details'); if(d&&!d.value)d.value='Product: '+NAMES[s]+'\\n';
  var p=document.getElementById('product'); if(p){var o=document.createElement('option');o.text=NAMES[s];o.selected=true;p.add(o,1);}
})();

// Photo lightbox for product galleries
(function(){
  var links=[].slice.call(document.querySelectorAll('a.lb')); if(!links.length)return;
  var d=document.createElement('dialog'); d.className='lightbox';
  d.innerHTML='<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous photo">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-next" aria-label="Next photo">›</button>';
  document.body.appendChild(d);
  var img=d.querySelector('img'),cap=d.querySelector('figcaption'),i=0;
  function show(n){i=(n+links.length)%links.length;var a=links[i],t=a.querySelector('img');img.src=a.href;img.alt=t.alt;cap.textContent=t.alt+'  ('+(i+1)+' of '+links.length+')';}
  links.forEach(function(a,n){a.addEventListener('click',function(e){if(!d.showModal)return;e.preventDefault();show(n);d.showModal();});});
  d.querySelector('.lb-close').onclick=function(){d.close();};
  d.querySelector('.lb-prev').onclick=function(){show(i-1);};
  d.querySelector('.lb-next').onclick=function(){show(i+1);};
  d.addEventListener('click',function(e){if(e.target===d)d.close();});
  document.addEventListener('keydown',function(e){if(!d.open)return;if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});
})();
'''
open(os.path.join(OUT, "assets/js/site.js"), "w", encoding="utf-8").write(js)
shutil.copy(os.path.join(HERE, "brand/BPC_Logo_Fan_v2_CAI.svg"), os.path.join(OUT, "favicon.svg"))
shutil.copy(os.path.join(HERE, "brand/BPC_Logo_Fan_v2_CAI.svg"), os.path.join(OUT, "assets/img/logo.svg"))
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
pu = "# plasticsunique.com.au redirects. NOT ACTIVE. Activate when the domain moves (Bruce, parked 24/10/2026).\n# Swap TARGET for the live domain, paste above the existing redirects in netlify.toml, deploy, test.\n\n"
for old, new in PU_REDIRECTS.items():
    for host in ("https://plasticsunique.com.au", "https://www.plasticsunique.com.au"):
        pu += f'[[redirects]]\n  from = "{host}{old}"\n  to = "https://TARGET{new}"\n  status = 301\n  force = true\n\n'
for host in ("https://plasticsunique.com.au", "https://www.plasticsunique.com.au"):
    pu += f'[[redirects]]\n  from = "{host}/*"\n  to = "https://TARGET/"\n  status = 301\n  force = true\n\n'
open(os.path.join(OUT, "plasticsunique-redirects-PENDING.toml"), "w").write(pu)
open(os.path.join(OUT, ".gitignore"), "w").write("desktop.ini\n__pycache__/\n")
for extra in ("README.md", "sovservices-redirects-PENDING.toml"):
    shutil.copy(os.path.join(HERE, extra), OUT)
shutil.copytree(HERE, os.path.join(OUT, "_src"), ignore=shutil.ignore_patterns("__pycache__", "README.md", "sovservices-redirects-PENDING.toml"))
print(len(pages), "pages")
