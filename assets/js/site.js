// Mobile nav
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.querySelector('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});}
})();

// Artwork upload: type and size check before Netlify receives it
(function(){
  var f=document.getElementById('artwork'),err=document.getElementById('artwork-error');
  if(!f)return;
  var MAX=8*1024*1024; // 8 MB: confirm against Netlify's current Forms upload limit
  f.addEventListener('change',function(){
    err.textContent='';
    var file=f.files[0]; if(!file)return;
    if(!/\.(pdf|jpe?g)$/i.test(file.name)){err.textContent='Upload a PDF or JPG file.';f.value='';return;}
    if(file.size>MAX){err.textContent='File is over 8 MB. Email larger files to sales@brisplastics.com.au.';f.value='';}
  });
})();

// ?type=repeat pre-selects the enquiry type on the contact page
(function(){
  var p=new URLSearchParams(location.search).get('type'); if(!p)return;
  var r=document.querySelector('input[name="enquiry_type"][value="'+p+'"]'); if(r)r.checked=true;
})();

// Live chat (Tawk.to). Paste the Property ID from the Tawk dashboard. Blank = no chat loads.
(function(){
  var TAWK_PROPERTY_ID='6adc80751b93b634803314f9', TAWK_WIDGET_ID='1k5mlbjah';
  if(!TAWK_PROPERTY_ID)return;
  window.Tawk_API=window.Tawk_API||{};window.Tawk_LoadStart=new Date();
  var s=document.createElement('script');
  s.async=true;s.src='https://embed.tawk.to/'+TAWK_PROPERTY_ID+'/'+TAWK_WIDGET_ID;
  s.charset='UTF-8';s.setAttribute('crossorigin','*');
  document.body.appendChild(s);
})();

// Google Analytics 4. Paste the Measurement ID (G-XXXXXXX). Blank = nothing loads.
// Thank-you pages (/thanks, /hospital/thanks, /uv-printing/thanks) are the conversion events for Google Ads.
(function(){
  var GA4_ID='G-DDRCCNERYX';
  if(!GA4_ID)return;
  var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA4_ID;document.head.appendChild(s);
  window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
  gtag('js',new Date());gtag('config',GA4_ID);
  // Google Ads conversion 'Request quote': print quote form thank-you page only
  if(/^\/uv-printing\/thanks(\.html)?\/?$/.test(location.pathname)){gtag('event','manual_event_REQUEST_QUOTE',{form:'print-quote'});}
})();

// Contact page: ?product=<slug> from a product page fills in the product
(function(){
  var NAMES={"ring-binders": "Ring binders and lever arch folders", "tab-dividers": "Custom tab dividers and medical ring binders", "slip-boxes": "Slip boxes for ring binders", "presentation-folders": "Presentation folders and covers", "display-folders": "Display books and sample display folders", "clipboard-folders": "Clipboard folders", "notebook-covers": "Pocket notebook covers", "take-5-safety-books": "Take 5 safety books and covers", "tally-books": "Drill pipe tally books and covers", "glovebox-wallets": "Glovebox, service book and dealership wallets", "fuel-card-holders": "Fuel card holders", "pvc-satchels": "PVC satchels and document wallets", "polypropylene-satchels": "Polypropylene satchels and document boxes", "travel-wallets": "Travel wallets", "tab-wallets": "TAB and gaming wallets", "id-tags": "ID tag pockets and card wallets", "luggage-tags": "Branded luggage tags", "noren-tags": "Noren tags and parts bin tags", "signs-and-tags": "Plastic signs, danger tags and isolation tags", "room-compendiums": "Room compendiums and menu books", "food-service-signage": "Food service and point-of-sale signage", "counter-mats": "Counter mats", "x-ray-sleeves": "X-ray protective sleeves", "funeral-folders": "In remembrance folders", "student-portfolios": "Student portfolio folders", "certificate-pockets": "Certificate pockets and folders", "school-folders": "School folders and binders", "music-folders": "Music folders", "promotional-products": "Rulers, plate frames and promotional items", "bean-lids": "32-8 bean lids for polystyrene boxes", "printing-and-finishing": "Printing, colours and finishing"};
  var s=new URLSearchParams(location.search).get('product'); if(!s||!NAMES[s])return;
  var d=document.getElementById('details'); if(d&&!d.value)d.value='Product: '+NAMES[s]+'\n';
  var p=document.getElementById('product'); if(p){var o=document.createElement('option');o.text=NAMES[s];o.selected=true;p.add(o,1);}
})();

// Photo lightbox for product galleries
(function(){
  var links=[].slice.call(document.querySelectorAll('a.lb')); if(!links.length)return;
  var d=document.createElement('dialog'); d.className='lightbox';
  d.innerHTML='<button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous photo">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-next" aria-label="Next photo">›</button>';
  document.body.appendChild(d);
  var img=d.querySelector('img'),cap=d.querySelector('figcaption'),i=0;
  function show(n){i=(n+links.length)%links.length;var a=links[i],t=a.querySelector('img');img.src=a.href;img.alt=t.alt;cap.textContent=t.alt+'  ('+(i+1)+' of '+links.length+')';}
  links.forEach(function(a,n){a.addEventListener('click',function(e){if(!d.showModal)return;e.preventDefault();show(n);d.showModal();});});
  d.querySelector('.lb-close').onclick=function(){d.close();};
  d.querySelector('.lb-prev').onclick=function(){show(i-1);};
  d.querySelector('.lb-next').onclick=function(){show(i+1);};
  d.addEventListener('click',function(e){if(e.target===d)d.close();});
  document.addEventListener('keydown',function(e){if(!d.open)return;if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});
})();
