"""Hospital section: Sov Services range, rebuilt from sovservices.net.au (read 24/10/2026)."""
from shell import *
from forms import TRACKING, ART_ACCEPT

FOLDER_COLOURS = [  # (name, code, swatch)
    ("Oxford Blue", "01", "#1F3A68"), ("Red", "02", "#D7322E"), ("Yellow", "03", "#F3C623"),
    ("Purple", "04", "#6B3FA0"), ("Navy", "06", "#16264A"), ("Grey", "07", "#8C939B"),
    ("Orange", "09", "#EF7A1A"), ("Pink", "10", "#EC7FB0"), ("Apple Green", "11", "#6DBE45"),
    ("Sky Blue", "13", "#5FB4E6"),
]

BLACK_NOTE = "Black is available on request."
FOLDER_COLOURS_TEXT = "10 colours: Oxford Blue, Red, Yellow, Purple, Navy, Grey, Orange, Pink, Apple Green, Sky Blue. " + BLACK_NOTE

ORDER_CODES = [
    ("Chart folders: unprinted", ["SS-PCU-13 (30 mm spine)", "SS-PCU-14 (40 mm spine)", "SS-PCU-15 (55 mm spine)", "SS-PCU-16 (68 mm spine)"]),
    ("Chart folders: ward and bed print", ["SS-PCU-03 (30 mm spine)", "SS-PCU-04 (40 mm spine)", "SS-PCU-05 (55 mm spine)", "SS-PCU-06 (68 mm spine)"]),
    ("Hanging chart folders: unprinted", ["SS-PCU-13 H (30 mm spine)", "SS-PCU-14 H (40 mm spine)"]),
    ("Hanging chart folders: ward and bed print", ["SS-PCU-03 H (30 mm spine)", "SS-PCU-04 H (40 mm spine)"]),
    ("Custom printed folders", ["Custom printed chart folder", "Custom printed hanging folder"]),
    ("Chart holders and clipboards", ["SS-PCU-033 A3 chart holder, horizontal", "SS-PCU-034 A4 chart holder, vertical", "SS-PCU-038 A4 wall-mounted holder, horizontal", "SS-PCU-039 A4 wall-mounted holder, vertical", "SS-CCB-010 A4 patient clipboard, vertical", "SS-CCB-011 A4 patient clipboard, horizontal", "SS-CCB-012 A4 patient clipboard, horizontal with D-rings", "SS-CCB-015 A3 patient clipboard, horizontal"]),
    ("Dividers", ["SS-PCU-043 5-tab divider, blank", "SS-PCU-045 5-tab divider, printed", "Custom tab dividers (1 to 10 tabs)"]),
]

import json as _json, os as _os
_SIZES = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "sov_photo_sizes.json")))

# Sov range per sovservices.net.au/products (read 25/10/2026), corrected after Elbe's review (26/10/2026):
# glove box holders and basket discontinued; hanging folders 30 and 40 mm only; custom dividers from $28.
# Prices ex GST. Folder prices are not published.
P_FOLD, P_HOLD, P_DIV = "/hospital/patient-chart-folders", "/hospital/patient-chart-holders", "/hospital/chart-dividers"
SOV_GROUPS = [(P_HOLD, "Patient clipboards and chart holders"), (P_FOLD, "Patient chart folders and hanging folders"), (P_DIV, "Chart dividers")]
ASK = "Price on request"
def P(a, page, name, code, price, colours, spec, photo, alt):
    return dict(id=a, page=page, name=name, code=code, price=price, colours=colours, spec=spec, photo=photo, alt=alt)
