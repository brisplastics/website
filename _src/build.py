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
m = m.replace("Cut, printed, welded and assembled in Tingalpa, checked and dispatched or ready for pick-up.</p>", "Cut, printed, welded and assembled in Tingalpa, checked and dispatched or ready for pick-up. Standard jobs take 10 to 15 working days from order and artwork approval. Ask about express turnaround.</p>")
assert "10 to 15 working days" in m
m = fix(m)
m = m.replace("<h1>Custom PVC and polypropylene products, made in Brisbane.</h1>", "<h1>Custom PVC and polypropylene products, and UV printing, in Brisbane.</h1>")
assert "and UV printing, in Brisbane." in m
m = m.replace('<div class="hero-sheets" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span></div>',
    '<div class="hero-photos">' + "".join(f'<img src="/assets/img/products/{f}" alt="{a}" loading="eager" decoding="async">' for f, a in [
        ("ring-binders/ring-binders-pu-01.jpg", "Range of custom printed ring binders"), ("notebook-covers/notebook-covers-pu-02.jpg", "Screen printed pocket notebook covers"),
        ("glovebox-wallets/glovebox-wallets-07.jpg", "Range of printed dealership glove box wallets"), ("sov/chart-folders-colour-range.jpg", "Patient chart folders in ten colours")]) + '</div>')
assert "hero-photos" in m
m = m.replace('<li class="t-green"><h3>Hospital products</h3><p>Patient chart holders, bed chart folders and ward stationery, supplied through our Sov Services division.</p></li>',
              '<li class="t-green"><h3><a href="/hospital/" style="color:inherit">Hospital products</a></h3><p>Patient chart folders, chart holders, clipboards and dividers from our Sov Services range. <a href="/hospital/order">Order online</a>.</p></li>')
m = m.replace('<li class="t-ink"><h3>Printing and branding</h3><p>Screen printing, flatbed UV printing and foil blocking, applied in-house so your job stays under one roof.</p></li>',
              '<li class="t-ink"><h3><a href="/uv-printing/" style="color:inherit">Printing and branding</a></h3><p>Screen printing, foil blocking and full-colour UV flatbed printing up to 1250 × 2500 mm. <a href="/uv-printing/trade">Trade printing</a> for sign shops and printers.</p></li>')
m = m.replace('<li><strong>Medical and hospital</strong><span>Chart holders and ward products through Sov Services.</span></li>',
              '<li><strong><a href="/hospital/">Medical and hospital</a></strong><span>Chart folders, holders and ward products through Sov Services.</span></li>')
def _route(href, img, alt, title, text, link):
    return (f'<li><a href="{href}"><span class="pimg"><img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async"></span>'
            f'<span class="pc-body"><strong>{title}</strong><span>{text}</span><span class="more">{link}</span></span></a></li>')
feature = ('<section class="block"><div class="wrap">\n<div class="section-head"><h2>What can we help with?</h2>'
    '<p class="lede">Five ways we work. Choose the one closest to your job.</p></div>\n<ul class="pgrid routes">'
    + _route("/products", "/assets/img/products/safety-data-sheet-binder.jpg", "Printed safety data sheet ring binder", "Custom printed products",
             "Your logo and artwork on folders, binders, wallets, satchels, tags and covers, by screen print, foil blocking or full-colour UV.", "See printed products")
    + _route("/products", "/assets/img/products/pvc-satchel-flap.jpg", "Blue welded PVC satchel with flap", "Made to your size",
             "Custom-size PVC and polypropylene products, RF welded, die cut and creased in our factory to fit exactly what you need.", "See what we make")
    + _route("/products/noren-tags", "/assets/img/products/noren-tags-sizes.jpg", "Clear PVC noren tags in three sizes", "Standard products",
             "Ready-made lines in standard sizes: noren tags, chart folders, tally book refills, TAB wallets and X-ray sleeves.", "See standard products")
    + _route("/hospital/", "/assets/img/products/sov/chart-folders-colour-range-t.jpg", "Patient chart folders in ten colours", "Hospital range",
             "Sov Services patient chart folders, chart holders, clipboards and dividers, with the same item codes.", "Order or reorder")
    + _route("/uv-printing/", "/assets/img/products/printed-polypropylene-sign.jpg", "Printed polypropylene venue sign", "UV Printing",
             "Full colour and white ink direct onto rigid material from heavy card up to 50.8 mm thick and 1250 × 2500 mm: acrylic, foamed PVC, polycarbonate, ACM, aluminium, wood, MDF, glass, tile and corflute.", "Printing services")
    + '</ul>\n</div></section>\n')
