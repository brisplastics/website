"""Multi-item quote form for /contact: standard inclusions and extras per product.
Source: Plastics Unique price book (PU_Price_Book_All_Lists_v2_CAI.docx, lists A1 to A22, Oct 2026).
Products not covered by a list show no standard line and no extras."""
from shell import *
from catalogue_data import PRODUCTS, GROUP_ORDER

STANDARD = {
    "ring-binders": ("Standard coloured PVC with a 2 D-ring from 15 to 65 mm, or a half or full lever arch. A4 or A5.",
        ["3 D-ring", "4 D-ring", "Half clear pocket inside front", "Half clear pockets inside front and back", "Welded business card pocket",
         "Welded CD pocket", "Clear overlay on front, back and spine", "Encapsulated print on front, back and spine", "Pen loop", "Print on the back"]),
    "glovebox-wallets": ("250 × 350 mm open, standard PVC. Clear pocket inside front and back, and 4 business card pockets inside.",
        ["Larger size 270 × 370 mm", "Larger size 270 × 405 mm", "Full colour print", "Full colour plus white"]),
    "travel-wallets": ("250 × 250 mm or 240 × 240 mm open, standard PVC. Clear pocket inside front and back.", ["Full colour print on white PVC"]),
    "tab-wallets": ("160 × 190 mm open, standard PVC. Clear pocket inside front and back.", []),
    "id-tags": ("Conference ID tags in 0.2 mm clear PVC with a clear pocket on one side and 3 lanyard holes, small 115 × 106 mm or large 115 × 170 mm. Card wallets are 100 × 130 mm open with a clear pocket inside front and back.",
        ["Large ID tag (115 × 170 mm)", "Card wallet", "Custom size"]),
    "music-folders": ("555 × 355 mm open. Clear diagonal pocket inside front and back, and a business card pocket on the outside front, top right.",
        ["A4 size", "Foil print", "Full colour print", "Full colour plus white"]),
    "notebook-covers": ("Standard PVC. Top opening 257 × 85 mm open, or side opening 125 × 200 mm open.",
        ["Hard cover (with board)", "Clear overlay front and back", "Encapsulated prints", "Clear pages", "Spine weld", "Double thickness PVC",
         "Larger side opening 140 × 190 mm", "Notebooks supplied", "Notebooks supplied and inserted"]),
    "tally-books": ("Hard cover with 1200 micron board and a clear pocket inside front and back. Large 198 × 208 mm or small 150 × 200 mm open. Notebook not included.",
        ["Foam padding", "Swing pockets", "Leather-look PVC", "Exercise book cut down and inserted", "Wiro ruled notebook supplied and inserted", "Full colour print"]),
    "clipboard-folders": ("Clipboard clip riveted on the front at the top. A4 clipboards are 320 × 224 mm in standard PVC with 2400 micron board, or 1.4 mm polypropylene with rounded corners.",
        ["A5 size (170 × 230 mm)", "Polypropylene instead of PVC", "Clipboard folder that closes"]),
    "certificate-pockets": ("A4. Opaque PVC back with a clear PVC front.", ["Cord supplied and assembled", "Gold cord", "Foil print"]),
    "pvc-satchels": ("Standard PVC with a business card pocket. V-flap 305 × 390 mm, tear drop 250 × 383 mm or zip 285 × 405 mm, plus flap. Job bags are 430 × 325 mm with a 100 mm flap and Velcro dot.",
        ["V-flap", "Tear drop flap", "Zip", "Velcro dot (22 mm)", "Job bag, A4 pocket one side", "Job bag, A4 pockets both sides"]),
    "polypropylene-satchels": ("A4 box satchels 220 × 320 mm in 10, 20, 30 or 40 mm capacity, and A4 envelopes, both with slot closure and supplied flat. 0.38 mm polypropylene as standard.",
        ["Box satchel", "Envelope", "0.6 mm polypropylene", "0.8 mm polypropylene"]),
    "luggage-tags": ("Standard PVC luggage tag.", ["Name card supplied", "Name card supplied and inserted"]),
    "noren-tags": ("Clear pocket with an 18 mm self-adhesive strip. Standard 75 × 100 mm, large 130 × 140 mm or small 70 × 70 mm.",
        ["Standard 75 × 100 mm", "Large 130 × 140 mm", "Small 70 × 70 mm"]),
    "presentation-folders": ("Diary and compendium covers in 0.6 or 0.8 mm polypropylene, clear frosted or coloured. Clear pockets available.",
        ["0.8 mm polypropylene", "Clear pockets"]),
    "promotional-products": ("Polypropylene business cards 55 × 90 mm, 0.6 mm white with rounded corners. Mouse mats 208 × 234 mm with a non-slip backing and a clear pocket for your print.",
        ["0.8 mm business cards", "Mouse mat with encapsulated print"]),
}
ITEMS_MAX = 8
PRINT_OPTS = ('<option value="">Choose one</option><option>No print</option><option>1 colour</option><option>2 colours</option>'
              '<option>3 or more colours</option><option>Full colour</option><option>Foil blocking</option><option>Embossing</option><option>Not sure</option>')