GLOSS = "Black or white gloss"
SOV_PRODUCTS = [
    P("a3-chart-holder", P_HOLD, "A3 patient chart holder, horizontal", "SS-PCU-033", "From $38 ex GST", GLOSS, "350 W × 300 H × 45 D mm, 50 mm rollover for the bed rail.", "a3-chart-holder-horizontal", "Black gloss A3 patient chart holder with rollover top"),
    P("a4-chart-holder", P_HOLD, "A4 patient chart holder, vertical", "SS-PCU-034", "From $38 ex GST", GLOSS, "280 W × 370 H × 50 D mm, 50 mm rollover for the bed rail.", "a4-chart-holder-vertical", "Black gloss A4 vertical patient chart holder with rollover top"),
    P("a4-wall-holder", P_HOLD, "A4 patient chart holder, wall mounted", "SS-PCU-038 / 039", "From $38 ex GST", GLOSS, "SS-PCU-038 horizontal, SS-PCU-039 vertical. 255 W × 315 H × 110 D mm.", "a4-chart-holder-wall-mounted", "White and black wall-mounted A4 patient chart holders"),
    P("a4-clipboard", P_HOLD, "A4 patient clipboard, vertical or horizontal", "SS-CCB-010 / 011 / 012", "From $29.50 ex GST", "White", "SS-CCB-010 vertical, SS-CCB-011 horizontal, SS-CCB-012 horizontal with 2 D-ring clips. Impact-resistant ABS, rollover top for the rail. 230 W × 360 H × 50 D mm.", "a4-patient-clipboard", "White ABS A4 patient clipboard with rollover top and clip"),
    P("a3-clipboard", P_HOLD, "A3 patient clipboard, horizontal", "SS-CCB-015", "From $37.80 ex GST", "White", "Impact-resistant ABS, rollover top for the rail. Clipboard clip or 2 D-ring clips. 450 W × 360 H × 50 D mm.", "a3-patient-clipboard", "White ABS A3 horizontal patient clipboard with rollover top and clip"),
    P("folder-colours", P_FOLD, "Patient chart folders, ten colours", "Colour codes 01 to 13", ASK, "10 stock colours. " + BLACK_NOTE, "Print in white or black. See the full colour list below.", "chart-folders-colour-range", "Ten colours of polypropylene patient chart folders, some printed with ward and bed"),
    P("folder-unprinted", P_FOLD, "Patient chart folder, unprinted", "SS-PCU-13 to 16", ASK, "10 colours. " + BLACK_NOTE, "Polypropylene. 30, 40, 55 and 68 mm spines.", "chart-folder-unprinted", "Open green unprinted patient chart folder with clip and 2-ring fitting"),
    P("folder-ward-bed", P_FOLD, "Patient chart folder, ward and bed print", "SS-PCU-03 to 06", ASK, "10 colours. " + BLACK_NOTE, "Ward and bed printed on the front and spine. Polypropylene. 30, 40, 55 and 68 mm spines.", "chart-folder-ward-bed", "Green patient chart folder printed with ward and bed on the front and spine"),
    P("folder-custom", P_FOLD, "Custom printed patient chart folder", "Custom", ASK, "10 colours, print in any colour. " + BLACK_NOTE, "Your ward name and bed number on the front and spine. Artwork set-up charge applies.", "custom-printed-chart-folder", "Red and green chart folders custom printed Admissions and Day Stay Unit"),
    P("folder-hanging", P_FOLD, "Patient chart hanging folder, unprinted", "SS-PCU-13 H / 14 H", ASK, "10 colours. " + BLACK_NOTE, "Polypropylene. 30 and 40 mm spines.", "hanging-chart-folder", "Open red hanging patient chart folder with clip, rings and hanging strip"),
    P("folder-hanging-printed", P_FOLD, "Hanging folder, ward and bed or custom print", "SS-PCU-03 H / 04 H, custom HC", ASK, "10 colours. " + BLACK_NOTE, "Ward and bed or custom print on the front and spine, landscape on the front. 30 and 40 mm spines.", "hanging-chart-folder-printed", "Blue hanging chart folder printed with bed number 34A"),
    P("dividers-blank", P_DIV, "5-tab dividers, blank", "SS-PCU-043", "From $12 ex GST per set", "", "Five blank tabs. No minimum order. Suits A4 2-ring binders.", "dividers-5-tab-blank", "Set of blank coloured 5-tab dividers"),
    P("dividers-printed", P_DIV, "5-tab dividers, printed", "SS-PCU-045", "From $13.90 ex GST per set", "", "Tabs printed Observations, Medications, Fluids, Care Plans, Other. No minimum order. Suits A4 2-ring binders.", "dividers-5-tab-printed", "Set of 5-tab dividers printed Observations, Medications, Fluids, Care Plans and Other"),
    P("dividers-custom", P_DIV, "Custom tab dividers, 1 to 10 tabs", "Custom", "From $28 ex GST per set", "", "Your wording on 1 to 10 tabs. 50 sets minimum. Suits A4 2-ring binders.", "dividers-5-tab-printed", "Printed coloured tab dividers"),
]