m = m.replace('<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>What we make</h2>', feature + '<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>What we make</h2>', 1)
assert 'What can we help with?' in m
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
# Testimonials published on plasticsunique.com.au (read 27/10/2026). Spelling corrected ("consistant").
TESTIMONIALS = [
    ("Highly recommended. The Plastics Unique team are fast, friendly, flexible and affordable.", "Sci-Fleet Toyota", ""),
    ("Quality products every time and great service. I would highly recommend Plastics Unique.", "Lauren Logan", "Centre Manager, Snap Printing"),
    ("We have been using Plastics Unique for 15 years. Consistent quality and great service you can rely on.", "Mark Emery", "Ramsay Health"),
]
quotes = "".join(f'<figure class="quote-card"><blockquote><p>{esc(q)}</p></blockquote><figcaption><strong>{esc(n)}</strong>{("<span>" + esc(r) + "</span>") if r else ""}</figcaption></figure>' for q, n, r in TESTIMONIALS)
m = m.replace('<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>How ordering works</h2>',
    '<section class="block"><div class="wrap"><div class="section-head"><h2>What our customers say</h2><p class="lede">From Plastics Unique customers. <a href="' + GBP_REVIEWS + '" rel="noopener">Read our Google reviews</a>.</p></div><div class="quotes">' + quotes + '</div></div></section>\n<section class="block alt"><div class="wrap">\n<div class="section-head"><h2>How ordering works</h2>', 1)
assert "What our customers say" in m
pages["/"] = page("/", "Custom PVC & Polypropylene Products Brisbane | Plastics Unique & Sov Services",
                  "Brisbane Plastics Company, home of Plastics Unique and Sov Services: custom PVC and polypropylene products, hospital chart folders and holders, and UV flatbed printing. Tingalpa.", m)

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
m = m.replace('<h2>Part of FormFill Group</h2>\n<p>Brisbane Plastics Company is part of <a href="https://www.formfill.com.au/" rel="noopener">FormFill Group</a>, an engineer-led group that buys and improves South East Queensland plastics manufacturers.</p>', '<h2>Owner-operated</h2>\n<p>Brisbane Plastics Company is run by its directors from the Tingalpa factory, bringing engineering, controls and commercial experience to a business that has made plastic products in Brisbane for 27 years.</p>')
d = d.replace("Brisbane Plastics Company, part of FormFill Group, owns", "Brisbane Plastics Company owns")
assert "FormFill" not in m and "FormFill" not in d
brands = f'''<section class="block"><div class="wrap"><div class="section-head"><h2>Our brands</h2><p class="lede">Plastics Unique and Sov Services keep their names, products and customers. Both are made and supplied by Brisbane Plastics Company.</p></div>
<div class="brand-row"><a href="/products"><img src="{BRAND}PU_Logo_Endorsed_v2_CAI.svg" alt="Plastics Unique, a Brisbane Plastics Company" width="262" height="120" loading="lazy"></a>
<a href="/hospital/"><img src="{BRAND}Sov_Logo_Endorsed_v2_CAI.svg" alt="Sov Services, a Brisbane Plastics Company" width="325" height="120" loading="lazy"></a></div></div></section>'''
m = fix(m)
m = m.replace('<p class="lede">Brisbane Plastics Company is a Queensland-owned manufacturer. From 26 October 2026 we own and run Plastics Unique and Sov Services, a Brisbane plastics fabricator trusted by local businesses for 27 years.</p>',
  '<p class="lede">Brisbane Plastics Company is a Queensland-owned plastics printing and stationery manufacturer. From 26 October 2026 the business incorporates Plastics Unique and Sov Services, two service lines trusted by local businesses for 27 years.</p>')
m = m.replace("""<p>Bruce spent 20 years building a project management consultancy, LogiKal Projects, growing it to more than 100 consultants across Australia, Asia and the UK before selling it in 2022. His work spans major infrastructure and resources projects and managing complex programmes.</p>
<p>At Brisbane Plastics Company he leads strategy, systems and investment, and finds the commercial opportunity inside the operational challenge.</p>""",
  """<p>Brisbane Plastics Company is Bruce's third business venture. As Director he leads strategy, systems and investment: pricing and quoting, finance, and the systems that connect customers, the office and the factory.</p>""")
assert "third business venture" in m and "stationery manufacturer" in m
m = m.replace("<li><strong>Owner-operated.</strong> The founders run the businesses themselves, alongside their investors.</li>", "<li><strong>Owner-operated.</strong> Our directors run the business from the Tingalpa factory.</li>")
m = m.replace("<li><strong>Engineering depth.</strong> Controls, automation and IoT experience applied inside our own factories.</li>", "<li><strong>Engineering depth.</strong> Controls, automation and systems experience applied on our factory floor.</li>")
assert "inside our own factories" not in m
m = m.replace('<section class="block"><div class="wrap">\n<div class="section-head"><h2>Our directors</h2>', brands.replace('<section class="block">','<section class="block alt">',1) + '\n<section class="block"><div class="wrap">\n<div class="section-head"><h2>Our directors</h2>', 1)
pages["/about"] = page("/about", t, fix(d), m, [("/", "Home"), ("/about", "About us")])

