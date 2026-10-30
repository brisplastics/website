"""Privacy statement and Terms of Trade. Wording drafted 30/10/2026 for Bruce; the liability, ownership and
cancellation clauses are flagged for a lawyer's review before they are relied on."""
from shell import *

UPDATED = "30/10/2026"
EMAIL = "sales@brisplastics.com.au"


def _wrap(h1, intro, body):
    return f'''<main id="main">
<section class="page-hero" style="padding-bottom:2rem"><div class="wrap">
<h1>{h1}</h1>
<p>{intro}</p>
</div></section>
<section class="block" style="padding-top:1rem"><div class="wrap legal">
{body}
<p class="form-note">Last updated {UPDATED}.</p>
</div></section></main>'''


def privacy_main():
    body = f'''<h2>Who we are</h2>
<p>Brisbane Plastics Company Pty Ltd (ABN 14 699 248 658), trading as Plastics Unique and Sov Services, 45a Millennium Place, Tingalpa QLD 4173. In this statement "we" and "us" means Brisbane Plastics Company.</p>

<h2>What we collect</h2>
<ul>
<li>Your name, business or organisation, email, phone, and billing and delivery addresses.</li>
<li>What you ask us to quote, make or deliver, including artwork and files you send us.</li>
<li>Quotes, orders, invoices and payment records. We do not receive or store your full card number (see Card payments below).</li>
<li>Live chat messages, emails and notes of phone calls.</li>
<li>How you use our website: pages visited and how you reached the site (for example a Google Ads click or an email campaign), collected with cookies.</li>
</ul>

<h2>How we use it</h2>
<p>To respond to your enquiry, quote, make and deliver your order, invoice you and take payment, keep a record of your jobs so you can reorder, and meet our tax and legal obligations. We use website reports in aggregate to see which pages and advertising work, not to identify individual visitors. If you tick the news box on a form, we also send occasional product news and offers by email; every email has an unsubscribe link.</p>
<p>We do not sell your information or use it for anything other than doing business with you.</p>

<h2>Who we share it with, and how</h2>
<p>We share only what each provider needs to do its job, through that provider's own secure systems over encrypted connections:</p>
<ul>
<li><strong>Netlify</strong> hosts this website and receives the forms you submit.</li>
<li><strong>Tawk.to</strong> provides live chat.</li>
<li><strong>Google</strong> provides Google Analytics and Google Ads measurement.</li>
<li><strong>Microsoft 365</strong> handles our email.</li>
<li><strong>Xero</strong> holds our customer records, quotes and invoices.</li>
<li><strong>Stripe</strong> processes card payments.</li>
<li><strong>Brevo</strong> sends our email newsletters, only if you opt in.</li>
<li><strong>Couriers and freight carriers</strong> receive your name, delivery address and phone number to deliver your order.</li>
<li><strong>Our accountants and professional advisers</strong>, where they need it to advise us.</li>
</ul>
<p>We also disclose information where the law requires it. Some of these providers store information outside Australia, including in the United States and Europe.</p>

<h2>Card payments</h2>
<p>Card payments made through the payment link on our invoices are processed by Stripe, a PCI DSS Level 1 certified payment provider. Your card details go directly to Stripe; we never see or store your full card number. If you pay by phone, we enter your card details straight into Stripe's secure system and do not write down or keep them.</p>

<h2>How we keep it safe</h2>
<ul>
<li>This website and the services above use encrypted (HTTPS) connections.</li>
<li>Only staff who need your information for their work can access it.</li>
<li>Our business systems are protected by individual logins, strong passwords and multi-factor authentication where the service supports it.</li>
<li>We keep records only as long as we need them for your orders and as Australian tax law requires, then delete or destroy them securely.</li>
</ul>

<h2>Cookies</h2>
<p>Google Analytics and Google Ads use cookies to count visits and enquiries. Live chat uses a cookie to keep your conversation open. You can block or delete cookies in your browser; the website still works without them.</p>

<h2>Access, correction and complaints</h2>
<p>To see, correct or remove the information we hold about you, or to make a privacy complaint, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:0733963744">(07) 3396 3744</a>. We reply within 30 days. If you are not satisfied with our response, you can contact the Office of the Australian Information Commissioner at <a href="https://www.oaic.gov.au" rel="noopener">oaic.gov.au</a>.</p>'''
    return _wrap("Privacy", "How Brisbane Plastics Company collects, uses, shares and protects your information.", body)


