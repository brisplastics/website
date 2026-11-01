"""Colour ranges and print options: one numbered list per range, shown on /products/printing-and-finishing,
linked from every product page, and used by the quote form's colour list (it follows the material chosen).
Sources: PVC 35-colour chart (PU colour chart folder, item 107); leather-look list from plasticsunique.com.au/leather-look-colour-range
(read 01/11/2026); tarp PVC list printed on its chart; polypropylene names read off the swatch tags in PU's photos, numbered left to
right, top to bottom. Names marked (?) in REVIEW are for Karen to confirm before go-live."""
from shell import esc
from forms_items import PVC_COLOURS

IMG = "/assets/img/products/printing-and-finishing/"

RANGES = [
    dict(key="pvc", title="Standard PVC", photo="printing-and-finishing-pu-10", w=1123, h=794,
         colours=PVC_COLOURS, note="35 colours. * A pastel surcharge applies to the colours marked with a star."),
    dict(key="leather", title="Leather-look PVC", photo="printing-and-finishing-pu-05", w=1600, h=1200,
         colours=["Premier Print – Burgundy", "Premier Print – Brown", "Premier Print – Blue", "Premier Print – Green",
                  "Director – Black", "Director – Charcoal", "Director – Navy", "Director – Burgundy", "Director – White"],
         note="Premier Print and Director leather-grain vinyl PVC. Numbered clockwise from the bottom of the fan."),
    dict(key="poly", title="Polypropylene", photo="printing-and-finishing-pu-08", w=1600, h=1200,
         colours=["White", "Light Grey", "Charcoal", "Navy Blue", "Pink", "Yellow", "Orange", "Purple",
                  "Red", "Apple Green", "Bottle Green", "Burgundy", "Aqua Blue", "Oxford Blue", "Cobalt Blue", "Black"],
         note="16 colours, numbered left to right from the top row."),
    dict(key="tpoly", title="Transparent polypropylene", photo="printing-and-finishing-pu-06", w=1600, h=1200,
         colours=["Grey", "Mandarin", "Lime", "Midori", "Strawberry", "Grape", "Yellow", "Cherry", "Blueberry"],
         note="See-through coloured polypropylene, numbered left to right from the top row."),
    dict(key="metal", title="Metallic polypropylene", photo="printing-and-finishing-pu-07", w=1600, h=1200,
         colours=["Gold", "Copper", "Silver", "Brass", "Bronze", "Jade"],
         note="Metallic-look polypropylene, numbered left to right from the top row."),
    dict(key="tarp", title="Tarp PVC", photo="printing-and-finishing-pu-09", w=1080, h=717,
         colours=["Orange", "Red", "Yellow", "Sand", "Black", "Grey", "White", "Light Blue", "Blue", "Purple",
                  "Pink", "Emerald Green", "Aqua", "Green", "White (2L)", "White Block Out"],
         note="Heavy-duty tarpaulin PVC, 16 colours."),
]
# Names read off swatch tags where the embossing was not legible: for Karen to confirm.
REVIEW = {"tpoly": ["Grey", "Yellow"], "poly": ["Aqua Blue"], "metal": ["Silver"]}

# Quote form: which colour list each material uses (None = no list, colour goes in notes)
MATERIAL_RANGE = {"Standard PVC": "pvc", "Padded PVC": "pvc", "Leather-look PVC": "leather", "Polypropylene": "poly",
                  "Transparent coloured polypropylene": "tpoly", "Metallic polypropylene": "metal", "Tarp PVC": "tarp",
                  "Clear PVC": None, "Clear or frosted polypropylene": None, "Not sure": "pvc"}

