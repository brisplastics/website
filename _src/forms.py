"""Shared form parts: tracking fields, marketing opt-in, artwork upload, and the general quote form (/contact).
Goal: enough detail on the first submission to quote without going back to the customer."""
from shell import *
from catalogue_data import PRODUCTS, GROUP_ORDER

ART_ACCEPT = ".pdf,.jpg,.jpeg,.png,.ai,.eps,.svg,application/pdf,image/jpeg,image/png,image/svg+xml"
ART_HINT = "PDF, AI, EPS, SVG, PNG or JPG, up to 8 MB"

# Filled by site.js from the visitor's first page this session (Google Ads click ID, UTM tags, old-site redirect flag).
TRACKING = "".join(f'<input type="hidden" name="{n}" value="">' for n in
                   ("landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign", "gclid", "came_from"))

def optin(label="Send me occasional product news and offers by email. You can unsubscribe at any time."):
    return f'<div class="field full"><label class="check"><input type="checkbox" name="news_optin" value="yes"> {label}</label></div>'

def artwork_fields(link=True):
    out = (f'<div class="field"><label for="artwork">Artwork, logo or drawing <span class="hint">{ART_HINT}</span></label>'
           f'<input id="artwork" name="artwork" type="file" accept="{ART_ACCEPT}"><p id="artwork-error" class="error" role="alert"></p></div>')
    if link:
        out += ('<div class="field"><label for="file_link">Or a file link <span class="hint">WeTransfer, Dropbox, Drive</span></label>'
                '<input id="file_link" name="file_link" type="url" placeholder="https://"></div>')
    return out

# What we need to quote each product group in one pass. site.js swaps the notes placeholder to match the product chosen.
GROUP_HINTS = {
    "Binders and folders": "Ring type and size (e.g. 2 D-ring, 25 mm), spine width, pockets, pen loop, business card slot, printing inside or outside",
    "Covers and books": "The book or pad it must fit (size or brand), top or side opening, pockets, whether you need refill books",
    "Wallets and satchels": "Closure (press stud, zip, Velcro or flap), pockets and card slots, gusset or flat, what goes inside",
    "Tags and cards": "Hole or slot, numbering or variable text, how it attaches (tie, cable tie, lanyard), indoor or outdoor",
    "Hospitality and healthcare": "Number of rooms or sites, inserts or pages, how and where it is used",
    "Schools and education": "School logo and colours, year levels, pockets, name card or certificate size",
    "Other products": "What it is for, where it will be used, and a photo or sample of anything similar",
}
GENERIC_HINT = "Pockets, fittings, ring size, what it holds, where it will be used, delivery address, deadlines"

def product_select():
    opts = '<option value="">Choose one</option>'
    for g in GROUP_ORDER:
        opts += f'<optgroup label="{esc(g)}">' + "".join(
            f'<option data-slug="{p["slug"]}" data-group="{esc(g)}">{esc(p["title"])}</option>'
            for p in PRODUCTS if p["group"] == g) + "</optgroup>"
    opts += ('<optgroup label="Other"><option data-group="sov">Hospital product (Sov Services)</option>'
             '<option data-group="print">UV flatbed printing</option><option>Something else or not sure</option></optgroup>')
    return f'<select id="product" name="product">{opts}</select>'

def contact_form():
    return f'''<form class="quote" name="quote-request" method="POST" action="/thanks" data-netlify="true" netlify-honeypot="company_website" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="quote-request">
{TRACKING}
<p class="hidden"><label>Leave this empty <input name="company_website"></label></p>
<fieldset>
<legend>What do you need?</legend>
<div class="choice">
<label><input type="radio" name="enquiry_type" value="quote" checked> A quote for a new job</label>
<label><input type="radio" name="enquiry_type" value="repeat"> Reorder a past job</label>
<label><input type="radio" name="enquiry_type" value="order"> Place an order</label>
<label><input type="radio" name="enquiry_type" value="general"> General enquiry</label>
</div>
</fieldset>
<fieldset>
<legend>Your details</legend>
<div class="grid2">
<div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div class="field"><label for="company">Company or school</label><input id="company" name="company" autocomplete="organization"></div>
<div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="contact_pref">Best way to reach you</label><select id="contact_pref" name="contact_preference"><option>Email</option><option>Phone</option><option>Either</option></select></div>
<div class="field"><label for="past">Ordered from us before?</label><select id="past" name="past_customer"><option value="">Choose one</option><option>Yes, from Plastics Unique</option><option>Yes, from Sov Services</option><option>No, first order</option></select></div>
</div>
</fieldset>
<fieldset>
<legend>The job</legend>
<div class="notice" id="route-sov" hidden><p>Hospital order? The <a href="/hospital/order">hospital order form</a> asks for item code, spine, colour and ward print, so we can quote it straight away.</p></div>
<div class="notice" id="route-print" hidden><p>Printing a sign or panel? The <a href="/uv-printing/#quote">print quote form</a> asks for material, thickness and cutting, so we can quote it straight away.</p></div>
<div class="grid2">
<div class="field full"><label for="product">Product</label>{product_select()}</div>
<div class="field"><label for="quantity">Quantity <span class="hint">list several for price breaks</span></label><input id="quantity" name="quantity" placeholder="e.g. 50, or 50 / 100 / 250"></div>
<div class="field"><label for="size">Size <span class="hint">A4, A5 or W × H mm</span></label><input id="size" name="size" placeholder="e.g. A4 or 310 × 240"></div>
<div class="field"><label for="material">Material and colour <span class="hint">if known</span></label><input id="material" name="material" placeholder="e.g. black PVC, clear, blue polypropylene"></div>
<div class="field"><label for="print">Printing</label>
<select id="print" name="print"><option value="">Choose one</option><option>No print</option><option>1 colour</option><option>2 colours</option><option>3 or more colours</option><option>Full colour</option><option>Foil blocking</option><option>Embossing</option><option>Not sure</option></select></div>
<div class="field"><span class="label">Where is the print? <span class="hint">tick all that apply</span></span>
<div class="choice inline"><label><input type="checkbox" name="print_position[]" value="Front"> Front</label><label><input type="checkbox" name="print_position[]" value="Back"> Back</label><label><input type="checkbox" name="print_position[]" value="Spine"> Spine</label><label><input type="checkbox" name="print_position[]" value="Inside"> Inside</label></div></div>
<div class="field"><label for="ink">Ink or foil colour <span class="hint">e.g. white, gold foil, PMS 286</span></label><input id="ink" name="ink_colour"></div>
<div class="field"><label for="needed_by">Needed by <span class="hint">standard 10 to 15 days, express available</span></label><input id="needed_by" name="needed_by" type="date"></div>
<div class="field"><label for="postcode">Delivery suburb and postcode <span class="hint">for freight</span></label><input id="postcode" name="delivery_postcode" autocomplete="postal-code" placeholder="e.g. Tingalpa 4173, or collect"></div>
<div class="field"><label for="reference">Previous job number or your PO <span class="hint">if you have one</span></label><input id="reference" name="reference"></div>
{artwork_fields()}
<div class="field full"><label for="details">Anything else we should know</label><textarea id="details" name="details" placeholder="{GENERIC_HINT}"></textarea></div>
{optin()}
</div>
</fieldset>
<button class="btn" type="submit">Send request</button>
<p class="form-note" style="margin-top:1rem">We reply within one business day. Your details are used only to respond to this request and, if you tick the box, to send you news. See our <a href="/privacy">privacy statement</a>.</p>
</form>'''