def terms_main():
    body = f'''<h2>1. Who we are</h2>
<p>These terms apply to every quote, order and sale by Brisbane Plastics Company Pty Ltd (ABN 14 699 248 658), trading as Plastics Unique and Sov Services ("we", "us"). By accepting a quote or placing an order you agree to these terms. If a quote states something different, the quote applies.</p>

<h2>2. Quotes and prices</h2>
<ul>
<li>Quotes are valid for 7 days unless the quote shows a different expiry date.</li>
<li>Prices are in Australian dollars. Quotes and invoices show GST separately.</li>
<li>Prices are confirmed once we have seen your final approved artwork.</li>
<li>Freight is charged separately unless the quote includes it.</li>
</ul>

<h2>3. Artwork and proofs</h2>
<ul>
<li>Please supply artwork as Illustrator (AI), high-resolution EPS or PDF files, with fonts converted to outlines or included.</li>
<li>New or changed artwork carries a setup charge, shown on your quote, which includes one round of changes.</li>
<li>We send a proof before anything is printed or made. Please check it carefully: once you approve it, we are not responsible for errors in the approved proof.</li>
<li>We match PMS colours as closely as possible, but exact matches cannot be guaranteed, especially on materials other than white, which may need a white print first.</li>
<li>You confirm you have the right to use any logos, images and text you send us for printing.</li>
</ul>

<h2>4. Turnaround and delivery</h2>
<ul>
<li>Standard turnaround is 10 to 15 working days from order and artwork approval. Express turnaround may be available; ask when you order.</li>
<li>Firm delivery dates are set once we receive your order. Delivery dates are estimates; we are not liable for delays caused by carriers or events outside our control.</li>
<li>Please check your order when it arrives and tell us about any damage or shortfall within 7 days.</li>
</ul>

<h2>5. Payment</h2>
<ul>
<li>Payment is due before dispatch, unless we have agreed account terms with you in writing (for example hospitals and approved account customers). Account customers pay by the due date on the invoice.</li>
<li>You can pay by bank transfer (EFT), by Visa or Mastercard through the secure payment link on your invoice, or by phone on <a href="tel:0733963744">(07) 3396 3744</a>. Please use your invoice number as the payment reference.</li>
<li>Card payments are processed securely by Stripe. See our <a href="/privacy">privacy statement</a>.</li>
<li>Goods remain our property until they are paid for in full.</li>
</ul>

<h2>6. Cancellations, returns and refunds</h2>
<ul>
<li>Our products are custom made to your order, so we do not offer refunds or returns for change of mind.</li>
<li>If you cancel an order after you have approved the proof, you pay for the work and materials already used.</li>
<li>If a product is faulty or not what you ordered and approved, tell us and we will repair, replace or refund it.</li>
</ul>

<h2>7. Your rights under the Australian Consumer Law</h2>
<p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. Nothing in these terms excludes, restricts or changes those rights.</p>

<h2>8. Our liability</h2>
<p>To the extent the law allows, our liability for any product is limited to repairing or replacing it, or refunding what you paid for it, and we are not liable for indirect or consequential loss.</p>

<h2>9. General</h2>
<ul>
<li>These terms are governed by the laws of Queensland.</li>
<li>We may update these terms from time to time. The version on this page when you accept a quote or place an order applies to that order.</li>
<li>Questions about these terms: email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:0733963744">(07) 3396 3744</a>.</li>
</ul>'''
    return _wrap("Terms of Trade", "The terms that apply to quotes, orders and payments with Plastics Unique and Sov Services.", body)
