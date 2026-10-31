"""Product catalogue pages: /products (index) and /products/<slug>."""
import os, json
from shell import *
from catalogue_data import PRODUCTS, EXTERNAL_RELATED, GROUP_ORDER, COVERS

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(HERE, "photo_manifest.json")))
# Photos pulled from the site after review (Elbe, 31/10/2026): reflection on the certificate pocket, fake checkerboard background on the bean lids
EXCLUDE = {"certificate-pockets-06", "bean-lids-pu-02"}
MANIFEST = {k: [x for x in v if x.get("file") not in EXCLUDE] for k, v in MANIFEST.items()}
for _s, _src in COVERS.items():  # move the cover photo to the front
    _l = MANIFEST.get(_s, [])
    if _l and "-pu-" in _l[0]["file"]: continue  # PU studio photo leads
    _i = next((i for i, x in enumerate(_l) if x["source"] == _src), None)
    if _i: _l.insert(0, _l.pop(_i))
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

def img_url(slug, base, thumb=False):
    return f"/assets/img/products/{slug}/{base}{'-t' if thumb else ''}.jpg"

def related_links(p):
    out = []
    for r in p["related"]:
        if r in BY_SLUG:
            out.append((f"/products/{r}", BY_SLUG[r]["title"]))
        elif r in EXTERNAL_RELATED:
            out.append(EXTERNAL_RELATED[r])
    return '<ul class="related">' + "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in out) + "</ul>"

def product_gallery(p):
    photos = MANIFEST.get(p["slug"], [])
    if not photos:
        return ""
    SHOW = 12
    figs = "".join(
        f'<figure{" class=\"more-photo\" hidden" if i >= SHOW else ""}><a class="lb" href="{img_url(p["slug"], x["file"])}" data-w="{x["w"]}" data-h="{x["h"]}">'
        f'<img src="{img_url(p["slug"], x["file"], True)}" alt="{esc(x["alt"])}" width="{x["tw"]}" height="{x["th"]}" loading="lazy" decoding="async"></a>'
        f'<figcaption>{esc(x["alt"])}</figcaption></figure>' for i, x in enumerate(photos))
    more = (f'<p style="margin-top:1.2rem"><button type="button" class="btn ghost show-photos">Show all {len(photos)} photos</button></p>' if len(photos) > SHOW else "")
    return (f'<section class="block alt"><div class="wrap"><div class="section-head"><h2>Examples from our factory</h2>'
            f'<p class="lede">Work made in our Tingalpa factory, including jobs for customers. Select a photo to enlarge it.</p></div>'
            f'<div class="gallery">{figs}</div>{more}</div></section>')

def product_page(p):
    path = f"/products/{p['slug']}"
    cr = [("/", "Home"), ("/products", "Products"), (path, p["title"])]
    quote = f"/contact?product={p['slug']}"
    main = hero(cr, esc(p["title"]), p["intro"], kicker=esc(p["group"]),
                buttons=[(quote, "Request a quote"), ("/contact?type=repeat", "Reorder a past job")])
    rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{b}</td></tr>' for a, b in p["facts"] + [("Turnaround", LEAD)])
    main += f'''<section class="block" style="padding-top:1rem"><div class="wrap two-col">
<div><div class="table-wrap"><table class="spec"><caption class="hidden">{esc(p["title"])} options</caption><tbody>{rows}</tbody></table></div></div>
<div><h2 style="font-size:1.3rem">Made to order in Tingalpa</h2>
<ul class="ticks"><li>Australian made in our Brisbane factory</li><li>Your size, material, colour and print</li><li>Proof approved before anything is made</li><li>Short runs and repeat orders welcome</li><li>10 to 15 working day turnaround, express available</li></ul>
<p class="btn-row" style="margin-top:1rem"><a class="btn" href="{quote}">Request a quote</a><button type="button" class="btn ghost add-quote" data-key="pu:{p['slug']}" data-name="{esc(p['title'])}">Add to quote request</button></p></div>
</div></section>'''
    main += product_gallery(p)
    SIGN_CALLOUT = {"Schools and education": ("/uv-printing/school-signs", "Need school signs or honour boards too? We print them in the same factory."),
                    "Hospitality and healthcare": ("/uv-printing/hospital-signs", "Need ward, room or wayfinding signs too? We print them in the same factory."),
                    "Tags and cards": ("/uv-printing/safety-industrial-signs", "Need safety signs or machine labels too? We print them in the same factory.")}
    if p["group"] in SIGN_CALLOUT:
        h_, t_ = SIGN_CALLOUT[p["group"]]
        main += f'<section class="block" style="padding-bottom:0"><div class="wrap"><div class="notice"><p>{esc(t_)} <a href="{h_}">See printed signs</a></p></div></div></section>'
    main += f'''<section class="block"><div class="wrap"><h2 style="font-size:1.3rem">Related products</h2>{related_links(p)}</div></section>'''
    main += cta()
    if len(p["intro"]) <= 155:
        desc = p["intro"]
    else:
        cut = p["intro"][:150]
        end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
        desc = (cut[:end + 1] if end > 60 else cut.rsplit(" ", 1)[0].rstrip(",;:-") + ".") + " Made in Brisbane."
    photos = MANIFEST.get(p["slug"], [])
    schema = {"@context": "https://schema.org", "@type": "Product", "name": p["title"], "description": p["intro"],
              "brand": {"@type": "Brand", "name": "Plastics Unique"}, "manufacturer": {"@id": SITE + "/#business"},
              "url": url(path)}
    if photos:
        schema["image"] = [url(img_url(p["slug"], x["file"])) for x in photos[:5]]
    return path, page(path, f"{p['title']} | Custom Made in Brisbane | Brisbane Plastics", desc, main, cr, [schema])

