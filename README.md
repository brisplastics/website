# Brisbane Plastics Company — holding website (v1)

Static site. No build step. GitHub → Netlify → Cloudflare DNS, the same stack as Formfill.

## Go live (about 45 minutes)

1. **GitHub.** Create private repo `AlertifyProjects/bpc-website`. Push this folder to `main`.
2. **Netlify.** Add new site → Import from GitHub → pick the repo. Build command: blank. Publish directory: `.`
3. **Forms.** Netlify → Site → Forms → enable form detection → redeploy. The `quote-request` form appears after the redeploy.
   Then go to Forms → Notifications → Email → `sales@brisplastics.com.au`.
4. **Domain.** Netlify → Domain management → add `brisplastics.com.au` and `www.brisplastics.com.au`. Set the apex as primary.
5. **Cloudflare DNS.**
   - Apex: CNAME `brisplastics.com.au` → `<site>.netlify.app` (Cloudflare flattens it).
   - www: CNAME `www` → `<site>.netlify.app`.
   - Set both to **DNS only (grey cloud)** until Netlify has issued the SSL certificate.
   - **Do not touch the MX or TXT records**, because email runs on them.
6. **Live chat.** Sign up at tawk.to and create a property. Paste the Property ID into `assets/js/site.js` (`TAWK_PROPERTY_ID`), commit, and it deploys.
   Install the Tawk.to app on your phone and set business hours so an offline form shows after hours.
7. **Google.** Search Console → add domain property (verify with a Cloudflare TXT record) → submit `/sitemap.xml`.
   Create a Google Business Profile for Brisbane Plastics Company, Tingalpa.
8. **Test.** Submit a form with a PDF attached. Confirm the email arrives and the file downloads from Netlify.

## Editing

- Every page is plain HTML. Change it, commit, and Netlify redeploys in under a minute.
- Colours and type are set at the top of `assets/css/site.css`.
- Photos go in `assets/img/`. Real factory and product photos are the biggest single improvement to make after 12/10.