# Product tile id -> the order-form line it preselects (/hospital/order?item=<id>). Colour-chart card has no line.
ORDER_OPT = {
    "a3-chart-holder": "SS-PCU-033 A3 chart holder, horizontal", "a4-chart-holder": "SS-PCU-034 A4 chart holder, vertical",
    "a4-wall-holder": "SS-PCU-038 A4 wall-mounted holder, horizontal", "a4-clipboard": "SS-CCB-010 A4 patient clipboard, vertical",
    "a3-clipboard": "SS-CCB-015 A3 patient clipboard, horizontal", "folder-unprinted": "SS-PCU-13 (30 mm spine)",
    "folder-ward-bed": "SS-PCU-03 (30 mm spine)", "folder-custom": "Custom printed chart folder", "folder-hanging": "SS-PCU-13 H (30 mm spine)",
    "folder-hanging-printed": "SS-PCU-03 H (30 mm spine)", "dividers-blank": "SS-PCU-043 5-tab divider, blank",
    "dividers-printed": "SS-PCU-045 5-tab divider, printed", "dividers-custom": "Custom tab dividers (1 to 10 tabs)",
}

def _img(photo, alt):
    w, h, tw, th = _SIZES[photo]
    return f'<img src="/assets/img/products/sov/{photo}-t.jpg" alt="{esc(alt)}" width="{tw}" height="{th}" loading="lazy" decoding="async">'

def _body(p, spec=False):
    out = f'<span class="sku">{esc(p["code"])}</span><strong>{esc(p["name"])}</strong><span class="price">{esc(p["price"])}</span>'
    if p["colours"]:
        out += f'<span class="colours">Colours: {esc(p["colours"])}</span>'
    if spec:
        out += f'<span>{esc(p["spec"])}</span>'
    return out

def quote_btn(key, name):
    return f'<button type="button" class="add-quote" data-key="{esc(key)}" data-name="{esc(name)}">Add to quote request</button>'

def sov_link_tiles(items=None):
    """Card links (hub and /products): each opens its product on the group page."""
    items = items if items is not None else SOV_PRODUCTS
    return '<ul class="pgrid">' + "".join(
        f'<li><a href="{p["page"]}#{p["id"]}"><span class="pimg">{_img(p["photo"], p["alt"])}</span><span class="pc-body">{_body(p)}</span></a></li>'
        for p in items) + "</ul>"

def sov_product_tiles(page_path):
    """Product tiles on a group page: photo opens the lightbox; tile is the anchor target."""
    out = ""
    for p in SOV_PRODUCTS:
        if p["page"] != page_path: continue
        w, h, tw, th = _SIZES[p["photo"]]
        out += (f'<li id="{p["id"]}"><a class="lb pimg" href="/assets/img/products/sov/{p["photo"]}.jpg" data-w="{w}" data-h="{h}">{_img(p["photo"], p["alt"])}</a>'
                f'<div class="pc-body">{_body(p, spec=True)}<div class="tile-actions">{quote_btn("sov:" + p["id"], p["code"] + " " + p["name"])}{('<a class="more" href="/hospital/order?item=' + p["id"] + '">Order</a>') if p["id"] in ORDER_OPT else ''}</div></div></li>')
    return (f'<section class="block"><div class="wrap"><div class="section-head"><h2>Products and prices</h2>'
            f'<p class="lede">Prices exclude GST. Select a photo to enlarge it.</p></div><ul class="pgrid detail">{out}</ul></div></section>')

def sov_schema():
    items = []
    for i, p in enumerate(SOV_PRODUCTS):
        prod = {"@type": "Product", "name": p["name"], "sku": p["code"], "description": p["spec"], "url": url(f'{p["page"]}#{p["id"]}'),
                "image": url(f'/assets/img/products/sov/{p["photo"]}.jpg'), "brand": {"@type": "Brand", "name": "Sov Services"}}
        if p["price"].startswith("From $"):
            amt = p["price"].split("$")[1].split(" ")[0]
            prod["offers"] = {"@type": "Offer", "priceCurrency": "AUD", "price": amt,
                              "priceSpecification": {"@type": "UnitPriceSpecification", "price": amt, "priceCurrency": "AUD", "valueAddedTaxIncluded": False},
                              "availability": "https://schema.org/InStock", "seller": {"@id": SITE + "/#business"}}
        items.append({"@type": "ListItem", "position": i + 1, "item": prod})
    return {"@context": "https://schema.org", "@type": "ItemList", "name": "Sov Services hospital range", "itemListElement": items}

