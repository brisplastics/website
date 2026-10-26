"""UV flatbed printing section. Machine: Canon Arizona 135 GT, serial 3301022.
Spec from Canon ANZ product page and Canon spec sheet (read 24/10/2026).
Configuration per Bruce 24/10/2026: white ink yes, varnish no, roll option no."""
from shell import *
from forms import TRACKING, optin, artwork_fields

HUB = "/uv-printing/"
C_HUB = [("/", "Home"), (HUB, "UV Printing")]

MATERIALS = ["Acrylic (clear, frosted, coloured)", "Foamed PVC sheet", "Rigid PVC", "Polycarbonate", "Styrene",
             "Polypropylene sheet", "Corflute (fluted polypropylene)", "Aluminium composite panel (ACM)", "Aluminium sheet",
             "Wood and plywood", "MDF", "Glass", "Ceramic tile", "Heavy card and board", "Pre-cut items and objects"]

BED_SVG = '''<figure class="bed">
<svg viewBox="0 0 560 300" role="img" aria-labelledby="bedt bedd" xmlns="http://www.w3.org/2000/svg">
<title id="bedt">Printable area of the flatbed</title>
<desc id="bedd">The bed prints sheets up to 2500 mm long, 1250 mm wide and 50.8 mm thick, edge to edge. An A4 sheet is shown for scale.</desc>
<rect x="40" y="30" width="480" height="240" rx="6" fill="#D6E4F8" stroke="#122B4A" stroke-width="2"/>
<g stroke="#1E5FD9" stroke-opacity=".25">
<line x1="136" y1="30" x2="136" y2="270"/><line x1="232" y1="30" x2="232" y2="270"/><line x1="328" y1="30" x2="328" y2="270"/><line x1="424" y1="30" x2="424" y2="270"/>
<line x1="40" y1="90" x2="520" y2="90"/><line x1="40" y1="150" x2="520" y2="150"/><line x1="40" y1="210" x2="520" y2="210"/>
</g>
<rect x="56" y="214" width="40" height="57" fill="#fff" stroke="#122B4A" stroke-width="1.5" transform="translate(0,-16)"/>
<text x="76" y="232" font-family="Inter,sans-serif" font-size="11" fill="#122B4A" text-anchor="middle">A4</text>
<line x1="40" y1="16" x2="520" y2="16" stroke="#122B4A" stroke-width="1.5"/>
<line x1="40" y1="10" x2="40" y2="22" stroke="#122B4A" stroke-width="1.5"/><line x1="520" y1="10" x2="520" y2="22" stroke="#122B4A" stroke-width="1.5"/>
<text x="280" y="12" font-family="Inter,sans-serif" font-size="13" font-weight="600" fill="#122B4A" text-anchor="middle">2500 mm</text>
<line x1="534" y1="30" x2="534" y2="270" stroke="#122B4A" stroke-width="1.5"/>
<line x1="528" y1="30" x2="540" y2="30" stroke="#122B4A" stroke-width="1.5"/><line x1="528" y1="270" x2="540" y2="270" stroke="#122B4A" stroke-width="1.5"/>
<text x="548" y="154" font-family="Inter,sans-serif" font-size="13" font-weight="600" fill="#122B4A" text-anchor="middle" transform="rotate(90 548 150)">1250 mm</text>
<text x="280" y="150" font-family="Archivo,sans-serif" font-size="22" font-weight="800" fill="#122B4A" text-anchor="middle">Print bed</text>
<text x="280" y="174" font-family="Inter,sans-serif" font-size="13" fill="#55667C" text-anchor="middle">Edge to edge · up to 50.8 mm thick</text>
</svg>
<figcaption>Full sheets up to 1250 × 2500 mm print in one pass. Smaller items are ganged across the bed, which keeps short runs economical.</figcaption>
</figure>'''

SPEC_ROWS = [
    ("Printer", "Canon Arizona 135 GT true flatbed, LED-UV curing"),
    ("Maximum print size", "1250 × 2500 mm, edge to edge"),
    ("Maximum thickness", "50.8 mm"),
    ("Inks", "CMYK plus white"),
    ("White ink uses", "Under-print on clear and dark materials, reverse (second-surface) printing on clear acrylic, diffuser layers for backlit panels"),
    ("Run lengths", "One-off prototypes to production runs"),
    ("Turnaround", "10 to 15 working days for standard jobs. Express turnaround available"),
    ("Finishing in house", "Guillotining, die cutting, creasing, RF welding, foil blocking, eyelets and rivets"),
    ("Collection and freight", "Pick-up from Tingalpa, Brisbane, or freight Australia-wide"),
]

def spec_table():
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in SPEC_ROWS)
    return f'<div class="table-wrap"><table class="spec"><caption class="hidden">UV flatbed printing specification</caption><tbody>{rows}</tbody></table></div>'

def materials_list():
    return '<ul class="ticks" style="columns:2;column-gap:2rem">' + "".join(f"<li>{m}</li>" for m in MATERIALS) + "</ul>"