def product_select(n):
    opts = '<option value="">Choose a product</option>'
    for g in GROUP_ORDER:
        opts += f'<optgroup label="{esc(g)}">' + "".join(
            f'<option data-slug="{p["slug"]}" data-group="{esc(g)}">{esc(p["title"])}</option>'
            for p in PRODUCTS if p["group"] == g) + "</optgroup>"
    opts += ('<optgroup label="Other"><option data-group="sov">Hospital product (Sov Services)</option>'
             '<option data-group="print">UV flatbed printing</option><option>Something else or not sure</option></optgroup>')
    return f'<select id="item_{n}_product" name="item_{n}_product" class="item-product">{opts}</select>'


def item_block(n, generic_hint):
    hidden = "" if n == 1 else " hidden"
    remove = "" if n == 1 else '<button type="button" class="item-remove">Remove this item</button>'
    return f'''<div class="item" data-n="{n}"{hidden}>
<div class="item-head"><h3>Item {n}</h3>{remove}</div>
<div class="grid2">
<div class="field full"><label for="item_{n}_product">Product</label>{product_select(n)}
<p class="item-std" hidden></p></div>
<div class="field full item-extras-wrap" hidden><span class="label">Extras <span class="hint">tick any you need</span></span><div class="choice inline item-extras"></div>
<input type="hidden" name="item_{n}_extras" class="item-extras-value"></div>
<div class="field"><label for="item_{n}_qty">Quantity <span class="hint">list several for price breaks</span></label><input id="item_{n}_qty" name="item_{n}_quantity" placeholder="e.g. 50, or 50 / 100 / 250"></div>
<div class="field"><label for="item_{n}_size">Size <span class="hint">A4, A5 or W × H mm</span></label><input id="item_{n}_size" name="item_{n}_size" placeholder="e.g. A4 or 310 × 240"></div>
<div class="field"><label for="item_{n}_material">Material and colour <span class="hint">if known</span></label><input id="item_{n}_material" name="item_{n}_material" placeholder="e.g. black PVC, clear, blue polypropylene"></div>
<div class="field"><label for="item_{n}_print">Printing</label><select id="item_{n}_print" name="item_{n}_print">{PRINT_OPTS}</select></div>
<div class="field"><span class="label">Where is the print? <span class="hint">tick all that apply</span></span>
<div class="choice inline item-pos"><label><input type="checkbox" value="Front"> Front</label><label><input type="checkbox" value="Back"> Back</label><label><input type="checkbox" value="Spine"> Spine</label><label><input type="checkbox" value="Inside"> Inside</label></div>
<input type="hidden" name="item_{n}_print_position" class="item-pos-value"></div>
<div class="field"><label for="item_{n}_ink">Ink or foil colour <span class="hint">e.g. white, gold foil, PMS 286</span></label><input id="item_{n}_ink" name="item_{n}_ink_colour"></div>
<div class="field full"><label for="item_{n}_notes">Notes for this item</label><textarea id="item_{n}_notes" name="item_{n}_notes" class="item-notes" style="min-height:80px" placeholder="{generic_hint}"></textarea></div>
</div>
</div>'''


def contact_form(tracking, artwork, optin_html, generic_hint):
    items = "".join(item_block(n, generic_hint) for n in range(1, ITEMS_MAX + 1))
    return f'''<form class="quote" name="quote-request" method="POST" action="/thanks" data-netlify="true" netlify-honeypot="company_website" enctype="multipart/form-data">
<input type="hidden" name="form-name" value="quote-request">
{tracking}
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
<div class="field"><label for="repeat_product">Product <span class="hint">if you know it</span></label><input id="repeat_product" name="repeat_product" placeholder="e.g. glove box wallets"></div>
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
<div class="field"><label for="needed_by">Needed by <span class="hint">standard 10 to 15 working days, express available</span></label><input id="needed_by" name="needed_by" type="date"></div>
<div class="field"><label for="postcode">Delivery suburb and postcode <span class="hint">for freight</span></label><input id="postcode" name="delivery_postcode" autocomplete="postal-code" placeholder="e.g. Tingalpa 4173, or collect"></div>
<div class="field"><label for="reference">Previous job number or your PO <span class="hint">if you have one</span></label><input id="reference" name="reference"></div>
<div class="field"></div>
{artwork}
<div class="field full"><label for="details">Anything else we should know</label><textarea id="details" name="details" placeholder="Delivery instructions, deadlines, anything that applies to the whole order"></textarea></div>
{optin_html}
</div>
</fieldset>
<button class="btn" type="submit">Send request</button>
<p class="form-note" style="margin-top:1rem">We reply within one business day. Your details are used only to respond to this request and, if you tick the box, to send you news. See our <a href="/privacy">privacy statement</a>.</p>
</form>'''
