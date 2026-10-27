"""Multi-item quote form for /contact: standard inclusions and extras per product.
Source: Plastics Unique price book (PU_Price_Book_All_Lists_v2_CAI.docx, lists A1 to A22, Oct 2026).
Products not covered by a list show no standard line and no extras."""
from shell import *
from catalogue_data import PRODUCTS, GROUP_ORDER

# desc: what comes as standard. sizes: suggestions for the Size box. extras: physical add-ons only
# (print methods live in the Printing list; sizes in the Size box).
def S(desc, sizes=(), extras=()):
    return {"desc": desc, "sizes": list(sizes), "extras": list(extras)}
STANDARD = {
    "ring-binders": S("Standard coloured PVC with a 2 D-ring from 15 to 65 mm, or a half or full lever arch.",
        ["A4", "A5", "Custom size"],
        ["3 D-ring", "4 D-ring", "Half clear pocket inside front", "Half clear pockets inside front and back", "Welded business card pocket",
         "Welded CD pocket", "Clear overlay on front, back and spine", "Pen loop"]),
    "glovebox-wallets": S("Standard PVC. Clear pocket inside front and back, and 4 business card pockets inside.",
        ["250 × 350 mm open (standard)", "270 × 370 mm open", "270 × 405 mm open", "Custom size"]),
    "travel-wallets": S("Standard PVC. Clear pocket inside front and back.", ["250 × 250 mm open", "240 × 240 mm open", "Custom size"]),
    "tab-wallets": S("Standard PVC. Clear pocket inside front and back.", ["160 × 190 mm open", "Custom size"]),
    "id-tags": S("Conference ID tags in 0.2 mm clear PVC with a clear pocket on one side and 3 lanyard holes. Card wallets have a clear pocket inside front and back.",
        ["Small ID tag 115 × 106 mm", "Large ID tag 115 × 170 mm", "Card wallet 100 × 130 mm open", "Custom size"]),
    "music-folders": S("Clear diagonal pocket inside front and back, and a business card pocket on the outside front, top right.",
        ["555 × 355 mm open (standard)", "A4", "Custom size"]),
    "notebook-covers": S("Standard PVC.", ["Top opening 257 × 85 mm open", "Side opening 125 × 200 mm open", "Side opening 140 × 190 mm open", "Custom size"],
        ["Hard cover (with board)", "Clear overlay front and back", "Clear pages", "Spine weld", "Double thickness PVC", "Notebooks supplied", "Notebooks supplied and inserted"]),
    "tally-books": S("Hard cover with 1200 micron board and a clear pocket inside front and back. Notebook not included.",
        ["Large 198 × 208 mm open", "Small 150 × 200 mm open"],
        ["Foam padding", "Swing pockets", "Exercise book cut down and inserted", "Wiro ruled notebook supplied and inserted"]),
    "clipboard-folders": S("Clipboard clip riveted on the front at the top. Standard PVC with 2400 micron board, or 1.4 mm polypropylene with rounded corners.",
        ["A4 320 × 224 mm", "A5 170 × 230 mm", "Custom size"], ["Folder that closes over the clipboard"]),
    "certificate-pockets": S("Opaque PVC back with a clear PVC front.", ["A4", "Custom size"], ["Cord supplied and assembled", "Gold cord"]),
    "pvc-satchels": S("Standard PVC with a business card pocket.",
        ["V-flap 305 × 390 mm plus flap", "Tear drop 250 × 383 mm plus flap", "Zip 285 × 405 mm plus flap", "Job bag 430 × 325 mm with 100 mm flap", "Custom size"],
        ["Velcro dot (22 mm)", "Job bag: A4 pocket one side", "Job bag: A4 pockets both sides"]),
    "polypropylene-satchels": S("Slot closure, supplied flat. 0.38 mm polypropylene as standard.",
        ["A4 box satchel 10 mm", "A4 box satchel 20 mm", "A4 box satchel 30 mm", "A4 box satchel 40 mm", "A4 envelope", "Custom size"],
        ["0.6 mm polypropylene", "0.8 mm polypropylene"]),
    "luggage-tags": S("Standard PVC luggage tag.", [], ["Name card supplied", "Name card supplied and inserted"]),
    "noren-tags": S("Clear pocket with an 18 mm self-adhesive strip.", ["Standard 75 × 100 mm", "Large 130 × 140 mm", "Small 70 × 70 mm"]),
    "presentation-folders": S("Diary and compendium covers in 0.6 or 0.8 mm polypropylene, clear frosted or coloured.",
        ["242 × 170 mm", "148 × 212 mm", "255 × 210 mm", "296 × 210 mm", "296 × 225 mm", "Custom size"], ["0.8 mm polypropylene", "Clear pockets"]),
    "promotional-products": S("Polypropylene business cards 55 × 90 mm, 0.6 mm white with rounded corners. Mouse mats 208 × 234 mm with a non-slip backing and clear pocket.",
        ["Business card 55 × 90 mm", "Mouse mat 208 × 234 mm", "Custom size"], ["0.8 mm business cards"]),
}
ITEMS_MAX = 8
PRINT_OPTS = "".join(f"<option>{o}</option>" for o in ["No print", "Screen print, 1 colour", "Screen print, 2 colours", "Screen print, 3 or more colours",
    "Full colour (CMYK)", "Full colour plus white", "Foil", "Embossing or debossing", "Encapsulated print", "Not sure"])