def index_page(materials_html):
    path = "/products"
    cr = [("/", "Home"), ("/products", "Products")]
    main = hero(cr, "Products we make",
                "Every Plastics Unique and Sov Services product, made to order in our Tingalpa factory, with a 10 to 15 working day standard turnaround and express available. Choose a product to see options and photos of work we have made, then send us your size, material, quantity and print.",
                buttons=[("/contact", "Request a quote"), ("/hospital/", "Hospital range (Sov Services)")])
    def gid(g): return "g-" + "".join(ch if ch.isalnum() else "-" for ch in g.lower()).strip("-")
    jump = ('<section class="block finder"><div class="wrap"><div class="finder-row">'
            '<label for="prod-search" class="label">Find a product or item code</label>'
            '<input id="prod-search" type="search" placeholder="e.g. music folder, noren, SS-PCU-034" autocomplete="off">'
            '<p class="form-note" id="prod-count" aria-live="polite"></p></div>'
            '<nav class="jump" aria-label="Product groups">' + "".join(f'<a href="#{gid(g)}">{esc(g)}</a>' for g in GROUP_ORDER)
            + '<a href="#g-hospital">Hospital range</a></nav></div></section>')
    groups = jump
    for g in GROUP_ORDER:
        cards = ""
        for p in [x for x in PRODUCTS if x["group"] == g]:
            ph = MANIFEST.get(p["slug"], [])
            img = (f'<img src="{img_url(p["slug"], ph[0]["file"], True)}" alt="{esc(ph[0]["alt"])}" width="{ph[0]["tw"]}" height="{ph[0]["th"]}" loading="lazy" decoding="async">'
                   if ph else '<span class="noimg" aria-hidden="true"></span>')
            n = f'<span class="count">{len(ph)} photos</span>' if ph else ""
            cards += f'<li><a href="/products/{p["slug"]}">{img}<span class="pc-body"><strong>{esc(p["title"])}</strong><span>{esc(p["card"])}</span>{n}</span></a></li>'
        groups += f'<section class="block{" alt" if GROUP_ORDER.index(g) % 2 == 0 else ""} pgroup" id="{gid(g)}"><div class="wrap"><h2>{esc(g)}</h2><ul class="pcards">{cards}</ul></div></section>'
    # Sov range card group
    from hospital import sov_link_tiles
    groups += ('<section class="block pgroup" id="g-hospital"><div class="wrap"><h2>Hospital range (Sov Services)</h2>'
               '<p class="lede">Patient chart folders, holders, clipboards and dividers. Prices exclude GST. <a href="/hospital/">See the hospital range</a> or <a href="/hospital/order">order online</a>.</p>'
               + sov_link_tiles() + '</div></section>')
    main += groups + materials_html + cta()
    schema = {"@context": "https://schema.org", "@type": "ItemList", "name": "Products made by Brisbane Plastics Company",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f"/products/{p['slug']}"), "name": p["title"]}
                                  for i, p in enumerate(PRODUCTS)]}
    return path, page(path, "Custom PVC & Polypropylene Products | Brisbane Plastics Company",
                      "Ring binders, notebook covers, glove box wallets, satchels, tags, compendiums, school and music folders, all custom made in Brisbane. Photos and options for every product.",
                      main, cr, [schema])

def build(materials_html):
    pages = {}
    path, html_ = index_page(materials_html); pages[path] = html_
    for p in PRODUCTS:
        path, html_ = product_page(p); pages[path] = html_
    return pages