# ---- Contact ----
t, d, m = v6("contact.html")
m = fix(m)
m = m.replace('<div class="wrap split" style="grid-template-columns:1.6fr 1fr">','<div class="wrap split contact-split">')
import re as _re, forms
m = _re.sub(r'<form class="quote" name="quote-request".*?</form>', lambda _m: forms.contact_form(), m, count=1, flags=_re.S)
assert 'past_customer' in m
m = m.replace('<li><strong>Factory</strong><br>45a Millennium Place, Tingalpa QLD 4173</li>', f'<li><strong>Factory and collection</strong><br><a href="{GBP_MAP}" rel="noopener">{ADDRESS}</a><br>{HOURS_TEXT}</li>\n<li><strong>Google reviews</strong><br><a href="{GBP_REVIEWS}" rel="noopener">Read our reviews</a> or <a href="{GBP_WRITE}" rel="noopener">leave one</a></li>')
assert 'Factory and collection' in m
m = m.replace('<li><strong>Live chat</strong>', f'<li><strong>Hospital orders</strong><br>Use the <a href="/hospital/order">hospital order form</a> or email <a href="mailto:{SOV_EMAIL}">{SOV_EMAIL}</a></li>\n<li><strong>Printing</strong><br>Use the <a href="/uv-printing/#quote">print quote form</a> for UV printing jobs.</li>\n<li><strong>Live chat</strong>')
pages["/contact"] = page("/contact", t, d, m, [("/", "Home"), ("/contact", "Request a quote")])

