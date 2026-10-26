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
    if(!/\.(pdf|jpe?g|png|ai|eps|svg)$/i.test(file.name)){err.textContent='Upload a PDF, AI, EPS, SVG, PNG or JPG file.';f.value='';return;}
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

// Contact page: ?product=<slug> selects the product; the notes hint changes to what we need to quote it
(function(){
  var p=document.getElementById('product'); if(!p)return;
  var HINTS={"Binders and folders": "Ring type and size (e.g. 2 D-ring, 25 mm), spine width, pockets, pen loop, business card slot, printing inside or outside", "Covers and books": "The book or pad it must fit (size or brand), top or side opening, pockets, whether you need refill books", "Wallets and satchels": "Closure (press stud, zip, Velcro or flap), pockets and card slots, gusset or flat, what goes inside", "Tags and cards": "Hole or slot, numbering or variable text, how it attaches (tie, cable tie, lanyard), indoor or outdoor", "Hospitality and healthcare": "Number of rooms or sites, inserts or pages, how and where it is used", "Schools and education": "School logo and colours, year levels, pockets, name card or certificate size", "Other products": "What it is for, where it will be used, and a photo or sample of anything similar"}, GEN="Pockets, fittings, ring size, what it holds, where it will be used, delivery address, deadlines";
  var d=document.getElementById('details'), rs=document.getElementById('route-sov'), rp=document.getElementById('route-print');
  function upd(){var o=p.options[p.selectedIndex],g=o?o.getAttribute('data-group'):'';
    if(d)d.placeholder=HINTS[g]||GEN; if(rs)rs.hidden=g!=='sov'; if(rp)rp.hidden=g!=='print';}
  var s=new URLSearchParams(location.search).get('product');
  if(s){for(var i=0;i<p.options.length;i++){if(p.options[i].getAttribute('data-slug')===s){p.selectedIndex=i;break;}}}
  p.addEventListener('change',upd); upd();
})();

// Lead source: remember the first page, referrer, UTM tags and Google Ads click ID for this visit and add them to every form
(function(){
  var K='bpc_src', src=null;
  try{src=JSON.parse(sessionStorage.getItem(K)||'null');}catch(e){}
  if(!src){var q=new URLSearchParams(location.search);
    src={landing_page:location.pathname+location.search,referrer:document.referrer||'',utm_source:q.get('utm_source')||'',utm_medium:q.get('utm_medium')||'',
         utm_campaign:q.get('utm_campaign')||'',gclid:q.get('gclid')||'',came_from:q.get('from')||''};
    try{sessionStorage.setItem(K,JSON.stringify(src));}catch(e){}}
  [].forEach.call(document.querySelectorAll('form[data-netlify] input[type=hidden]'),function(i){if(src[i.name]!==undefined&&!i.value)i.value=src[i.name];});
  window.BPC_SRC=src;
})();

// Visitors redirected from plasticsunique.com.au or sovservices.net.au see a one-line welcome
(function(){
  var f=(window.BPC_SRC||{}).came_from; if(f!=='pu'&&f!=='sov')return;
  try{if(sessionStorage.getItem('bpc_welcome_closed'))return;}catch(e){}
  var name=f==='pu'?'Plastics Unique':'Sov Services', link=f==='pu'?'/products':'/hospital/';
  var b=document.createElement('div'); b.className='welcome-bar'; b.setAttribute('role','status');
  b.innerHTML='<div class="wrap"><p><strong>'+name+' has a new website.</strong> Same team, same Tingalpa factory, same products, item codes and phone numbers. <a href="'+link+'">Find your product</a></p><button type="button" aria-label="Close">×</button></div>';
  var m=document.getElementById('main'); (m||document.body).insertBefore(b,(m||document.body).firstChild);
  b.querySelector('button').onclick=function(){b.remove();try{sessionStorage.setItem('bpc_welcome_closed','1');}catch(e){}};
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
