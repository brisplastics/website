"""Shared form parts: tracking fields, marketing opt-in, artwork upload, and the general quote form (/contact).
Goal: enough detail on the first submission to quote without going back to the customer."""
from shell import *
from catalogue_data import PRODUCTS, GROUP_ORDER

ART_ACCEPT = ".pdf,.jpg,.jpeg,.png,.ai,.eps,.svg,application/pdf,image/jpeg,image/png,image/svg+xml"
ART_HINT = "PDF, AI, EPS, SVG, PNG or JPG, up to 8 MB"

# Filled by site.js from the visitor's first page this session (Google Ads click ID, UTM tags, old-site redirect flag).
TRACKING = "".join(f'<input type="hidden" name="{n}" value="">' for n in
                   ("landing_page", "referrer", "utm_source", "utm_medium", "utm_campaign", "gclid", "came_from", "quote_list"))

def optin(label="Send me occasional product news and offers by email. You can unsubscribe at any time."):
    return f'<div class="field full"><label class="check"><input type="checkbox" name="news_optin" value="yes"> {label}</label></div>'

def artwork_fields(link=True):
    out = (f'<div class="field"><label for="artwork">Artwork, logo or drawing</label><span class="hint">{ART_HINT}</span>'
           f'<input id="artwork" name="artwork" type="file" accept="{ART_ACCEPT}"><p id="artwork-error" class="error" role="alert"></p></div>')
    if link:
        out += ('<div class="field"><label for="file_link">Or a file link</label><span class="hint">WeTransfer, Dropbox, Drive</span>'
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


import forms_items as _fi
STANDARD = _fi.STANDARD
ITEMS_MAX = _fi.ITEMS_MAX

def contact_form():
    return _fi.contact_form(TRACKING, artwork_fields(), optin(), GENERIC_HINT)