# ---- Privacy, thanks, 404 ----
t, d, m = v6("privacy.html")
m = fix(m).replace("Live chat is provided by Tawk.to.", "Live chat is provided by Tawk.to. We measure website visits with Google Analytics, which uses cookies to count visits and see which pages are used. We use these reports in aggregate and do not use them to identify individual visitors.").replace("Last updated 30/09/2026", "Last updated 26/10/2026").replace("We do not sell your information", "Our forms record how you reached the site (for example a Google Ads click or an email campaign) so we can see which advertising works. Google Ads uses cookies to count enquiries that come from an ad. If you tick the news box on a form, we add your email to our mailing list and send occasional product news and offers; every email has an unsubscribe link. We do not sell your information")
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
js = js.replace("if(!/\\.(pdf|jpe?g)$/i.test(file.name)){err.textContent='Upload a PDF or JPG file.'", "if(!/\\.(pdf|jpe?g|png|ai|eps|svg)$/i.test(file.name)){err.textContent='Upload a PDF, AI, EPS, SVG, PNG or JPG file.'")
assert 'png|ai|eps' in js
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
import forms
js += '''
// Lead source: remember the first page, referrer, UTM tags and Google Ads click ID for this visit and add them to every form
(function(){
  var K='bpc_src', src=null;
  try{src=JSON.parse(sessionStorage.getItem(K)||'null');}catch(e){}
  if(!src){var q=new URLSearchParams(location.search);
    src={landing_page:location.pathname+location.search,referrer:document.referrer||'',utm_source:q.get('utm_source')||'',utm_medium:q.get('utm_medium')||'',
         utm_campaign:q.get('utm_campaign')||'',gclid:q.get('gclid')||'',came_from:q.get('from')||''};
    try{sessionStorage.setItem(K,JSON.stringify(src));}catch(e){}}
  [].forEach.call(document.querySelectorAll('form[data-netlify] input[type=hidden]'),function(i){if(src[i.name]!==undefined&&!i.value)i.value=src[i.name];});
  window.BPC_SRC=src;
})();

// Visitors redirected from plasticsunique.com.au or sovservices.net.au see a one-line welcome
(function(){
  var f=(window.BPC_SRC||{}).came_from; if(f!=='pu'&&f!=='sov')return;
  try{if(sessionStorage.getItem('bpc_welcome_closed'))return;}catch(e){}
  var name=f==='pu'?'Plastics Unique':'Sov Services', link=f==='pu'?'/products':'/hospital/';
  var b=document.createElement('div'); b.className='welcome-bar'; b.setAttribute('role','status');
  b.innerHTML='<div class="wrap"><p><strong>'+name+' has a new website.</strong> Same team, same Tingalpa factory, same products, item codes and phone numbers. <a href="'+link+'">Find your product</a></p><button type="button" aria-label="Close">×</button></div>';
  var m=document.getElementById('main'); (m||document.body).insertBefore(b,(m||document.body).firstChild);
  b.querySelector('button').onclick=function(){b.remove();try{sessionStorage.setItem('bpc_welcome_closed','1');}catch(e){}};
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
js += "\n" + open(os.path.join(HERE, "quote.js"), encoding="utf-8").read().replace("__STANDARD__", json.dumps(forms.STANDARD, ensure_ascii=False)).replace("__HINTS__", json.dumps(forms.GROUP_HINTS)).replace("__GENERIC__", json.dumps(forms.GENERIC_HINT))
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

# ---- llms.txt: plain-language map of the site for AI assistants and answer engines ----
import re as _re2, html as _h
def _meta(h):
    t=_re2.search(r"<title>(.*?)</title>",h,_re2.S); d=_re2.search(r'name="description" content="(.*?)"',h)
    return _h.unescape(t.group(1)) if t else "", _h.unescape(d.group(1)) if d else ""
SECTIONS=[("Products (Plastics Unique)", lambda p: p=="/products" or p.startswith("/products/")),
          ("Hospital range (Sov Services)", lambda p: p.startswith("/hospital/") and p!="/hospital/order"),
          ("UV flatbed printing", lambda p: p.startswith("/uv-printing/")),
          ("Company and ordering", lambda p: p in ("/", "/about", "/contact", "/hospital/order"))]
L=["# Brisbane Plastics Company", "",
   "> Brisbane Plastics Company Pty Ltd (ABN " + ABN + ") makes custom PVC and polypropylene products in Tingalpa, Brisbane, Queensland, Australia. "
   "It owns and runs Plastics Unique (custom folders, binders, wallets, satchels, tags and school products) and Sov Services (patient chart folders, chart holders, clipboards and dividers for hospitals since 1994), "
   "and offers UV flatbed printing on rigid sheet up to 1250 x 2500 mm and 50.8 mm thick, with white ink.", "",
   "- Address: 45a Millennium Place, Tingalpa QLD 4173", "- Phone: (07) 3396 3744 or 1300 744 104",
   "- Quotes: " + SALES + "; hospital orders: " + SOV_EMAIL, "- Delivers Australia-wide; all products are made to order in the Tingalpa factory.", "- Turnaround: 10 to 15 working days from order and artwork approval for standard jobs; ask about express turnaround.", ""]
for name, test in SECTIONS:
    L.append("## " + name); L.append("")
    for p in locs:
        if test(p):
            t, d = _meta(pages[p]); L.append(f"- [{t.split(' | ')[0]}]({url(p)}): {d}")
    L.append("")
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))
nt=open(os.path.join(V6, "netlify.toml")).read()
nt+="\n# Glove box holders discontinued 26/10/2026 (Elbe)\n[[redirects]]\n  from = \"/hospital/glove-box-holders\"\n  to = \"/hospital/\"\n  status = 301\n"
nt+="\n# Keep the page generator source private\n[[redirects]]\n  from = \"/_src/*\"\n  to = \"/404\"\n  status = 404\n  force = true\n"
open(os.path.join(OUT, "netlify.toml"),"w").write(nt)
pu = "# plasticsunique.com.au redirects. NOT ACTIVE. Activate when the domain moves (Bruce, parked 24/10/2026).\n# Swap TARGET for the live domain, paste above the existing redirects in netlify.toml, deploy, test.\n\n"
for old, new in PU_REDIRECTS.items():
    for host in ("https://plasticsunique.com.au", "https://www.plasticsunique.com.au"):
        pu += f'[[redirects]]\n  from = "{host}{old}"\n  to = "https://TARGET{new.split('#')[0]}?from=pu{('#'+new.split('#')[1]) if '#' in new else ''}"\n  status = 301\n  force = true\n\n'
for host in ("https://plasticsunique.com.au", "https://www.plasticsunique.com.au"):
    pu += f'[[redirects]]\n  from = "{host}/*"\n  to = "https://TARGET/?from=pu"\n  status = 301\n  force = true\n\n'
open(os.path.join(OUT, "plasticsunique-redirects-PENDING.toml"), "w").write(pu)
open(os.path.join(OUT, ".gitignore"), "w").write("desktop.ini\n__pycache__/\n")
for extra in ("README.md", "sovservices-redirects-PENDING.toml"):
    shutil.copy(os.path.join(HERE, extra), OUT)
shutil.copytree(HERE, os.path.join(OUT, "_src"), ignore=shutil.ignore_patterns("__pycache__", "README.md", "sovservices-redirects-PENDING.toml"))
print(len(pages), "pages")