PRINT_OPTS = '<option value="">Choose one</option>' + PRINT_OPTS
MATERIALS = ["Standard PVC", "Clear PVC", "Leather-look PVC", "Padded PVC", "Polypropylene", "Clear or frosted polypropylene", "Tarp PVC", "Not sure"]
MAT_OPTS = '<option value="">Choose one</option>' + "".join(f"<option>{m}</option>" for m in MATERIALS)


def product_select(n):
    opts = '<option value="">Choose a product</option>'
    for g in GROUP_ORDER:
        opts += f'<optgroup label="{esc(g)}">' + "".join(
            f'<option data-slug="{p["slug"]}" data-group="{esc(g)}">{esc(p["title"])}</option>'
            for p in PRODUCTS if p["group"] == g) + "</optgroup>"
    opts += ('<optgroup label="Other"><option data-group="sov">Hospital product (Sov Services)</option>'
             '<option data-group="print">UV flatbed printing</option><option>Something else or not sure</option></optgroup>')
    return f'<select id="item_{n}_product" name="item_{n}_product" class="item-product">{opts}</select>'


def L(n, text, for_id):
    """Label with a hidden item number, so each field has a unique name in the submission email."""
    return f'<label for="{for_id}"><span class="vh">Item {n} </span>{text}</label>'

def item_block(n, generic_hint, sov_opts, sov_colours):
    hidden = "" if n == 1 else " hidden"
    remove = "" if n == 1 else '<button type="button" class="item-remove">Remove this item</button>'
    return f'''<div class="item" data-n="{n}"{hidden}>
<div class="item-head"><h3>Item {n}</h3>{remove}</div>
<div class="grid2">
<div class="field full">{L(n, "Product", f"item_{n}_product")}{product_select(n)}
<p class="item-std" hidden></p></div>
<div class="sov-fields field full" hidden><div class="grid2">
<div class="field full">{L(n, "Hospital item", f"item_{n}_sov_item")}<select id="item_{n}_sov_item" name="item_{n}_sov_item" class="sov-item">{sov_opts}</select></div>
<div class="field">{L(n, "Colour", f"item_{n}_sov_colour")}<select id="item_{n}_sov_colour" name="item_{n}_sov_colour" class="sov-colour">{sov_colours}</select></div>
<div class="field">{L(n, "Ward and bed print", f"item_{n}_sov_print")}<input id="item_{n}_sov_print" name="item_{n}_sov_print" placeholder="e.g. Ward 4B, beds 1 to 24"></div>
</div></div>
<div class="pu-fields field full"><div class="grid2">
<div class="field">{L(n, "Size", f"item_{n}_size")}<span class="hint">pick or type</span><input id="item_{n}_size" name="item_{n}_size" list="item_{n}_sizes" placeholder="e.g. A4 or 310 × 240"><datalist id="item_{n}_sizes"></datalist></div>
<div class="field">{L(n, "Material", f"item_{n}_material")}<select id="item_{n}_material" name="item_{n}_material">{MAT_OPTS}</select></div>
<div class="field">{L(n, "Colour", f"item_{n}_colour")}<span class="hint">see our <a href="/products/printing-and-finishing" target="_blank" rel="noopener">colour range</a></span><input id="item_{n}_colour" name="item_{n}_colour" placeholder="e.g. black, navy, clear"></div>
<div class="field">{L(n, "Printing", f"item_{n}_print")}<select id="item_{n}_print" name="item_{n}_print">{PRINT_OPTS}</select></div>
<div class="field"><span class="label">Where is the print?</span><span class="hint">tick all that apply</span>
<div class="choice inline item-pos"><label><input type="checkbox" value="Front"> Front</label><label><input type="checkbox" value="Back"> Back</label><label><input type="checkbox" value="Spine"> Spine</label><label><input type="checkbox" value="Inside"> Inside</label></div>
<input type="hidden" name="item_{n}_print_position" class="item-pos-value"></div>
<div class="field">{L(n, "Ink or foil colour", f"item_{n}_ink")}<span class="hint">e.g. white, gold foil, PMS 286</span><input id="item_{n}_ink" name="item_{n}_ink_colour"></div>
<div class="field full item-extras-wrap" hidden><span class="label">Extras</span><span class="hint">tick any you need</span><div class="choice inline item-extras"></div>
<input type="hidden" name="item_{n}_extras" class="item-extras-value"></div>
</div></div>
<div class="field">{L(n, "Quantity", f"item_{n}_qty")}<span class="hint">list several for price breaks</span><input id="item_{n}_qty" name="item_{n}_quantity" placeholder="e.g. 50, or 50 / 100 / 250"></div>
<div class="field full">{L(n, "Notes or other customisation", f"item_{n}_notes")}<textarea id="item_{n}_notes" name="item_{n}_notes" class="item-notes" style="min-height:80px" placeholder="{generic_hint}"></textarea></div>
</div>
</div>'''


