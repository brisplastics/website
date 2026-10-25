"""Resize Drive product photos into the site.
Run: python3 -I process_photos.py "<Drive Product Photos folder>" <photo_list.txt> <site_dir>
Writes assets/img/products/<slug>/<slug>-NN.jpg (max 1600 px) and -NN-t.jpg thumbs (600 px),
plus _src/photo_manifest.json used by the page build."""
import os, sys, json, re
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from assign_photos import assign
from catalogue_data import PRODUCTS

TOKENS = [  # filename fragment -> words for alt text (checked in order)
    ("binderenc", "ring binder with full-colour encapsulated print"), ("bindersp&padding", "padded ring binder with screen print"),
    ("bindersp", "screen printed ring binder"), ("bindesp", "screen printed ring binder"), ("binder3colsp", "ring binder with three-colour screen print"),
    ("binder3dring", "3 D-ring binder"), ("binder4dring", "4 D-ring binder"), ("binderbcpkt", "ring binder with business card pocket"),
    ("binderinside", "inside of a ring binder with pockets"), ("bindersa4", "range of A4 printed ring binders"), ("bindersafety", "safety data sheet ring binder"),
    ("ll&foil", "leather-look binder with foil stamping"), ("ll&sp", "leather-look binder with screen print"), ("llwithsp", "leather-look binder with screen print"),
    ("llinside", "inside of a leather-look binder"), ("slipbox", "binder slip box"), ("magazinebinder", "magazine binder"), ("magazine wires", "magazine binder wires"),
    ("legal binders", "legal ring binder"), ("overlay", "clear overlay presentation binder"), ("penloop", "binder with pen loop"), ("finger ring", "finger ring binder mechanism"),
    ("ring - matt black", "matt black ring mechanism"), ("2mm foam", "padded PVC ring binder"), ("large radius", "binder with large radius corners"),
    ("poly binder", "polypropylene ring binder"), ("display binder", "easel display binder"), ("bse", "foil stamped staff achievement folder"),
    ("4 d 25mm", "4 D-ring 25 mm binder"), ("2 o 13mm", "2 O-ring 13 mm binder"), ("2 'o' 13mm", "2 O-ring 13 mm binder"), ("a44d15mm", "A4 4 D-ring 15 mm binder"),
    ("cardboarddividers", "cardboard tab dividers"), ("polydividers", "polypropylene tab dividers"), ("printeddividers", "printed tab dividers"),
    ("unprinteddividers", "blank tab dividers"), ("treasury", "treasury tag"),
    ("clipboardfolder inside", "inside of a clipboard folder"), ("clipboardfolder", "printed clipboard folder"), ("clipboard metal", "riveted clipboard clip"),
    ("a4 clipboard", "PVC-covered A4 clipboard"),
    ("pnbcsidemulti", "multi-panel side opening notebook cover"), ("pnbcsideinside", "inside of a side opening notebook cover"), ("pnbcside", "side opening notebook cover"),
    ("pnbc side opening", "side opening notebook cover"), ("sideopeninside", "inside of a side opening notebook cover"), ("pnbcenc", "notebook cover with encapsulated print"),
    ("encprint", "notebook cover with encapsulated print"), ("pnbcsp", "screen printed notebook cover"), ("pnbcbcpkt", "notebook cover with business card pocket"),
    ("pnbcinside", "inside of a pocket notebook cover"), ("pnbcemboss", "embossed notebook cover"), ("pnbcsidesoft", "soft side opening notebook cover"),
    ("3 part cover", "three-part notebook cover"), ("swingpockets", "notebook cover with swing pockets"), ("hard cover", "hard notebook cover"),
    ("cmykdigiprint", "full-colour digitally printed notebook cover"), ("pocket notebook covers", "pocket notebook covers"), ("notebook", "pocket notebook cover"),
    ("sn", "Take 5 safety book cover"), ("books", "Take 5 safety books"),
    ("tallybookinsidesewn", "inside of a sewn tally book cover"), ("tallybookoutsidesewn", "sewn tally book cover"), ("tallybook inside", "inside of a tally book cover"),
    ("tallybook outside", "tally book cover"), ("small tallybook", "small tally book cover"), ("cover+book", "tally book cover with refill"), ("with book", "tally book cover with refill"),
    ("full colour digital", "full-colour digitally printed tally book cover"), ("tally", "tally book"),
    ("gbwinside", "inside of a glovebox wallet"), ("gbwenc", "glovebox wallet with encapsulated print"), ("gbw1colsp", "glovebox wallet with one-colour screen print"),
    ("gbw3colsp", "glovebox wallet with three-colour screen print"), ("encapsulated print", "glovebox wallet with encapsulated print"), ("dealership-wallet-cluster", "range of dealership service wallets"),
    ("service wallet", "dealership service and warranty wallet"), ("handover wallet", "vehicle handover wallet"), ("bluewalletwhiteprint", "blue service wallet with white print"),
    ("rma", "printed document wallet"), ("fuelcard", "fuel card holder"),
    ("press stud", "press stud closure on a PVC wallet"), ("zip", "PVC zip satchel"), ("vflap", "V-flap PVC satchel"), ("satchelflap", "PVC satchel with flap"),
    ("tarp", "heavy-duty tarp satchel with eyelets"), ("biohazard", "biohazard spill kit satchel"), ("doculope", "printed document envelope"), ("letter file", "polypropylene letter file"),
    ("polyenv", "polypropylene envelope"), ("scoop", "scoop and scraper"), ("a5 satchel", "A5 PVC satchel"), ("small satchel", "small PVC satchel"), ("satchel various", "range of PVC satchels"),
    ("40mm satchel", "40 mm polypropylene box satchel"), ("a5 poly satchel", "A5 polypropylene satchel"), ("poly colour swatch", "polypropylene colour swatches"),
    ("poly swatch", "polypropylene colour swatches"), ("footlocker", "printed polypropylene shape"), ("nufarm", "printed polypropylene product"), ("satchel", "polypropylene satchel"),
    ("front cover", "travel wallet"), ("travel wallet", "travel wallet and luggage tag"), ("tab", "printed TAB wallet"),
    ("idtag", "clear PVC ID tag pocket"), ("img_1451", "ID tag pocket"), ("luggage tag", "branded luggage tag"), ("lugage tag", "branded luggage tag"),
    ("norenlarge", "large noren tag, 130 × 140 mm"), ("norensmall", "small noren tag, 70 × 70 mm"), ("norenstandard", "standard noren tag, 75 × 100 mm"),
    ("noren tag", "noren tags in three sizes"), ("noren", "noren tags in use on parts bins"),
    ("danger tag", "danger tag"), ("testing tag", "annual testing tag"), ("poly card", "printed polypropylene tag"), ("cpr", "printed CPR guide sign"),
    ("photo 1", "danger sign for RF welders"), ("sign", "printed safety sign"),
    ("roomcomp", "room compendium"), ("hilton", "hotel room compendium"), ("menufolder", "menu folder"), ("room folder", "room folder"), ("diary cover", "foil stamped diary cover"),
    ("interscrews", "folder with interscrews"), ("folder with strap", "folder with strap closure"), ("half clear pocket", "folder with half clear pocket"),
    ("clear slip cover", "clear PVC slip cover"), ("guestinfoemboss", "embossed guest information folder"), ("thumbnail_img_3006", "embossed PVC cover"),
    ("ice cream", "die-cut ice cream sign"), ("fruit talker", "die-cut produce talker"), ("counter mat", "printed counter mat"), ("countermatenc", "encapsulated counter mat"),
    ("2 pt", "two-part student portfolio"), ("3 col screen", "student portfolio with three-colour screen print"), ("1 col screen", "student portfolio with one-colour screen print"),
    ("gold foil", "student portfolio with gold foil print"), ("name card pocket", "student portfolio with name card pocket"), ("adhesive pocket", "student portfolio with adhesive pocket"),
    ("3ptstrip", "three-part student portfolio"),
    ("certificate pocket", "certificate display pocket"), ("certificate folder", "certificate folder"), ("clear pocket", "clear PVC pocket"),
    ("2part folder", "two-part school folder"), ("cd pocket", "punched CD pocket"), ("school folder", "school display folder"), ("schoolfolderinside", "inside of a school display folder"),
    ("group_music", "range of school music folders"), ("inside with card pkt", "music folder with card pocket"), ("insideblue", "inside of a music folder"),
    ("insidegreen", "inside of a music folder"), ("foil", "music folder with foil print"),
    ("a4 folder", "A4 presentation folder"), ("compendium cover", "compendium cover"), ("folder3", "presentation folder"), ("poly folder", "printed polypropylene folder"),
    ("display folder 1 col", "display book with one-colour print"), ("display folder inside", "display book with clear sleeves"),
    ("ruler", "printed ruler"), ("plate frame", "printed number plate frame"), ("door sign", "printed door hanger"),
    ("colour chart", "stock PVC colour chart"), ("screenprint or foil", "screen print and foil stamp options"), ("printer", "screen printing press in our factory"),
    ("wallet", "full-colour printed wallet"), ("digital print", "full-colour digital print"), ("folder", "printed folder"),
]
COLOURS = {"blue poly": "blue polypropylene", "burgundy": "burgundy PVC", "charcoal": "charcoal PVC and polypropylene", "director": "Director leather-look PVC",
           "greens": "green PVC", "marmo": "Marmo PVC", "pink poly": "pink polypropylene", "redcolours": "red PVC", "reds": "red PVC"}

