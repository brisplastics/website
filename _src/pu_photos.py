"""Add product photos from plasticsunique.com.au (studio shots, read 27/10/2026) to the catalogue.
Run: python3 -I pu_photos.py <folder of downloaded PU images> <photo_out site dir>
Puts them first in each product's gallery (the first becomes the card photo). Lifestyle images with stock models are not used."""
import os, sys, json, glob
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
PU = {
    "ring-binders": [("092", "Range of custom printed ring binders"), ("025", "Ring binders with foil and print branding"), ("093", "Ring binder with encapsulated full-colour print")],
    "tab-dividers": [("046", "Ring binders with custom printed tab dividers"), ("014", "Custom printed tab dividers")],
    "notebook-covers": [("043", "Range of printed pocket notebook covers"), ("097", "Screen printed pocket notebook covers"), ("033", "Pocket notebook cover with PVC colour swatch")],
    "music-folders": [("020", "Music folders with foil and screen print, and colour swatches")],
    "take-5-safety-books": [("080", "Take 5 books with top and side opening covers"), ("109", "Top opening Take 5 book covers")],
    "id-tags": [("049", "Printed ID pockets and lanyard tags"), ("089", "Printed student card wallets")],
    "polypropylene-satchels": [("031", "Printed polypropylene satchels and boxes")],
    "student-portfolios": [("060", "Student portfolio folders with foil print and colour swatches")],
    "travel-wallets": [("027", "Printed travel wallets")],
    "clipboard-folders": [("032", "Printed clipboards")],
    "bean-lids": [("085", "32-8 bean lid with polystyrene boxes"), ("108", "Polystyrene produce boxes")],
    "tally-books": [("071", "Printed tally book covers")],
    "tab-wallets": [("087", "Printed TAB wallets")],
    "display-folders": [("084", "Material sample display folders"), ("094", "Material sample display folder")],
    "noren-tags": [("029", "Noren tags in three sizes")],
    "signs-and-tags": [("016", "Printed safety signs and danger tags")],
    "printing-and-finishing": [("099", "Foil printed covers"), ("100", "Debossed covers"), ("098", "Full-colour digital prints"), ("096", "Encapsulated prints"),
                               ("095", "Leather-look PVC colours"), ("102", "Transparent polypropylene colours"), ("103", "Metallic polypropylene colours"),
                               ("104", "Standard polypropylene colours"), ("106", "Tarp PVC colours"), ("107", "PVC colour swatches")],
}

def main(src, site):
    man = json.load(open(os.path.join(HERE, "photo_manifest.json")))
    for slug, items in PU.items():
        d = os.path.join(site, "assets/img/products", slug); os.makedirs(d, exist_ok=True)
        man[slug] = [x for x in man.get(slug, []) if not x["file"].startswith(slug + "-pu-")]
        new = []
        for i, (code, alt) in enumerate(items, 1):
            f = glob.glob(os.path.join(src, code + "_*"))[0]
            im = Image.open(f)
            if im.mode in ("P", "RGBA", "LA"):
                im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg
            im = ImageOps.exif_transpose(im).convert("RGB")
            base = f"{slug}-pu-{i:02d}"
            big = im.copy(); big.thumbnail((1600, 1600)); big.save(os.path.join(d, base + ".jpg"), quality=80, optimize=True, progressive=True)
            th = im.copy(); th.thumbnail((600, 600)); th.save(os.path.join(d, base + "-t.jpg"), quality=74, optimize=True, progressive=True)
            new.append({"file": base, "w": big.width, "h": big.height, "tw": th.width, "th": th.height, "alt": alt, "source": "plasticsunique.com.au: " + os.path.basename(f)[4:]})
        man[slug] = new + man[slug]
    json.dump(man, open(os.path.join(HERE, "photo_manifest.json"), "w"), indent=1)
    print(sum(len(v) for v in PU.values()), "PU photos added")

if __name__ == "__main__":
    main(*sys.argv[1:3])