PAGES_INDEX = [
    ("/uv-printing/trade", "Trade printing", "Print-ready files in, printed sheets out. For sign shops, printers, designers and promo companies.", "var(--ink)"),
    ("/uv-printing/acrylic", "Acrylic printing", "Clear, frosted and coloured acrylic, printed face or reverse with white ink.", "var(--pvc-clear)"),
    ("/uv-printing/pvc-signs", "PVC and foamed PVC signs", "Foamed PVC, rigid PVC, polycarbonate, styrene and corflute.", "var(--pvc-blue)"),
    ("/uv-printing/acm-aluminium-signs", "ACM and aluminium signs", "Aluminium composite panel and aluminium sheet for durable signs.", "var(--steel)"),
    ("/uv-printing/safety-industrial-signs", "Safety and industrial signs", "Site signs, machine labels, nameplates and control panel overlays.", "var(--pvc-yellow)"),
    ("/uv-printing/pos-displays", "Retail and POS displays", "Counter displays, menu boards, shelf signs and packaging prototypes.", "var(--pvc-red)"),
    ("/uv-printing/printed-plastic-products", "Printed and fabricated products", "Printed, then cut, welded, creased or foiled in the same factory.", "var(--pvc-green)"),
    ("/uv-printing/office-signs", "Office and business signs", "Reception, door, room and wayfinding signs for offices, clinics and shops.", "var(--blue)"),
    ("/uv-printing/school-signs", "School signs and honour boards", "Campus wayfinding, building, sports and honour boards for schools.", "var(--pvc-yellow)"),
    ("/uv-printing/hospital-signs", "Hospital and clinic signs", "Ward, room, wayfinding and notice signs for hospitals, clinics and aged care.", "var(--teal)"),
]

def index_cards(exclude=None):
    lis = "".join(f'<li style="--tab:{c}"><h3><a href="{h}">{t}</a></h3><p>{d}</p><a class="more" href="{h}">More</a></li>'
                  for h, t, d, c in PAGES_INDEX if h != exclude)
    return f'<ul class="cards">{lis}</ul>'

def related(current):
    return '<ul class="related">' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _, _ in PAGES_INDEX if h != current) + '<li><a href="/uv-printing/">UV Printing overview</a></li></ul>'

MAT_OPTS = ["Not sure yet", "Acrylic", "Foamed PVC", "Rigid PVC", "Polycarbonate", "Corflute", "ACM / aluminium composite", "Aluminium sheet",
            "Wood, plywood or MDF", "Glass or tile", "Card or board", "Polypropylene", "Our own items or objects", "Other"]

def quote_form(path, heading="Get a print quote", trade_default=False):
    mats = "".join(f"<option>{m}</option>" for m in MAT_OPTS)
    t_chk = " checked" if trade_default else ""
    d_chk = "" if trade_default else " checked"
    return f'''<section class="block alt" id="quote"><div class="wrap two-col">
<form class="quote" name="print-quote" method="POST" action="/uv-printing/thanks" data-netlify="true" netlify-honeypot="company_website" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="print-quote">
<input type="hidden" name="page" value="{path}">
{TRACKING}
<p class="hidden"><label>Leave this empty <input name="company_website"></label></p>
<h2 style="font-size:1.6rem">{heading}</h2>
<fieldset>
<legend>About you</legend>
<div class="choice" style="margin-bottom:1rem">
<label><input type="radio" name="customer_type" value="trade"{t_chk}> Trade (sign shop, printer, designer, reseller)</label>
<label><input type="radio" name="customer_type" value="direct"{d_chk}> Business or organisation</label>
</div>
<div class="grid2">
<div class="field"><label for="pq-name">Name</label><input id="pq-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="pq-company">Business</label><input id="pq-company" name="company" autocomplete="organization"></div>
<div class="field"><label for="pq-email">Email</label><input id="pq-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="pq-phone">Phone</label><input id="pq-phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
</fieldset>
<fieldset>
<legend>The job</legend>
<div class="grid2">
<div class="field"><label for="pq-use">What is it?</label><select id="pq-use" name="job_type"><option>Sign or panel</option><option>Display or stand</option><option>Label, nameplate or overlay</option><option>Award, plaque or gift</option><option>Printing on items I supply</option><option>Prototype or sample</option><option>Other</option></select></div>
<div class="field"><label for="pq-where">Where will it be used?</label><select id="pq-where" name="location"><option>Indoors</option><option>Outdoors</option><option>Not sure</option></select></div>
<div class="field"><label for="pq-material">Material</label><select id="pq-material" name="material">{mats}</select></div>
<div class="field"><label for="pq-supply">Who supplies the material?</label><select id="pq-supply" name="material_supply"><option>You supply it</option><option>I supply it</option><option>Not sure</option></select></div>
<div class="field"><label for="pq-size">Finished size <span class="hint">W × H mm</span></label><input id="pq-size" name="size" placeholder="e.g. 600 × 900"></div>
<div class="field"><label for="pq-thick">Thickness <span class="hint">mm, if known</span></label><input id="pq-thick" name="thickness" placeholder="e.g. 3"></div>
<div class="field"><label for="pq-qty">Quantity <span class="hint">list several for price breaks</span></label><input id="pq-qty" name="quantity" placeholder="e.g. 20, or 10 / 50 / 100"></div>
<div class="field"><label for="pq-sides">Print</label><select id="pq-sides" name="print_sides"><option>Full colour, one side</option><option>Full colour, both sides</option><option>Reverse print on clear (second surface)</option><option>White ink only or spot white</option><option>Not sure</option></select></div>
<div class="field"><label for="pq-cut">Cutting</label><select id="pq-cut" name="cutting"><option>Supplied to size, no cutting</option><option>Straight cuts to size</option><option>Shaped or die cut</option><option>Not sure</option></select></div>
<div class="field"><label for="pq-date">Needed by <span class="hint">standard 10 to 15 working days, express available</span></label><input id="pq-date" name="needed_by" type="date"></div>
<div class="field"><label for="pq-post">Delivery suburb and postcode <span class="hint">for freight</span></label><input id="pq-post" name="delivery_postcode" autocomplete="postal-code" placeholder="e.g. Tingalpa 4173, or collect"></div>
<div class="field"><label for="pq-repeat">Will you need this again?</label><select id="pq-repeat" name="repeat"><option>One-off</option><option>Yes, regularly</option><option>Not sure</option></select></div>
{artwork_fields()}
<div class="field full"><label for="pq-notes">Anything else</label><textarea id="pq-notes" name="notes" placeholder="Finish, fixing holes or stand-offs, double-sided tape, shape, brand colours to match"></textarea></div>
{optin()}
</div>
</fieldset>
<button class="btn" type="submit">Send for a quote</button>
<p class="form-note" style="margin-top:1rem">We reply within one business day. Your details are used only to respond to this request. See our <a href="/privacy">privacy statement</a>.</p>
</form>
<aside>
<h2 style="font-size:1.3rem">File checklist</h2>
<ul class="ticks">
<li>PDF preferred, with fonts outlined or embedded.</li>
<li>Artwork at finished size, with 3 mm bleed for edge-to-edge prints.</li>
<li>Photos and raster images at 150 to 300 dpi at finished size.</li>
<li>CMYK colour. Tell us any brand colours that must match.</li>
<li>White ink on its own spot colour layer. We confirm the naming when we check your file.</li>
</ul>
<div class="notice"><p>Not print-ready? Send what you have. We check every file before printing and tell you if anything needs fixing.</p></div>
</aside>
</div></section>'''