def alt_for(slug, title, f):
    name = os.path.splitext(os.path.basename(f))[0].lower()
    if f.startswith("Colour Chart/") and name in COLOURS:
        return f"Swatches of {COLOURS[name]} colours"
    for k, words in TOKENS:
        if name.startswith(k) or k in name:
            return words[0].upper() + words[1:]
    if "inside" in name:
        return "Inside view: " + title[0].lower() + title[1:]
    return "Custom " + title[0].lower() + title[1:]

def main(src, lst, site):
    allf = [l.rstrip("\n") for l in open(lst) if l.strip()]
    fixes = json.load(open(os.path.join(HERE, "photo_fixes.json")))
    out, _ = assign(src, allf)
    manifest = {}
    for p in PRODUCTS:
        slug = p["slug"]; d = os.path.join(site, "assets/img/products", slug)
        files = [f for f in out[slug] if fixes.get(f) != "exclude"]
        if files: os.makedirs(d, exist_ok=True)
        manifest[slug] = []
        for i, f in enumerate(files, 1):
            im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert("RGB")
            if isinstance(fixes.get(f), int): im = im.rotate(fixes[f], expand=True)
            big = im.copy(); big.thumbnail((1600, 1600))
            base = f"{slug}-{i:02d}"
            big.save(os.path.join(d, base + ".jpg"), quality=80, optimize=True, progressive=True)
            th = im.copy(); th.thumbnail((600, 600))
            th.save(os.path.join(d, base + "-t.jpg"), quality=72, optimize=True, progressive=True)
            manifest[slug].append({"file": base, "w": big.width, "h": big.height, "tw": th.width, "th": th.height,
                                   "alt": alt_for(slug, p["title"], f), "source": f})
    json.dump(manifest, open(os.path.join(HERE, "photo_manifest.json"), "w"), indent=1)
    print(sum(map(len, manifest.values())), "photos")

if __name__ == "__main__":
    main(*sys.argv[1:4])