PRINTS = [
    ("screen", "Screen print", "printing-and-finishing-15", 640, 480,
     "Best for logos and simple designs in one or a few solid colours, and the most economical for larger runs. Any PMS colour on white PVC; on coloured material we may print a white base first. In house, up to 600 × 800 mm."),
    ("foil", "Foil stamping", "printing-and-finishing-pu-01", 1600, 1200,
     "Gold, silver and coloured foils for a premium finish on binders, folders, and book and Bible covers. Up to 250 × 300 mm."),
    ("deboss", "Embossing and debossing", "printing-and-finishing-pu-02", 1600, 1200,
     "Your logo pressed into the material for a subtle, permanent finish."),
    ("digital", "Full-colour digital (CMYK)", "printing-and-finishing-pu-03", 1600, 1200,
     "Photos, gradients and full-colour artwork with no limit on colours. UV flatbed print up to 1250 × 2500 mm."),
    ("encapsulated", "Encapsulated print", "printing-and-finishing-pu-04", 1600, 1200,
     "Full-colour print sealed under clear PVC, so the design is protected from wear."),
]
USED_PHOTOS = {r["photo"] for r in RANGES} | {p[2] for p in PRINTS}


def _fig(photo, w, h, alt):
    return (f'<a class="lb" href="{IMG}{photo}.jpg" data-w="{w}" data-h="{h}">'
            f'<img src="{IMG}{photo}-t.jpg" alt="{esc(alt)}" loading="lazy" decoding="async"></a>')


def section():
    """Full colour and print section for the printing-and-finishing page."""
    rng = "".join(
        f'<article class="crange" id="colours-{r["key"]}">{_fig(r["photo"], r["w"], r["h"], r["title"] + " colour range, numbered")}'
        f'<div><h3>{esc(r["title"])}</h3><p>{esc(r["note"])}</p>'
        f'<ol class="clist">{"".join(f"<li>{esc(c)}</li>" for c in r["colours"])}</ol></div></article>'
        for r in RANGES)
    prn = "".join(
        f'<article class="crange" id="print-{k}">{_fig(ph, w, h, t)}<div><h3>{esc(t)}</h3><p>{esc(txt)}</p></div></article>'
        for k, t, ph, w, h, txt in PRINTS)
    return (f'<section class="block" id="colours"><div class="wrap"><div class="section-head"><h2>Colour ranges</h2>'
            f'<p class="lede">Quote the range and number, for example "Standard PVC 11 Navy Blue". Screen colours vary, so ask for a physical swatch if the shade matters. Select a photo to enlarge it.</p></div>{rng}</div></section>'
            f'<section class="block alt" id="print-options"><div class="wrap"><div class="section-head"><h2>Print options</h2>'
            f'<p class="lede">Not sure which suits your artwork? Send it to us and we will recommend one.</p></div>{prn}</div></section>')


def sidebar():
    """Small box on each product page linking to the ranges, like the old PU site."""
    thumbs = [("colours-pvc", "Standard PVC colours", "printing-and-finishing-pu-10"),
              ("colours-leather", "Leather-look colours", "printing-and-finishing-pu-05"),
              ("colours-poly", "Polypropylene colours", "printing-and-finishing-pu-08"),
              ("colours-metal", "Metallic colours", "printing-and-finishing-pu-07")]
    prints = [("print-screen", "Screen print"), ("print-foil", "Foil and debossing"), ("print-digital", "Full-colour digital"), ("print-encapsulated", "Encapsulated print")]
    base = "/products/printing-and-finishing#"
    return ('<div class="cbox"><h3>Colours and print options</h3><ul class="cthumbs">'
            + "".join(f'<li><a href="{base}{a}"><img src="{IMG}{ph}-t.jpg" alt="" loading="lazy" width="96" height="72"><span>{t}</span></a></li>' for a, t, ph in thumbs)
            + '</ul><p class="cprints">' + " · ".join(f'<a href="{base}{a}">{t}</a>' for a, t in prints) + '</p></div>')


def form_data():
    """Colour lists for the quote form JS: {material: [options]}."""
    out = {}
    for m, k in MATERIAL_RANGE.items():
        if k is None:
            out[m] = {"chart": "", "list": []}
            continue
        r = next(x for x in RANGES if x["key"] == k)
        out[m] = {"chart": k, "list": [f"{i} {c}" for i, c in enumerate(r["colours"], 1)]}
    return out