def service_schema(path, name, desc):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "UV flatbed printing",
            "description": desc, "url": url(path), "provider": {"@id": SITE + "/#business"},
            "areaServed": [{"@type": "City", "name": "Brisbane"}, {"@type": "State", "name": "Queensland"}, {"@type": "Country", "name": "Australia"}]}

def sub(path, label, title, desc, h1, lede, body, faqs, trade_default=False):
    cr = C_HUB + [(path, label)]
    main = hero(cr, h1, lede, kicker="UV flatbed printing · Brisbane", buttons=[("#quote", "Get a quote"), ("/uv-printing/", "Printer specification")])
    main += body
    main += f'''<section class="block"><div class="wrap" style="max-width:860px">
{faq_block(faqs)}
<h2 style="margin-top:2.5rem;font-size:1.3rem">More printing</h2>
{related(path)}
</div></section>'''
    main += quote_form(path, trade_default=trade_default)
    return page(path, title, desc, main, cr, [service_schema(path, h1, desc), faq_schema(faqs)])

def block(left, right):
    return f'<section class="block alt"><div class="wrap split"><div>{left}</div><div>{right}</div></div></section>'

def build():
    pages = {}

    # ---------- HUB ----------
    faqs = [
        ("What can you print on?", "Most flat, rigid materials up to 50.8 mm thick: acrylic, foamed PVC, polycarbonate, ACM, aluminium, wood, MDF, glass, tile, card and corflute, plus many pre-cut items. Send us a sample if you are unsure and we will run a test."),
        ("What is the biggest size you can print?", "1250 × 2500 mm in one piece, edge to edge. Larger signs can be printed in panels and joined on site."),
        ("Do you print white ink?", "Yes. White is printed under colour on clear and dark materials, as a solid colour, or behind reverse-printed clear acrylic so the image reads through the face."),
        ("Is there a minimum order?", "No set minimum. We print single prototypes and production runs. Small items are ganged across the bed, so short runs stay economical."),
        ("Can I supply my own material or products?", "Yes. Trade customers often supply cut blanks or finished items. Tell us the material so we can confirm ink adhesion, and we will run a test piece if it is new to us."),
        ("How long does a print job take?", "Standard jobs take 10 to 15 working days. Express turnaround is available. Tell us your date on the quote form."),
        ("Do you print banners or fabric?", "Not at the moment. Our printer is set up for rigid sheet and objects. We do not print roll media such as banners, vinyl or fabric."),
    ]
    main = hero(C_HUB, "UV flatbed printing in Brisbane",
                "Full-colour printing direct onto rigid sheet and objects up to 1250 × 2500 mm and 50.8 mm thick, with white ink. Printed on a Canon Arizona 135 GT in Tingalpa for trade and business customers across Brisbane and Australia.",
                kicker="Trade and direct · Tingalpa, Brisbane",
                buttons=[("#quote", "Get a print quote"), ("/uv-printing/trade", "Trade printing")])
    main += f'''<section class="block alt"><div class="wrap printer">
<h2>The printer: Canon Arizona 135 GT</h2>
<div class="printer-bed">{BED_SVG}</div>
{spec_table()}
</div></section>
<section class="block"><div class="wrap">
<div class="section-head"><h2>What we print</h2><p class="lede">Direct to the material, no mounting or laminating. Choose the job closest to yours.</p></div>
{index_cards()}
</div></section>
<section class="block alt"><div class="wrap split">
<div><h2>Materials</h2>{materials_list()}</div>
<div>
<h2>Why print with a plastics fabricator</h2>
<ul class="facts">
<li><strong>Print and make in one place.</strong> We print, then guillotine, die cut, crease, RF weld, foil block and fit eyelets and rivets in the same factory. One supplier, one lead time.</li>
<li><strong>We know plastics.</strong> We have worked with PVC, polypropylene and acrylic sheet in Tingalpa for 27 years.</li>
<li><strong>White ink on clear.</strong> Under-print, reverse print and backlit diffuser layers on clear acrylic and polycarbonate.</li>
<li><strong>No minimums.</strong> One prototype or a production run, quoted per job.</li>
</ul>
<h3 style="margin-top:1.6rem">What we do not do</h3>
<ul class="ticks crosses"><li>Roll media: banners, vinyl, wallpaper or fabric.</li><li>Sign installation.</li></ul>
</div>
</div></section>
<section class="block"><div class="wrap" style="max-width:860px">{faq_block(faqs)}</div></section>
{quote_form(HUB)}'''
    desc = "UV flatbed printing in Brisbane on acrylic, PVC, ACM, wood, glass and more. Up to 1250 x 2500 mm and 50.8 mm thick, with white ink. Trade and direct. Tingalpa."
    pages[HUB] = page(HUB, "UV Flatbed Printing Brisbane | Trade & Direct | Brisbane Plastics", desc, main, C_HUB,
                      [service_schema(HUB, "UV flatbed printing", desc), faq_schema(faqs)])

    # ---------- TRADE ----------
    p = "/uv-printing/trade"
    body = block(
        '''<h2>Who we print for</h2>
<ul class="ticks">
<li>Sign shops that need a flatbed job printed without buying a flatbed.</li>
<li>Printers and print brokers with rigid jobs outside their kit.</li>
<li>Graphic designers and agencies who want one supplier for print and finish.</li>
<li>Promotional product and display companies printing short runs.</li>
<li>Fabricators and makers who supply cut blanks or finished items for printing.</li>
</ul>''',
        '''<h2>How trade printing works</h2>
<ol class="steps" style="grid-template-columns:1fr">
<li><h3>Send files and specs</h3><p>Print-ready PDF, material, size, quantity and whether you supply the material.</p></li>
<li><h3>Quote and proof</h3><p>We quote within one business day and check every file before it prints.</p></li>
<li><h3>Printed, packed, gone</h3><p>Collect from Tingalpa or we freight it to you or your customer in plain packaging.</p></li>
</ol>''')
    body += f'''<section class="block"><div class="wrap printer"><h2>Specification</h2><div class="printer-bed">{BED_SVG}</div>{spec_table()}</div></section>'''
    faqs = [
        ("Do you offer trade pricing?", "Yes. Regular trade customers can apply for a trade account and trade pricing. Ask on the quote form."),
        ("Will you contact my customer?", "No. Trade work is yours. We deal only with you and can deliver in plain packaging with no Brisbane Plastics branding."),
        ("Can you print on material I supply?", "Yes. Supply cut blanks or full sheets. For a material we have not printed before, we run a test piece first."),
        ("How big can a single print be?", "1250 × 2500 mm and up to 50.8 mm thick, edge to edge. Smaller pieces are ganged across the bed."),
    ]
    desc = "Trade UV flatbed printing in Brisbane for sign shops, printers and designers. Print-ready files, your material or ours, up to 1250 x 2500 mm with white ink. Plain packaging."
    pages[p] = sub(p, "Trade printing", "Trade UV Flatbed Printing Brisbane | Sign Shops & Printers", desc,
                   "Trade UV flatbed printing for sign shops, printers and designers",
                   "Send print-ready files and we print direct to rigid sheet up to 1250 × 2500 mm, with white ink. Your material or ours, quoted within one business day, delivered in plain packaging.",
                   body, faqs, trade_default=True)

    # ---------- ACRYLIC ----------
    p = "/uv-printing/acrylic"
    body = block(
        '''<h2>Acrylic print options</h2>
<ul class="facts">
<li><strong>Face printed.</strong> Colour printed on the front surface. Good for opaque and coloured acrylic.</li>
<li><strong>Reverse printed (second surface).</strong> Printed on the back of clear acrylic with a white backing, so the image sits behind a glossy, protected face.</li>
<li><strong>Backlit.</strong> Colour with a white diffuser layer for light boxes and illuminated signs.</li>
<li><strong>White only or spot white.</strong> Crisp white text and logos on clear, frosted or coloured acrylic.</li>
</ul>''',
        '''<h2>Typical acrylic jobs</h2>
<ul class="ticks">
<li>Reception and office wall signs</li>
<li>Door, room and wayfinding signs</li>
<li>Acrylic photo prints and wall art</li>
<li>Counter displays, stands and menu holders</li>
<li>Light box faces and backlit panels</li>
<li>Plaques, awards and donor boards</li>
<li>Splashbacks and decorative panels</li>
</ul>''')
    faqs = [
        ("What thickness of acrylic can you print?", "Any thickness up to 50.8 mm. Most signs use 3 mm, 4.5 mm or 6 mm sheet."),
        ("Can you print behind clear acrylic?", "Yes. Reverse (second-surface) printing puts the image behind the acrylic with a white backing, so it reads through a glossy, scratch-protected face."),
        ("Can you cut acrylic to shape?", "We cut to size in house. Tell us the shape you need and we will quote it."),
    ]
    desc = "Acrylic printing in Brisbane: face, reverse and backlit printing on clear, frosted and coloured acrylic up to 1250 x 2500 mm, with white ink. Trade and direct."
    pages[p] = sub(p, "Acrylic printing", "Acrylic Printing Brisbane | Clear, Reverse & Backlit", desc,
                   "Acrylic printing in Brisbane",
                   "Full-colour printing on clear, frosted and coloured acrylic, face printed, reverse printed behind clear, or with a white diffuser for backlit signs. Sheets up to 1250 × 2500 mm.",
                   body, faqs)

    # ---------- PVC ----------
    p = "/uv-printing/pvc-signs"
    body = block(
        '''<h2>Materials</h2>
<ul class="facts">
<li><strong>Foamed PVC.</strong> Light, rigid and easy to fix. The standard board for indoor signs and displays.</li>
<li><strong>Rigid PVC.</strong> Thin, tough sheet for labels, panels and printed parts.</li>
<li><strong>Polycarbonate.</strong> Near-unbreakable clear sheet for guards, covers and high-wear signs.</li>
<li><strong>Styrene.</strong> Low-cost sheet for short-life displays and promotions.</li>
<li><strong>Corflute.</strong> Fluted polypropylene for temporary and event signs.</li>
</ul>''',
        '''<h2>Typical jobs</h2>
<ul class="ticks">
<li>Indoor signs and notice boards</li>
<li>School and campus signs</li>
<li>Exhibition and event signage</li>
<li>Display panels and stands</li>
<li>Printed panels and covers for products</li>
<li>Temporary and project signs</li>
</ul>''')
    body += gallery([("printed-polypropylene-sign.jpg","Orange printed polypropylene reserved sign for a gaming venue","Printed polypropylene venue sign"),("drain-warning-sign.jpg","Blue printed drain warning sign","Printed outdoor site sign")], "Examples from our factory")
    faqs = [
        ("Is foamed PVC suitable outdoors?", "It is widely used for short and medium-term outdoor signs. For long-term outdoor use, tell us where the sign will go and we will suggest the right board."),
        ("What thicknesses do you print?", "Anything up to 50.8 mm. Foamed PVC signs are usually 3 mm, 5 mm or 10 mm."),
        ("Can I order a single sign?", "Yes. There is no minimum. Single signs and production runs are both quoted per job."),
    ]
    desc = "PVC sign printing in Brisbane on foamed PVC, rigid PVC, polycarbonate, styrene and corflute. Direct UV print up to 1250 x 2500 mm. Single signs to production runs."
    pages[p] = sub(p, "PVC and foamed PVC signs", "PVC & Foamed PVC Sign Printing Brisbane | Direct UV Print", desc,
                   "PVC and foamed PVC sign printing",
                   "Direct UV printing on foamed PVC, rigid PVC, polycarbonate, styrene and corflute, from a single sign to a production run. Made by a Brisbane PVC fabricator.",
                   body, faqs)

    # ---------- ACM ----------
    p = "/uv-printing/acm-aluminium-signs"
    body = block(
        '''<h2>Why ACM</h2>
<p>Aluminium composite panel (ACM) is two thin aluminium skins bonded to a solid core. It is flat, rigid, light and stable outdoors, which makes it the usual choice for building, site and property signs.</p>
<p>We print direct to the panel face, so there is no vinyl to lift or peel.</p>''',
        '''<h2>Typical jobs</h2>
<ul class="ticks">
<li>Building and shopfront signs</li>
<li>Construction and site signs</li>
<li>Property, estate and directory boards</li>
<li>Wayfinding and car park signs</li>
<li>Equipment and plant panels</li>
</ul>''')
    faqs = [
        ("Can you print on aluminium sheet as well as ACM?", "Yes. We print on ACM and on primed or coated aluminium sheet. Send a sample of anything unusual for a test print."),
        ("Can you supply the panels cut to size?", "Yes. We buy ACM panels in cut to your finished sizes and quote the panels and the print together. Or send us panels already cut and we print them."),
        ("How big can an ACM sign be?", "1250 × 2500 mm printed in one piece. Larger signs are printed as panels."),
    ]
    desc = "ACM and aluminium sign printing in Brisbane. Direct UV print on aluminium composite panel up to 1250 x 2500 mm for building, site and property signs. Trade and direct."
    pages[p] = sub(p, "ACM and aluminium signs", "ACM & Aluminium Sign Printing Brisbane | Direct UV Print", desc,
                   "ACM and aluminium sign printing",
                   "Direct UV printing on aluminium composite panel (ACM) and aluminium sheet, up to 1250 × 2500 mm. Building, site, property and wayfinding signs printed in Brisbane.",
                   body, faqs)

    # ---------- SAFETY / INDUSTRIAL ----------
    p = "/uv-printing/safety-industrial-signs"
    body = block(
        '''<h2>What we print</h2>
<ul class="ticks">
<li>Site safety and mandatory signs</li>
<li>Machine, isolation and hazard labels</li>
<li>Equipment nameplates and asset labels</li>
<li>Control panel overlays and switchboard labels</li>
<li>Pipe, valve and process identification</li>
<li>Emergency and evacuation plans</li>
<li>Danger and out-of-service tags, printed and punched</li>
</ul>''',
        '''<h2>Built for industrial sites</h2>
<ul class="facts">
<li><strong>Tough materials.</strong> Polycarbonate, rigid PVC, ACM and aluminium for workshops, plants and mine sites.</li>
<li><strong>Batches with sequential text.</strong> Numbered labels and asset tags in one run.</li>
<li><strong>Cut, punched and fitted.</strong> Fixing holes, eyelets and die-cut shapes done in house.</li>
<li><strong>Your standard.</strong> Supply your sign artwork or tell us the standard your site works to, for example AS 1319.</li>
</ul>''')
    body += gallery([("danger-sign-rf-welders.jpg","Printed white and red danger sign warning of RF welders in use","Workplace danger sign, made in our factory"),("drain-warning-sign.jpg","Blue printed sign reading Drains to waterway, do not pollute","Environmental site sign")], "Examples from our factory")
    faqs = [
        ("Can you match our site's sign standard?", "Yes. Send your existing artwork or the standard your site follows and we print to it. We do not make compliance assessments for your site."),
        ("Can you print numbered labels and asset tags?", "Yes. Send a spreadsheet of numbers or text and we print them as one batch."),
        ("Do you make lockout and danger tags?", "Yes. Plastics Unique has made danger and out-of-service tags for years. We can print them full colour and punch them for ties."),
    ]
    desc = "Safety signs, machine labels, nameplates and control panel overlays printed in Brisbane on polycarbonate, PVC, ACM and aluminium. Numbered batches and danger tags."
    pages[p] = sub(p, "Safety and industrial signs", "Safety Signs, Machine Labels & Panel Overlays Brisbane", desc,
                   "Safety signs, machine labels and control panel overlays",
                   "Industrial signs and labels printed direct onto polycarbonate, PVC, ACM and aluminium in Brisbane, with numbered batches, fixing holes and die-cut shapes done in house.",
                   body, faqs)

    # ---------- POS ----------
    p = "/uv-printing/pos-displays"
    body = block(
        '''<h2>What we make</h2>
<ul class="ticks">
<li>Counter and point-of-sale displays</li>
<li>Menu boards and table talkers</li>
<li>Shelf signs and wobblers</li>
<li>Product stands and dispensers</li>
<li>Window and door signs on clear sheet</li>
<li>Packaging prototypes and short-run boxes</li>
</ul>''',
        '''<h2>Printed and made to shape</h2>
<p>Displays often need more than a print. We print the sheet, then cut, crease and fold polypropylene, or weld PVC to make pockets, stands and holders, so the finished display comes from one factory.</p>
<p>Short runs for a store trial are as easy as a national roll-out.</p>''')
    body += gallery([("pos-fruit-talker.jpg","Die-cut printed point-of-sale fruit talker for a fruit shop","Die-cut fruit talker for produce displays"),("printed-polypropylene-sign.jpg","Printed polypropylene counter sign","Printed counter sign")], "Examples from our factory")
    faqs = [
        ("Can you make a prototype first?", "Yes. We can print and make a single display for sign-off before the full run."),
        ("Do you print on card for packaging mock-ups?", "Yes. We print heavy card and board for packaging prototypes and short runs."),
        ("Can you fold and crease plastic displays?", "Yes. We crease and fold polypropylene and weld PVC in house."),
    ]
    desc = "Retail and POS display printing in Brisbane: counter displays, menu boards, shelf signs and packaging prototypes. Printed, cut, creased and welded in house."
    pages[p] = sub(p, "Retail and POS displays", "POS Display & Retail Sign Printing Brisbane", desc,
                   "Retail and point-of-sale display printing",
                   "Counter displays, menu boards, shelf signs and packaging prototypes, printed direct and then cut, creased or welded in our Brisbane factory. From one prototype to a national roll-out.",
                   body, faqs)

    # ---------- PRINTED PLASTIC PRODUCTS ----------
    p = "/uv-printing/printed-plastic-products"
    body = block(
        '''<h2>Full colour without screens</h2>
<p>Screen printing suits long runs in a few spot colours. Flatbed UV printing puts full-colour artwork, photos and gradients onto PVC and polypropylene with no screens to make, so short runs and personalised items cost far less to set up.</p>
<p>We then turn the printed sheet into the finished product with the same equipment we have used for 27 years.</p>''',
        '''<h2>Products we print and make</h2>
<ul class="ticks">
<li>Full-colour folders, binders and presentation covers</li>
<li>Printed wallets, pockets and document holders</li>
<li>Tags, cards, luggage tags and swing tags</li>
<li>Menu covers and hospitality holders</li>
<li>Music and school folders with photo artwork</li>
<li>Printed covers and panels for your own products</li>
</ul>''')
    body += '''<section class="block"><div class="wrap">
<div class="section-head"><h2>Print then make</h2><p class="lede">Every step happens in our Tingalpa factory.</p></div>
<ol class="steps">
<li><h3>Print</h3><p>Full colour and white printed flat onto PVC or polypropylene sheet.</p></li>
<li><h3>Cut</h3><p>Guillotined to size or die cut to shape.</p></li>
<li><h3>Form</h3><p>RF welded, creased and folded, or foil blocked.</p></li>
<li><h3>Fit and pack</h3><p>Ring mechanisms, eyelets, rivets and press studs fitted, then checked and packed.</p></li>
</ol>
</div></section>'''
    faqs = [
        ("When is UV printing better than screen printing?", "For full-colour artwork, photos, gradients and short runs. Screen printing is still the better value for long runs in one or two spot colours. We do both and will recommend the right one."),
        ("Can you print each item differently?", "Yes. Names, numbers or different artwork on each piece cost little extra with flatbed printing."),
        ("What is the minimum run?", "There is no set minimum. We quote samples and short runs per job."),
    ]
    desc = "Full-colour printed PVC and polypropylene products made in Brisbane: folders, binders, wallets, tags and menu covers, printed then cut, welded and assembled in house."
    pages[p] = sub(p, "Printed and fabricated products", "Full-Colour Printed PVC & Polypropylene Products | Brisbane", desc,
                   "Full-colour printed plastic products, made in Brisbane",
                   "We print full colour onto PVC and polypropylene sheet, then cut, weld, crease, foil and assemble it into finished folders, wallets, tags and covers, all in one Brisbane factory.",
                   body, faqs)


    # ---------- OFFICE AND BUSINESS SIGNS ----------
    p = "/uv-printing/office-signs"
    body = block(
        '''<h2>Signs we print</h2>
<ul class="ticks">
<li>Reception and feature wall signs with your logo</li>
<li>Door, room and meeting room signs</li>
<li>Wayfinding and directory boards</li>
<li>Shopfront, window and counter signs</li>
<li>Opening hours, notice and policy boards</li>
<li>Desk plates and staff name plates</li>
<li>Car park and building signs on ACM</li>
</ul>''',
        '''<h2>How it is made</h2>
<ul class="facts">
<li><strong>Printed direct.</strong> Full colour and white ink straight onto acrylic, foamed PVC, ACM or aluminium. No vinyl to lift or peel.</li>
<li><strong>Reverse-printed acrylic.</strong> Your logo printed behind clear acrylic for a glossy, protected face.</li>
<li><strong>Cut in house.</strong> Cut to size and drilled for fixings in our Tingalpa factory.</li>
<li><strong>One sign or a full fit-out.</strong> A single door sign or every sign for a new office, quoted per job.</li>
</ul>
<p>We print and cut the signs. We do not install them, so your builder or fit-out team fits them on site.</p>''')
    faqs = [
        ("What material is best for a reception sign?", "Reverse-printed clear acrylic gives the classic glossy look. Foamed PVC is lighter and costs less. ACM suits large signs and outdoor walls. Tell us the size and where it goes and we will suggest one."),
        ("Can you match our brand colours?", "Yes. Send your brand colours as CMYK or Pantone references and we print a test if an exact match matters."),
        ("Do you install signs?", "No. We print and cut the signs, drilled for fixings if you need them. Your builder, fit-out team or handyman installs them."),
        ("Can you do all the signs for a new office?", "Yes. Send the sign schedule or floor plan with the wording for each sign and we quote the full set."),
    ]
    desc = "Office and business signs printed in Brisbane: reception, door, room and wayfinding signs on acrylic, PVC and ACM. Full colour with white ink. One sign or a full fit-out."
    pages[p] = sub(p, "Office and business signs", "Office, Reception & Wayfinding Signs Brisbane | Printed Acrylic & PVC", desc,
                   "Office, reception and wayfinding signs",
                   "Reception, door, room and wayfinding signs printed in full colour on acrylic, foamed PVC and ACM in our Tingalpa factory. One sign or every sign for a new fit-out.",
                   body, faqs)

    # ---------- SCHOOL SIGNS ----------
    p = "/uv-printing/school-signs"
    body = block(
        '''<h2>Signs for schools</h2>
<ul class="ticks">
<li>Campus maps and wayfinding signs</li>
<li>Building, block and classroom signs</li>
<li>Honour boards, dux and captain boards</li>
<li>Sports, house and trophy displays</li>
<li>Reception and front office signs</li>
<li>Rules, safety and notice boards</li>
<li>Event, open day and fete signs on corflute</li>
</ul>''',
        '''<h2>Already a supplier to schools</h2>
<p>Plastics Unique has made school folders, music folders, student portfolios and certificate pockets for Queensland schools for years. The same factory now prints signs, so your school can order folders and signs from one supplier with one account.</p>
<ul class="facts">
<li><strong>Your crest in full colour.</strong> Printed direct onto acrylic, PVC or ACM, with white ink on clear and dark boards.</li>
<li><strong>Add names each year.</strong> Honour boards can be made as panels so new names are added without replacing the board.</li>
<li><strong>Indoor or outdoor.</strong> ACM and aluminium for outdoor signs, acrylic and PVC indoors.</li>
</ul>''')
    faqs = [
        ("Can you add names to an honour board each year?", "Yes. We can design the board as separate panels or strips so a new panel is printed each year and added to the board."),
        ("Do you supply signs to schools outside Brisbane?", "Yes. We freight Australia-wide. Signs are packed flat and protected for transport."),
        ("Can we order on a school purchase order?", "Yes. Send your purchase order with the quote acceptance."),
    ]
    desc = "School signs printed in Brisbane: campus wayfinding, building and classroom signs, honour boards and sports displays on acrylic, PVC and ACM. From the makers of Plastics Unique school folders."
    pages[p] = sub(p, "School signs and honour boards", "School Signs & Honour Boards Brisbane | Printed Acrylic, PVC & ACM", desc,
                   "School signs and honour boards",
                   "Campus wayfinding, building and classroom signs, honour boards and sports displays printed in full colour on acrylic, PVC and ACM, by the Brisbane factory that makes Plastics Unique school folders.",
                   body, faqs)

    # ---------- HOSPITAL AND CLINIC SIGNS ----------
    p = "/uv-printing/hospital-signs"
    body = block(
        '''<h2>Signs for wards and clinics</h2>
<ul class="ticks">
<li>Ward, room and bed bay signs</li>
<li>Wayfinding and department directories</li>
<li>Reception and nurse station signs</li>
<li>Patient information and notice boards</li>
<li>Door signs for consulting and treatment rooms</li>
<li>Staff-only, restricted area and safety signs</li>
</ul>''',
        '''<h2>From the makers of Sov Services chart folders</h2>
<p>Sov Services has supplied patient chart folders and holders to Australian hospitals since 1994. The same Tingalpa factory now prints ward and wayfinding signs, so your ward can order folders, holders and signs from one supplier.</p>
<ul class="facts">
<li><strong>Smooth, flat faces.</strong> Printed direct onto acrylic, PVC or ACM, with no vinyl edges to lift.</li>
<li><strong>Your colour coding.</strong> Match the colours you already use for wards and departments.</li>
<li><strong>Your standards.</strong> Send your health service's sign templates or style guide and we print to them.</li>
</ul>''')
    faqs = [
        ("Can you match our hospital's sign templates?", "Yes. Send the templates, style guide or a photo of an existing sign and we print to match."),
        ("Can we order signs with our chart folders?", f"Yes. Add the signs to your Sov Services order, or email {SOV_EMAIL} and we quote both together."),
        ("Do you install signs?", "No. We print and cut the signs and drill them for fixings if needed. Your maintenance team installs them."),
    ]
    desc = "Hospital, clinic and aged care signs printed in Brisbane: ward, room and wayfinding signs on acrylic, PVC and ACM. From the makers of Sov Services patient chart folders."
    pages[p] = sub(p, "Hospital and clinic signs", "Hospital, Ward & Clinic Signs | Printed in Brisbane | Sov Services", desc,
                   "Hospital, ward and clinic signs",
                   "Ward, room, wayfinding and notice signs printed in full colour on acrylic, PVC and ACM for hospitals, clinics and aged care, by the Brisbane factory that makes Sov Services chart folders.",
                   body, faqs)

    # ---------- THANKS ----------
    p = "/uv-printing/thanks"
    main = f'''<section class="page-hero"><div class="wrap">
<h1>Thanks. Your print enquiry is in.</h1>
<p class="lede">We check your files and reply with a quote within one business day. If your files are large, reply to our email with a download link.</p>
<div class="btn-row"><a class="btn" href="/uv-printing/">Back to UV Printing</a><a class="btn ghost" href="/">Home</a></div>
</div></section>'''
    pages[p] = page(p, "Enquiry received | Brisbane Plastics Company", "Thank you for your print enquiry.", main, noindex=True)
    return pages
