"""Assign Drive photos to catalogue products. Explicit file selectors win over folder selectors."""
import os, hashlib, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue_data import PRODUCTS
def assign(src, allf):
    md5 = lambda f: hashlib.md5(open(os.path.join(src, f), 'rb').read()).hexdigest()
    used, seen, out = set(), set(), {p['slug']: [] for p in PRODUCTS}
    for folder_pass in (False, True):
        for p in PRODUCTS:
            for sel in p['photos']:
                if sel.endswith('/') != folder_pass: continue
                for f in [x for x in allf if (x.startswith(sel) if folder_pass else x == sel)]:
                    if f in used: continue
                    used.add(f); d = md5(f)
                    if d in seen: continue
                    seen.add(d); out[p['slug']].append(f)
    # keep original folder order within each product
    order = {f: i for i, f in enumerate(allf)}
    for k in out: out[k].sort(key=lambda f: order[f])
    return out, [f for f in allf if f not in used]
if __name__ == '__main__':
    src, lst = sys.argv[1], sys.argv[2]
    allf = [l.rstrip('\n') for l in open(lst) if l.strip()]
    out, un = assign(src, allf)
    print('unassigned', un); print({k: len(v) for k, v in out.items()}, sum(map(len, out.values())))
    json.dump(out, open(sys.argv[3], 'w'), indent=0)