def contact_form(tracking, artwork, optin_html, generic_hint):
    import hospital
    sov_opts = '<option value="">Choose an item</option>' + "".join(
        f'<optgroup label="{esc(g)}">' + "".join(f"<option>{esc(o)}</option>" for o in items) + "</optgroup>" for g, items in hospital.ORDER_CODES)
    sov_colours = '<option value="">Colour</option>' + "".join(f"<option>{n} {c}</option>" for n, c, _ in hospital.FOLDER_COLOURS) + \
        "<option>Black (on request)</option><option>Black gloss</option><option>White gloss</option><option>White</option><option>Not applicable</option>"
    items = "".join(item_block(n, generic_hint, sov_opts, sov_colours) for n in range(1, ITEMS_MAX + 1))
    return f'''<form class="quote" name="quote-request" method="POST" action="/thanks" data-netlify="true" netlify-honeypot="company_website" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="quote-request">
<textarea name="quote_summary" class="hidden" aria-hidden="true" tabindex="-1"></textarea>
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
<fieldset class="repeat-fs" hidden>
<legend>Your repeat order</legend>
<p class="form-note">We pull up your last job, confirm the price and send it back for your OK. Only tell us what has changed.</p>
<div class="grid2">
<div class="field"><label for="repeat_ref">Previous job number, invoice or PO</label><input id="repeat_ref" name="repeat_reference" placeholder="e.g. invoice 12345 or your PO"></div>
<div class="field"><label for="repeat_qty">Quantity this time</label><input id="repeat_qty" name="repeat_quantity" placeholder="e.g. 250"></div>
<div class="field"><label for="repeat_same">Any changes?</label><select id="repeat_same" name="repeat_changes_flag"><option>Exactly the same as last time</option><option>Some changes</option></select></div>
<div class="field"><label for="repeat_product">Product</label><span class="hint">if you know it</span><input id="repeat_product" name="repeat_product" placeholder="e.g. glove box wallets"></div>
<div class="field full repeat-changes" hidden><label for="repeat_changes">What has changed?</label><textarea id="repeat_changes" name="repeat_changes" style="min-height:80px" placeholder="New artwork, different colour, new address, different quantity breaks"></textarea></div>
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
<fieldset class="items-fs">
<legend>Items you have chosen</legend>
<p class="form-note">Products you added with "Add to quote request" appear here. Add more below, up to {ITEMS_MAX} items.</p>
<div class="notice" id="route-sov" hidden><p>Hospital order? The <a href="/hospital/order">hospital order form</a> asks for item code, spine, colour and ward print, so we can quote it straight away.</p></div>
<div class="notice" id="route-print" hidden><p>Printing a sign or panel? The <a href="/uv-printing/#quote">print quote form</a> asks for material, thickness and cutting, so we can quote it straight away.</p></div>
{items}
<button type="button" class="btn ghost" id="add-item">Add another product</button>
</fieldset>
<fieldset>
<legend>Delivery and artwork</legend>
<div class="grid2">
<div class="field"><label for="needed_by">Needed by</label><span class="hint">standard 10 to 15 working days from order and artwork approval</span><input id="needed_by" name="needed_by" type="date"></div>
<div class="field"><label for="postcode">Delivery suburb and postcode</label><span class="hint">for freight</span><input id="postcode" name="delivery_postcode" autocomplete="postal-code" placeholder="e.g. Tingalpa 4173, or collect"></div>
<div class="field"><label for="reference">Your PO number</label><span class="hint">if you have one</span><input id="reference" name="po_number"></div>
<div class="field"></div>
{artwork}
<div class="field full"><label for="details">Anything else we should know</label><textarea id="details" name="details" placeholder="Delivery instructions, deadlines, anything that applies to the whole order"></textarea></div>
{optin_html}
</div>
</fieldset>
{tracking}
<button class="btn" type="submit">Send request</button>
<p class="form-note" style="margin-top:1rem">We reply within one business day. Your details are used only to respond to this request and, if you tick the box, to send you news. See our <a href="/privacy">privacy statement</a>.</p>
</form>'''