HUB = "/hospital/"
C_HUB = [("/", "Home"), (HUB, "Hospital products")]

def swatches():
    return '<ul class="swatches">' + "".join(
        f'<li><i style="background:{c}"></i>{n} <span class="code">{code}</span></li>' for n, code, c in FOLDER_COLOURS) + "</ul>"

def order_cta(extra=""):
    return f'''<section class="cta"><div class="wrap">
<h2>Ordering for your ward?</h2>
<div class="btn-row" style="margin:0"><a class="btn" href="/hospital/order">Order or reorder online</a><a class="btn ghost" href="mailto:{SOV_EMAIL}">Email {SOV_EMAIL}</a><a class="btn ghost" href="tel:1300744104">Call 1300 744 104</a></div>
</div></section>'''

def related(current):
    links = [("/hospital/patient-chart-folders", "Patient chart folders"), ("/hospital/patient-chart-holders", "Chart holders and clipboards"),
             ("/hospital/chart-dividers", "Chart dividers"), ("/hospital/order", "Order form")]
    return '<ul class="related">' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in links if h != current) + "</ul>"

def build():
    pages = {}

    # ---------- HUB ----------
    faqs = [
        ("Is Sov Services still trading?", "Yes. Sov Services has supplied patient chart folders and holders to Australian hospitals since 1994. From 26 October 2026 it is owned and run by Brisbane Plastics Company from the same Tingalpa factory, with the same products and item codes."),
        ("Do your item codes stay the same?", "Yes, for every product we still make, so you can reorder from your last order sheet or purchase order. Glove box holders (SS-GB-015, SS-GB-008) and the accessory basket (SS-GB-029) are no longer made, and hanging folders now come in 30 and 40 mm spines only."),
        ("Can we still email our orders?", f"Yes. <a href=\"mailto:{SOV_EMAIL}\">{SOV_EMAIL}</a> stays open, and so does our phone number, 1300 744 104. The online order form is quicker because it asks for the ward, colour and print details we need, so we do not have to come back to you."),
        ("Has your ABN changed?", f"Yes. Orders from 26 October 2026 are supplied and invoiced by Brisbane Plastics Company Pty Ltd, ABN {ABN}. If your purchasing system still lists the old supplier, please ask your supply team to update the vendor record. We will verify bank details by phone on request."),
        ("How long does an order take?", "Standard orders take 10 to 15 working days from order and artwork approval. Ask about express turnaround. Put your date in the Needed by box on the order form."),
        ("Can you print our ward name and bed numbers?", "Yes. Folders can be printed with the ward name and bed number on the front and spine in black or white. Tell us the ward name and the bed numbers you need on the order form."),
    ]
    main = hero(C_HUB, "Patient chart folders, chart holders and hospital ward products",
                "The Sov Services hospital range: patient chart folders, hanging folders, chart holders, clipboards and tab dividers. Australian made, infection control approved, and preferred supplier to more than 250 medical establishments across Australia since 1994. Now made and supplied by Brisbane Plastics Company in Tingalpa, Brisbane.",
                kicker="Sov Services · Australian made",
                buttons=[("/hospital/order", "Order or reorder online"), ("#range", "See the range")])
    range_groups = "".join(
        f'<h3 class="sov-group"><a href="{pg}">{esc(g)}</a></h3>' + sov_link_tiles([x for x in SOV_PRODUCTS if x["page"] == pg])
        for pg, g in SOV_GROUPS)
    main += f'''<div class="band"><div class="wrap">
<p><strong>Same products, same item codes, new owner.</strong> From 26 October 2026 Sov Services orders are supplied and invoiced by Brisbane Plastics Company Pty Ltd, ABN {ABN}.</p>
</div></div>
<section class="block alt" id="range"><div class="wrap">
<div class="section-head"><h2>The range</h2><p class="lede">Built for wards: wipe-clean, colour-coded and made to fit the bed rail, the wall and the 2-ring binder. Prices exclude GST.</p></div>
{range_groups}
<div class="notice"><p><strong>Need ward or wayfinding signs?</strong> We print ward, room and directory signs in the same factory. <a href="/uv-printing/hospital-signs">Hospital and clinic signs</a></p></div>
</div></section>
<section class="block"><div class="wrap split">
<div>
<h2>Why wards keep reordering</h2>
<ul class="ticks">
<li>Australian made in our Tingalpa factory.</li>
<li>Infection control approved, and trusted by more than 250 medical establishments across Australia.</li>
<li>Designed with nursing and theatre staff, and refined from their feedback since 1994.</li>
<li>Colour-coded folders make the right chart easy to find at the bedside.</li>
<li>Wipe-clean polypropylene and gloss finishes for ward cleaning routines.</li>
<li>Ward and bed printing on the front and spine, so charts go back to the right bed.</li>
<li>The same SS- item codes, so reorders are quick for your supply team.</li>
</ul>
</div>
<div>
<h2>Ordering in three steps</h2>
<ol class="steps" style="grid-template-columns:1fr">
<li><h3>Send the order</h3><p>Use the <a href="/hospital/order">online order form</a>, email your purchase order to {SOV_EMAIL} or call 1300 744 104.</p></li>
<li><h3>We confirm</h3><p>We confirm price, print details and delivery by return email, and send a proof for any new printing.</p></li>
<li><h3>Made and delivered</h3><p>Printed and packed in Tingalpa and freighted to your ward or store anywhere in Australia. Standard orders take 10 to 15 working days from order and artwork approval. Ask about express turnaround.</p></li>
</ol>
</div>
</div></section>
<section class="block alt" id="faq"><div class="wrap" style="max-width:860px">
{faq_block(faqs, "Changes for existing Sov Services customers")}
</div></section>
{order_cta()}'''
    pages[HUB] = page(HUB, "Patient Chart Folders & Holders | Sov Services Hospital Range",
                      "Australian-made Sov Services patient chart folders, chart holders, clipboards and dividers. Supplying 250+ medical establishments since 1994. Order online.",
                      main, C_HUB, [faq_schema(faqs), sov_schema()])

    # ---------- CHART FOLDERS ----------
    p = "/hospital/patient-chart-folders"
    cr = C_HUB + [(p, "Patient chart folders")]
    faqs = [
        ("Which spine size do I need?", "Choose by how thick your charts get. If you are unsure, tell us the ward type and what your current folders look like, and we will suggest a size."),
        ("What is the difference between generic and custom print?", "Generic print has ward and bed fields on the front and spine for staff to fill in. Custom print has your ward name and the bed number printed for you. Custom print has a one-off digital artwork set-up charge."),
        ("Which colours work best with black print?", "Yellow and grey give the strongest contrast with black print. White print works best on the darker colours such as Navy, Oxford Blue and Purple."),
        ("Can we order a single colour per ward?", "Yes. Many hospitals colour-code by ward or unit. Tell us the colour code and quantity for each ward on one order."),
    ]
    rows = [("30 mm", "245 × 315 mm", "SS-PCU-13", "SS-PCU-03", "SS-PCU-13 H / 03 H"),
            ("40 mm", "255 × 315 mm", "SS-PCU-14", "SS-PCU-04", "SS-PCU-14 H / 04 H"),
            ("55 mm", "280 × 315 mm", "SS-PCU-15", "SS-PCU-05", "Not available"),
            ("68 mm", "280 × 315 mm", "SS-PCU-16", "SS-PCU-06", "Not available")]
    trs = "".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td><td><code>{c}</code></td><td><code>{d}</code></td><td>{'<code>'+e+'</code>' if e.startswith('SS') else e}</td></tr>" for a, b, c, d, e in rows)
    main = hero(cr, "Patient chart folders", "Polypropylene patient chart folders in four spine sizes and ten colours. Plain, printed with ward and bed fields, or custom printed with your ward name and bed number. Hanging versions for chart trolleys and filing.",
                kicker="Sov Services · Australian made", buttons=[("/hospital/order", "Order chart folders"), ("#sizes", "Sizes and codes")])
    main += sov_product_tiles(p)
    main += f'''<section class="block alt" id="sizes"><div class="wrap">
<div class="table-wrap"><table class="spec">
<caption class="hidden">Patient chart folder sizes and item codes</caption>
<thead><tr><th>Spine</th><th>Folder size</th><th>Unprinted</th><th>Ward and bed print</th><th>Hanging folder (unprinted / printed)</th></tr></thead>
<tbody>{trs}</tbody></table></div>
<p class="form-note" style="margin-top:.8rem">Add the two-digit colour code to the item code when you order, for example <span class="code">SS-PCU-04</span> in Navy <span class="code">06</span>.</p>
</div></section>
<section class="block"><div class="wrap two-col">
<div>
<h2>Colours</h2>
<p>Ten stock colours for colour-coding by ward, unit or specialty. Print in black or white. Black folders are available on request.</p>
{swatches()}
</div>
<div>
<h2>Print options</h2>
<ul class="facts">
<li><strong>Unprinted.</strong> Plain folders in any stock colour.</li>
<li><strong>Generic print.</strong> Ward and bed fields printed on the front and spine, ready for staff to fill in.</li>
<li><strong>Custom print.</strong> Your ward name and bed number printed on the front and spine. One-off artwork set-up charge.</li>
<li><strong>Hanging folders.</strong> 30 and 40 mm spines, generic or custom print. A landscape layout on the front cover is easiest to read in a trolley.</li>
</ul>
</div>
</div></section>
{gallery([("hospital-chart-folder-ward-bed.jpg","Polypropylene patient chart folder printed with ward and bed","Ward and bed print on the front and spine"),("hospital-chart-folder-open.jpg","Inside of a patient chart folder with clip and 2-ring binder fitting","Clip and 2-ring fitting inside")])}
<section class="block alt"><div class="wrap" style="max-width:860px">
{faq_block(faqs)}
<h2 style="margin-top:2.5rem;font-size:1.3rem">Also in the range</h2>
{related(p)}
</div></section>
{order_cta()}'''
    pages[p] = page(p, "Patient Chart Folders, Printed Ward & Bed | Sov Services",
                    "Polypropylene patient chart folders in 30, 40, 55 and 68 mm spines and ten colours. Ward and bed or custom print, hanging folders. Item codes and online ordering.",
                    main, cr, [faq_schema(faqs)])

    # ---------- CHART HOLDERS ----------
    p = "/hospital/patient-chart-holders"
    cr = C_HUB + [(p, "Chart holders and clipboards")]
    items = [
        ("SS-PCU-033", "A3 patient chart holder, horizontal", "Black or white gloss", "350 W × 300 H × 45 D mm, 50 mm rollover"),
        ("SS-PCU-034", "A4 patient chart holder, vertical", "Black or white gloss", "280 W × 370 H × 50 D mm, 50 mm rollover"),
        ("SS-PCU-038 / 039", "A4 wall-mounted chart holder, vertical or horizontal", "Black or white gloss", "255 W × 315 H × 110 D mm"),
        ("SS-CCB-010 / 011 / 012", "A4 patient clipboard: 010 vertical, 011 horizontal, 012 horizontal with D-rings", "White impact-resistant ABS", "230 W × 360 H × 50 D mm at the top"),
        ("SS-CCB-015", "A3 patient clipboard, horizontal", "White impact-resistant ABS", "450 W × 360 H × 50 D mm at the top"),
    ]
    trs = "".join(f"<tr><td><code>{a}</code></td><th scope=\"row\">{b}</th><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in items)
    faqs = [
        ("What is the rollover?", "The rollover is the curved top lip that hooks over the bed-end rail, so the chart sits at the foot of the bed without fixings."),
        ("Do the clipboards take a ring binder?", "Each clipboard is fitted with either a standard clipboard clip or two D-ring clips. Tell us which on your order."),
        ("Can the A4 holder go on the wall?", "Yes. The wall-mounted A4 holder comes in horizontal (SS-PCU-038) and vertical (SS-PCU-039) versions."),
    ]
    main = hero(cr, "Patient chart holders and clipboards", "A3 and A4 chart holders that hook over the bed rail or mount on the wall, and impact-resistant ABS clipboards with a rollover top for rail mounting.",
                kicker="Sov Services · Australian made", buttons=[("/hospital/order", "Order holders"), ("#range", "Sizes and codes")])
    main += sov_product_tiles(p)
    main += f'''<section class="block alt" id="range"><div class="wrap">
<div class="table-wrap"><table class="spec">
<caption class="hidden">Chart holder and clipboard item codes</caption>
<thead><tr><th>Item code</th><th>Product</th><th>Finish</th><th>Size</th></tr></thead>
<tbody>{trs}</tbody></table></div>
</div></section>
<section class="block"><div class="wrap" style="max-width:860px">
{faq_block(faqs)}
<h2 style="margin-top:2.5rem;font-size:1.3rem">Also in the range</h2>
{related(p)}
</div></section>
{order_cta()}'''
    pages[p] = page(p, "Patient Chart Holders & Bed Rail Clipboards | Sov Services",
                    "A3 and A4 patient chart holders for the bed rail or wall, and ABS patient clipboards with rollover top. Item codes, sizes and online ordering for hospitals.",
                    main, cr, [faq_schema(faqs)])

    # ---------- DIVIDERS ----------
    p = "/hospital/chart-dividers"
    cr = C_HUB + [(p, "Chart dividers")]
    faqs = [
        ("Is there a minimum order?", "There is no minimum for the standard blank and printed 5-tab dividers. Custom tab dividers have a minimum of 50 sets."),
        ("What if we need more than seven tabs?", "With eight or more tabs we suggest a set of five in front with the rest behind, so every tab stays readable in the binder."),
        ("Will they fit our binders?", "The dividers are made for A4 2-ring (2D) binders, which most patient chart systems use. If yours differ, send us a sample or the ring spacing."),
    ]
    main = hero(cr, "Tabbed chart dividers for patient records", "5-tab dividers for A4 2-ring binders, blank or printed with the standard chart sections. Custom tabs from 1 to 10 for your own chart structure.",
                kicker="Sov Services · Australian made", buttons=[("/hospital/order", "Order dividers")])
    main += sov_product_tiles(p)
    main += f'''<section class="block alt"><div class="wrap">
<div class="table-wrap"><table class="spec">
<caption class="hidden">Chart divider options</caption>
<thead><tr><th>Item code</th><th>Divider</th><th>Tabs</th><th>Minimum order</th></tr></thead>
<tbody>
<tr><td><code>SS-PCU-043</code></td><th scope="row">5-tab divider, blank</th><td>Five blank tabs</td><td>None</td></tr>
<tr><td><code>SS-PCU-045</code></td><th scope="row">5-tab divider, printed</th><td>Observations, Medications, Fluids, Care Plans, Other</td><td>None</td></tr>
<tr><td>Custom</td><th scope="row">Custom tab divider</th><td>1 to 10 tabs, your wording</td><td>50 sets</td></tr>
</tbody></table></div>
<p class="form-note" style="margin-top:.8rem">Suits hospitals, medical centres and health administration. Fits A4 2-ring (2D) binders.</p>
</div></section>
{gallery([("printed-tab-dividers.jpg","5-tab dividers with printed coloured tabs","Printed 5-tab dividers"),("hospital-dividers-5-tab.jpg","Coloured 5-tab chart dividers for A4 2-ring binders","Coloured tabs for quick section finding"),("polypropylene-tab-dividers.jpg","White polypropylene tab divider with punched holes","Polypropylene dividers, punched for 2-ring binders")])}
<section class="block"><div class="wrap" style="max-width:860px">
{faq_block(faqs)}
<h2 style="margin-top:2.5rem;font-size:1.3rem">Also in the range</h2>
{related(p)}
</div></section>
{order_cta()}'''
    pages[p] = page(p, "Patient Chart Dividers, 5-Tab & Custom | Sov Services",
                    "A4 2-ring patient chart dividers: 5-tab blank, 5-tab printed (Observations, Medications, Fluids, Care Plans, Other) and custom 1 to 10 tabs. Order online.",
                    main, cr, [faq_schema(faqs)])

    # ---------- ORDER FORM ----------
    p = "/hospital/order"
    cr = C_HUB + [(p, "Order form")]
    opts = '<option value="">Choose an item</option>' + "".join(
        f'<optgroup label="{esc(g)}">' + "".join(f"<option>{esc(o)}</option>" for o in items) + "</optgroup>" for g, items in ORDER_CODES)
    colours = '<option value="">Colour</option>' + "".join(f"<option>{n} {c}</option>" for n, c, _ in FOLDER_COLOURS) + "<option>Black (on request)</option><option>Black gloss</option><option>White gloss</option><option>White</option><option>Not applicable</option>"
    lines = ""
    for i in range(1, 9):
        req = " required" if i == 1 else ""
        hid = "" if i == 1 else " hidden"
        lines += f'''<tr class="order-line"{hid}>
<td data-label="Item"><select name="item_{i}" aria-label="Item {i}"{req}>{opts}</select></td>
<td data-label="Colour"><select name="colour_{i}" aria-label="Colour {i}">{colours}</select></td>
<td data-label="Print (ward, beds)"><input name="print_{i}" aria-label="Print text {i}" placeholder="e.g. Ward 4B, beds 1 to 24"></td>
<td data-label="Quantity"><input name="qty_{i}" aria-label="Quantity {i}" inputmode="numeric" pattern="[0-9]*[1-9][0-9]*" title="Enter a whole number" placeholder="Qty"{req}></td>
</tr>'''
    main = hero(cr, "Hospital order and reorder form", f"Order Sov Services products for your ward. We confirm price, print and delivery by return email before anything is made. Prefer email or phone? Send your purchase order to <a href=\"mailto:{SOV_EMAIL}\">{SOV_EMAIL}</a> or call <a href=\"tel:1300744104\">1300 744 104</a>.",
                kicker="Sov Services · Australian made")
    main += f'''<section class="block" style="padding-top:1.5rem"><div class="wrap">
<form class="quote" name="hospital-order" method="POST" action="/hospital/thanks" data-netlify="true" netlify-honeypot="company_website" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="hospital-order">
{TRACKING}
<p class="hidden"><label>Leave this empty <input name="company_website"></label></p>
<fieldset>
<legend>Order type</legend>
<div class="choice">
<label><input type="radio" name="order_type" value="reorder" checked> Reorder, same as last time</label>
<label><input type="radio" name="order_type" value="new" > New order or change</label>
<label><input type="radio" name="order_type" value="quote"> Price check or quote only</label>
</div>
</fieldset>
<fieldset>
<legend>Hospital and ward</legend>
<div class="grid2">
<div class="field"><label for="facility">Hospital or facility</label><input id="facility" name="facility" autocomplete="organization" required></div>
<div class="field"><label for="ward">Ward or department</label><input id="ward" name="ward" required></div>
<div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required></div>
<div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="po">Purchase order number <span class="hint">if you have one</span></label><input id="po" name="po_number"></div>
<div class="field full"><label for="delivery">Delivery address</label><textarea id="delivery" name="delivery_address" style="min-height:80px" placeholder="Ward, building, street, suburb, state, postcode"></textarea></div>
</div>
</fieldset>
<fieldset>
<legend>Items</legend>
<table class="items">
<thead><tr><th style="width:42%">Item</th><th style="width:18%">Colour</th><th>Print (ward, beds)</th><th style="width:11%">Qty</th></tr></thead>
<tbody>{lines}</tbody>
</table>
<button type="button" class="btn ghost" id="add-line">Add another item</button>
<p class="form-note">Need more than eight lines? Attach your order sheet below or add it to the notes.</p>
<script type="application/json" id="order-map">{_json.dumps(ORDER_OPT)}</script>
</fieldset>
<fieldset>
<legend>Anything else</legend>
<div class="grid2">
<div class="field"><label for="needed_by">Needed by</label><input id="needed_by" name="needed_by" type="date"></div>
<div class="field"><label for="artwork">Order sheet or artwork <span class="hint">PDF, PNG or JPG, up to 8 MB. Please do not include patient information.</span></label><input id="artwork" name="attachment" type="file" accept="{ART_ACCEPT}"><p id="artwork-error" class="error" role="alert"></p></div>
<div class="field full"><label for="notes">Notes</label><textarea id="notes" name="notes" placeholder="Bed numbers, print wording, delivery instructions, previous order reference"></textarea></div>
<div class="field full"><label class="check"><input type="checkbox" name="new_supplier_details" value="yes"> Send our supply team Brisbane Plastics Company's vendor details (ABN and bank details, verified by phone)</label></div>
</div>
</fieldset>
<button class="btn" type="submit">Send order</button>
<p class="form-note" style="margin-top:1rem">We confirm every order by email before it is made. Your details are used only to process this order. See our <a href="/privacy">privacy statement</a>.</p>
</form>
</div></section>'''
    pages[p] = page(p, "Hospital Order & Reorder Form | Sov Services",
                    "Order or reorder Sov Services patient chart folders, holders and dividers online. Item codes, colours and ward and bed printing.",
                    main, cr)

    # ---------- THANKS ----------
    p = "/hospital/thanks"
    main = f'''<section class="page-hero"><div class="wrap">
<h1>Order received. Thank you.</h1>
<p class="lede">We will confirm price, print details and delivery by email, usually within one business day. If anything is urgent, email <a href="mailto:{SOV_EMAIL}">{SOV_EMAIL}</a>.</p>
<div class="btn-row"><a class="btn" href="/hospital/">Back to the hospital range</a><a class="btn ghost" href="/hospital/order">Place another order</a></div>
</div></section>'''
    pages[p] = page(p, "Order received | Sov Services", "Thank you for your order.", main, noindex=True)
    return pages
