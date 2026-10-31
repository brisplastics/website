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
    if(file.size>MAX){err.textContent='File is over 8 MB. Email larger files to sales@plasticsunique.com.au.';f.value='';}
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

// Lead source: remember the first page, referrer, UTM tags and Google Ads click ID for this visit and add them to every form
(function(){
  var K='bpc_src', src=null;
  try{src=JSON.parse(sessionStorage.getItem(K)||'null');}catch(e){}
  if(!src){var q=new URLSearchParams(location.search);
    src={landing_page:location.pathname+location.search,referrer:document.referrer||'',utm_source:q.get('utm_source')||'',utm_medium:q.get('utm_medium')||'',
         utm_campaign:q.get('utm_campaign')||'',gclid:q.get('gclid')||'',came_from:q.get('from')||''};
    try{sessionStorage.setItem(K,JSON.stringify(src));}catch(e){}}
  var line=['landing '+src.landing_page,src.referrer?'from '+src.referrer.replace(/^https?:\/\//,'').replace(/\/$/,''):'',src.utm_source?'utm '+[src.utm_source,src.utm_medium,src.utm_campaign].filter(Boolean).join(' / '):'',src.gclid?'Google Ads click '+src.gclid:'',src.came_from?'old site '+src.came_from:''].filter(Boolean).join(' | ');
  [].forEach.call(document.querySelectorAll('input[name=lead_source]'),function(i){i.value=line;});
  window.BPC_SRC=src; window.BPC_SRC_LINE=line;
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


// Xero item code and Karen's quote tool sheet for a PU item. Draft mapping (Xero items import of 06/10/2026 and Karens_Quote_Tool_v4); Karen to confirm.
function xeroRef(slug,size,ring,extras){
  size=(size||'').toLowerCase(); ring=(ring||'').toLowerCase(); extras=(extras||'').toLowerCase();
  var custom=/custom/.test(size), a5=/a5/.test(size), m, t08=/0\.8 mm/.test(extras), t06=/0\.6 mm/.test(extras);
  var r=function(code,tool){return {code:code,tool:tool};};
  switch(slug){
    case 'ring-binders':
      if(custom)return r('PU-PB-41117 (custom)','Binders A4');
      var p=a5?'PU-A5-':'PU-A4-', tool=a5?'Binders A5':'Binders A4';
      if((m=/(\d+) mm/.exec(ring)))return (a5&&['15','20','25','38','50','65'].indexOf(m[1])<0)?r('PU-PB-41117 (A5 '+m[1]+' mm not on price list)',tool):r(p+'RING-BINDER-2D-'+m[1],tool);
      if(/lever/.test(ring))return a5?r('PU-PB-41117 (A5 lever arch not on price list)',tool):r('PU-A4-LEVER-ARCH',tool);
      if(/no rings/.test(ring))return r(p+'FOLDER',tool);
      return r(p+'RING-BINDER-2D-(ring size)',tool);
    case 'glovebox-wallets': return custom?r('PU-GBW-41113 (custom)','Glove Box Wallets'):r('PU-GLOVE-BOX-WALLET-STD','Glove Box Wallets');
    case 'travel-wallets': return custom?r('PU-TW-41114 (custom)','Travel Wallets'):r('PU-TRAVEL-WALLET-36','Travel Wallets');
    case 'tab-wallets': return r('PU-TAB-WALLET-78','TAB Wallets');
    case 'id-tags':
      if(/small/.test(size))return r('PU-CONF-ID-TAG-SMALL-203','Conference ID Tags');
      if(/large/.test(size))return r('PU-CONF-ID-TAG-LARGE-34','Conference ID Tags');
      if(/card wallet/.test(size))return r('PU-CARD-WALLET-21','Card Wallets');
      return r('PU-IH-41139 (custom)','Conference ID Tags');
    case 'music-folders': return custom?r('PU-MF-41112 (custom)','Music Folders'):r('PU-MUSIC-FOLDER-341','Music Folders');
    case 'notebook-covers': return custom?r('PU-PNC-41111 (custom)','Pocket Note Book'):r(/hard cover/.test(extras)?'PU-PNBC-TOPSIDE-BOARD':'PU-PNBC-TOPSIDE-NOBOARD','Pocket Note Book');
    case 'tally-books': return /small/.test(size)?r('PU-TALLY-SMALL-UNPRINTED','Tally Covers Small'):r('PU-TALLY-LARGE-UNPRINTED','Tally Covers Large');
    case 'clipboard-folders': return custom?r('PU-POLYCB-41130 or PU-PVCCB-41129 (custom)','Binders A4'):(a5?r('PU-A5-CLIPBOARD-FOLDER','Binders A5'):r('PU-A4-CLIPBOARD-FOLDER','Binders A4'));
    case 'certificate-pockets': return custom?r('PU-CP-41159 (custom)','Certificate Pockets A4'):r(/cord/.test(extras)?'PU-A4-CERTPKT-UNPRINTED-CORD':'PU-A4-CERTPKT-UNPRINTED','Certificate Pockets A4');
    case 'pvc-satchels':
      if(/job bag/.test(size))return r(/both sides/.test(extras)?'PU-JOB-BAG-A4-POCKET-2SIDE':/one side/.test(extras)?'PU-JOB-BAG-A4-POCKET-1SIDE':'PU-JOB-BAG-NO-POCKETS','Job Bags');
      if(/v-flap/.test(size))return r('PU-PVC-SATCHEL-VFLAP-S508','PVC Satchels');
      if(/tear drop/.test(size))return r('PU-PVC-SATCHEL-TEARDROP-8','PVC Satchels');
      if(/zip/.test(size))return r('PU-PVC-SATCHEL-ZIP-85','PVC Satchels');
      return r('PU-PS-41126 (custom)','PVC Satchels');
    case 'polypropylene-satchels':
      var th=t08?'08':t06?'06':'038';
      if(/envelope/.test(size))return r('PU-A4-POLY-ENVELOPE-'+th,'Poly Envelopes A4');
      if(/box satchel/.test(size))return r('PU-A4-POLY-BOX-SATCHEL-'+th,'Poly Box Satchels A4');
      return r('PU-PS-41119 (custom)','Poly Box Satchels A4');
    case 'luggage-tags': return r('PU-LUGGAGE-TAG-39','Luggage Tags');
    case 'noren-tags': return r(/large/.test(size)?'PU-NOREN-TAG-LARGE':/small/.test(size)?'PU-NOREN-TAG-SMALL':'PU-NOREN-TAG-STANDARD','Noren Tag Holders');
    case 'presentation-folders':
      if((m=/(\d+) × (\d+)/.exec(size)))return r('PU-DIARY-COVER-'+(t08?'08':'06')+'PP-'+m[1]+'X'+m[2],'Diary Covers');
      return r('PU-DC-41123 (custom)','Diary Covers');
    case 'promotional-products':
      if(/business card/.test(size))return r('PU-POLY-BUSCARD','Poly Business Cards');
      if(/mouse mat/.test(size))return r('PU-MOUSE-MAT','Mouse Mats');
      return r('PU-MPP-41146 (custom)','');
  }
  return null;
}
// Form emails: every form sends one plain-text "request" block laid out for Xero, plus the email field (for Reply) and any file.
// Radio groups carry data-group instead of a name so they are not listed separately in the email; names are added here
// for the browser to group them and removed again on submit.
var BPCF=(function(){
  [].forEach.call(document.querySelectorAll('input[data-group]'),function(r){r.name=r.getAttribute('data-group');});
  function el(f,id){return f.querySelector('#'+id);}
  function val(f,id){var e=el(f,id);if(!e)return '';if(e.type==='checkbox')return e.checked?'Yes':'';return (e.value||'').trim();}
  function radio(f,g){var e=f.querySelector('input[data-group="'+g+'"]:checked');return e?e.parentNode.textContent.trim():'';}
  function dmy(s){var m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s||'');return m?m[3]+'/'+m[2]+'/'+m[1]:(s||'');}
  function row(L,k,v){if(v)L.push(k+': '+v);}
  // Contact block in the order Xero's new contact screen asks for it
  function contact(L,c){
    var p=(c.name||'').trim().split(/\s+/), first=p.shift()||'', last=p.join(' ');
    L.push('','CONTACT (for Xero)');
    row(L,'Contact name',c.org||c.name); row(L,'First name',first); row(L,'Last name',last);
    row(L,'Email',c.email); row(L,'Phone',c.phone);
    (c.more||[]).forEach(function(x){row(L,x[0],x[1]);});
  }
  function finish(f,subject,L){
    var src=window.BPC_SRC_LINE||'';
    if(src)L.push('','Source: '+src);
    f.querySelector('[name=request]').value=L.join('\n').replace(/\n{3,}/g,'\n\n').trim();
    var s=f.querySelector('[name=subject]'); if(s&&subject)s.value=subject.slice(0,150);
    [].forEach.call(f.querySelectorAll('input[data-group]'),function(r){r.removeAttribute('name');});
  }
  function plural(n,w){return n+' '+w+(n===1?'':'s');}
  return {el:el,val:val,radio:radio,dmy:dmy,row:row,contact:contact,finish:finish,plural:plural};
})();

// Quote request: "Add to quote request" buttons collect products (kept in this browser only).
// On /contact each chosen product becomes an item block with its standard inclusions and extras.
// On /hospital/order chosen Sov products fill the order lines.
(function(){
  var STANDARD={"ring-binders": {"desc": "Standard coloured PVC with a 2 D-ring from 15 to 65 mm, or a half or full lever arch.", "sizes": ["A4", "A5", "Custom size"], "extras": ["3 D-ring", "4 D-ring", "Half clear pocket inside front", "Half clear pockets inside front and back", "Welded business card pocket", "Welded CD pocket", "Clear overlay on front, back and spine", "Internal clear pages", "Pen loop"], "rings": ["2 D-ring 15 mm", "2 D-ring 20 mm", "2 D-ring 25 mm", "2 D-ring 32 mm", "2 D-ring 38 mm", "2 D-ring 45 mm", "2 D-ring 50 mm", "2 D-ring 65 mm", "Half lever arch", "Full lever arch", "No rings (folder only)", "Not sure"]}, "glovebox-wallets": {"desc": "Standard PVC. Clear pocket inside front and back, and 4 business card pockets inside.", "sizes": ["250 × 350 mm open (standard)", "270 × 370 mm open", "270 × 405 mm open", "Custom size"], "extras": [], "rings": []}, "travel-wallets": {"desc": "Standard PVC. Clear pocket inside front and back.", "sizes": ["250 × 250 mm open", "240 × 240 mm open", "Custom size"], "extras": [], "rings": []}, "tab-wallets": {"desc": "Standard PVC. Clear pocket inside front and back.", "sizes": ["160 × 190 mm open", "Custom size"], "extras": [], "rings": []}, "id-tags": {"desc": "Conference ID tags in 0.2 mm clear PVC with a clear pocket on one side and 3 lanyard holes. Card wallets have a clear pocket inside front and back.", "sizes": ["Small ID tag 115 × 106 mm", "Large ID tag 115 × 170 mm", "Card wallet 100 × 130 mm open", "Custom size"], "extras": [], "rings": []}, "music-folders": {"desc": "Clear diagonal pocket inside front and back, and a business card pocket on the outside front, top right.", "sizes": ["555 × 355 mm open (standard)", "A4", "Custom size"], "extras": [], "rings": []}, "notebook-covers": {"desc": "Standard PVC.", "sizes": ["Top opening 257 × 85 mm open", "Side opening 125 × 200 mm open", "Side opening 140 × 190 mm open", "Custom size"], "extras": ["Hard cover (with board)", "Clear overlay front and back", "Clear pages", "Spine weld", "Double thickness PVC", "Pen loop", "Notebooks supplied", "Notebooks supplied and inserted"], "rings": []}, "tally-books": {"desc": "Hard cover with 1200 micron board and a clear pocket inside front and back. Notebook not included.", "sizes": ["Large 198 × 208 mm open", "Small 150 × 200 mm open"], "extras": ["Foam padding", "Swing pockets", "Exercise book cut down and inserted", "Wiro ruled notebook supplied and inserted"], "rings": []}, "clipboard-folders": {"desc": "Clipboard clip riveted on the front at the top. Standard PVC with 2400 micron board, or 1.4 mm polypropylene with rounded corners.", "sizes": ["A4 320 × 224 mm", "A5 170 × 230 mm", "Custom size"], "extras": ["Folder that closes over the clipboard"], "rings": []}, "certificate-pockets": {"desc": "Opaque PVC back with a clear PVC front.", "sizes": ["A4", "Custom size"], "extras": ["Cord supplied and assembled", "Gold cord"], "rings": []}, "pvc-satchels": {"desc": "Standard PVC with a business card pocket.", "sizes": ["V-flap 305 × 390 mm plus flap", "Tear drop 250 × 383 mm plus flap", "Zip 285 × 405 mm plus flap", "Job bag 430 × 325 mm with 100 mm flap", "Custom size"], "extras": ["Velcro dot (22 mm)", "Job bag: A4 pocket one side", "Job bag: A4 pockets both sides"], "rings": []}, "polypropylene-satchels": {"desc": "Slot closure, supplied flat. 0.38 mm polypropylene as standard.", "sizes": ["A4 box satchel 10 mm", "A4 box satchel 20 mm", "A4 box satchel 30 mm", "A4 box satchel 40 mm", "A4 envelope", "Custom size"], "extras": ["0.6 mm polypropylene", "0.8 mm polypropylene"], "rings": []}, "luggage-tags": {"desc": "Standard PVC luggage tag.", "sizes": [], "extras": ["Name card supplied", "Name card supplied and inserted"], "rings": []}, "noren-tags": {"desc": "Clear pocket with an 18 mm self-adhesive strip.", "sizes": ["Standard 75 × 100 mm", "Large 130 × 140 mm", "Small 70 × 70 mm"], "extras": [], "rings": []}, "presentation-folders": {"desc": "Diary and compendium covers in 0.6 or 0.8 mm polypropylene, clear frosted or coloured.", "sizes": ["242 × 170 mm", "148 × 212 mm", "255 × 210 mm", "296 × 210 mm", "296 × 225 mm", "Custom size"], "extras": ["0.8 mm polypropylene", "Clear pockets"], "rings": []}, "promotional-products": {"desc": "Polypropylene business cards 55 × 90 mm, 0.6 mm white with rounded corners. Mouse mats 208 × 234 mm with a non-slip backing and clear pocket.", "sizes": ["Business card 55 × 90 mm", "Mouse mat 208 × 234 mm", "Custom size"], "extras": ["0.8 mm business cards"], "rings": []}}, HINTS={"Binders and folders": "Ring type and size (e.g. 2 D-ring, 25 mm), spine width, pockets, pen loop, business card slot, printing inside or outside", "Covers and books": "The book or pad it must fit (size or brand), top or side opening, pockets, whether you need refill books", "Wallets and satchels": "Closure (press stud, zip, Velcro or flap), pockets and card slots, gusset or flat, what goes inside", "Tags and cards": "Hole or slot, numbering or variable text, how it attaches (tie, cable tie, lanyard), indoor or outdoor", "Hospitality and healthcare": "Number of rooms or sites, inserts or pages, how and where it is used", "Schools and education": "School logo and colours, year levels, pockets, name card or certificate size", "Other products": "What it is for, where it will be used, and a photo or sample of anything similar"}, GENERIC="Pockets, fittings, ring size, what it holds, where it will be used, delivery address, deadlines";
  var K='bpc_quote', list=[];
  function load(){try{list=JSON.parse(localStorage.getItem(K)||'[]')||[];}catch(e){list=[];}}
  function save(){try{localStorage.setItem(K,JSON.stringify(list));}catch(e){}}
  function has(k){return list.some(function(x){return x.key===k;});}
  function drop(k){list=list.filter(function(x){return x.key!==k;});save();}
  load();
  var path=location.pathname;
  if(/\/thanks(\.html)?\/?$/.test(path)){list=[];save();return;}
  var onContact=/^\/contact/.test(path), onOrder=/^\/hospital\/order/.test(path);

  // Floating link to the chosen items
  var pill=document.createElement('a'); pill.className='quote-pill';
  document.body.appendChild(pill);
  function renderButtons(){
    var sovOnly=list.length&&list.every(function(x){return x.key.indexOf('sov:')===0;});
    pill.href=sovOnly?'/hospital/order':'/contact';
    pill.textContent='Your chosen items ('+list.length+')';
    pill.hidden=!list.length||onContact||onOrder;
    [].forEach.call(document.querySelectorAll('.add-quote'),function(b){
      var on=has(b.getAttribute('data-key'));
      b.textContent=on?'Added to quote request':'Add to quote request'; b.classList.toggle('on',on);});
    [].forEach.call(document.querySelectorAll('input[name=quote_list]'),function(i){i.value=list.map(function(x){return x.name;}).join('\n');});
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.add-quote'); if(!b)return;
    var k=b.getAttribute('data-key');
    if(has(k))drop(k); else {list.push({key:k,name:b.getAttribute('data-name')});save();}
    renderButtons();
  });
  renderButtons();

  // ---- /contact: item blocks (general products only; hospital and UV printing have their own forms) ----
  var form=document.querySelector('form[name=quote-request]');
  if(form){
    var items=[].slice.call(form.querySelectorAll('.item')), addBtn=document.getElementById('add-item');
    function opt(sel){return sel.options[sel.selectedIndex];}
    function v(div,suffix){var e=div.querySelector('#item_'+div.getAttribute('data-n')+'_'+suffix);return e?e.value.trim():'';}
    function checked(div,cls){return [].map.call(div.querySelectorAll(cls+' input:checked'),function(c){return c.value;}).join(', ');}
    function onProduct(div){
      var o=opt(div.querySelector('.item-product'));
      if(o&&o.getAttribute('data-go')){location.href=o.getAttribute('data-go');return;}
      var slug=o?o.getAttribute('data-slug'):'', g=o?o.getAttribute('data-group'):'';
      var std=STANDARD[slug], p=div.querySelector('.item-std'), wrap=div.querySelector('.item-extras-wrap'), box=div.querySelector('.item-extras');
      if(std){p.textContent='Comes with: '+std.desc; p.hidden=false;} else {p.textContent=''; p.hidden=true;}
      var dl=div.querySelector('datalist'), sizes=(std&&std.sizes)||[]; dl.innerHTML='';
      sizes.forEach(function(x){var op=document.createElement('option');op.value=x;dl.appendChild(op);});
      div.querySelector('.size-hint').textContent=sizes.length?'pick from the list or type':'W × H mm';
      var rw=div.querySelector('.item-ring-wrap'), rs=div.querySelector('#item_'+div.getAttribute('data-n')+'_ring'), rings=(std&&std.rings)||[], rk=rs.value;
      rs.innerHTML='<option value="">Choose one</option>'; rings.forEach(function(x){var op=document.createElement('option');op.text=x;rs.add(op);}); rs.value=rk; rw.hidden=!rings.length;
      var keep=checked(div,'.item-extras').split(', ');
      box.innerHTML='';
      if(std&&std.extras.length){
        std.extras.forEach(function(x){var l=document.createElement('label');var c=document.createElement('input');c.type='checkbox';c.value=x;c.checked=keep.indexOf(x)>=0;l.appendChild(c);l.appendChild(document.createTextNode(' '+x));box.appendChild(l);});
        wrap.hidden=false;
      } else wrap.hidden=true;
      div.querySelector('.item-notes').placeholder=HINTS[g]||GENERIC;
    }
    function show(div){div.hidden=false; addBtn.hidden=items.every(function(d){return !d.hidden;});}
    function selectSlug(div,slug){var s=div.querySelector('.item-product');for(var i=0;i<s.options.length;i++){if(s.options[i].getAttribute('data-slug')===slug){s.selectedIndex=i;break;}}onProduct(div);}
    items.forEach(function(div){
      div.querySelector('.item-product').addEventListener('change',function(){onProduct(div);});
      var r=div.querySelector('.item-remove');
      if(r)r.addEventListener('click',function(){
        var k=div.getAttribute('data-key'); if(k){drop(k);div.removeAttribute('data-key');renderButtons();}
        [].forEach.call(div.querySelectorAll('input,select,textarea'),function(f){if(f.type==='checkbox')f.checked=false;else if(f.tagName==='SELECT')f.selectedIndex=0;else f.value='';});
        onProduct(div); div.hidden=true; addBtn.hidden=false;
      });
    });
    addBtn.addEventListener('click',function(){var d=items.filter(function(x){return x.hidden;})[0]; if(d){show(d); d.querySelector('.item-product').focus();}});
    // Fill from ?product= and from the chosen items. Hospital items belong on the hospital order form.
    var q=new URLSearchParams(location.search).get('product');
    var queue=list.filter(function(x){return x.key.indexOf('pu:')===0;});
    if(q&&!queue.some(function(x){return x.key==='pu:'+q;}))queue.unshift({key:'pu:'+q,fromLink:true});
    queue.slice(0,items.length).forEach(function(x,i){var div=items[i]; show(div); if(!x.fromLink)div.setAttribute('data-key',x.key); selectSlug(div,x.key.slice(3));});
    document.getElementById('route-sov').hidden=!list.some(function(x){return x.key.indexOf('sov:')===0;});
    items.forEach(function(d){if(!d.hidden)onProduct(d);});

    // On send: one plain block for the email, contact details first, then one line per item ready for a Xero quote line
    form.addEventListener('submit',function(){
      var F=BPCF, f=form, L=[], val=function(id){return F.val(f,id);};
      var kind=(f.querySelector('input[data-group=enquiry_type]:checked')||{}).value||'quote';
      var who=val('company')||val('name'), n=0, subject;
      var KIND={quote:'QUOTE REQUEST',repeat:'REPEAT ORDER',order:'ORDER',general:'GENERAL ENQUIRY'};
      var head=[KIND[kind]||'REQUEST'];
      var needed=F.dmy(val('needed_by'));
      var lines=[];
      if(kind==='repeat'){
        lines.push('','REPEAT ORDER');
        F.row(lines,'Previous job, invoice or PO',val('repeat_ref')); F.row(lines,'Product',val('repeat_product'));
        F.row(lines,'Quantity',val('repeat_qty')); F.row(lines,'Changes',val('repeat_same')); F.row(lines,'What has changed',val('repeat_changes'));
        subject='Repeat order: '+who+(val('repeat_ref')?', ref '+val('repeat_ref'):'');
      } else {
        lines.push('','ITEMS (one Xero quote line each)');
        items.forEach(function(div){
          if(div.hidden)return; var ps=div.querySelector('.item-product'); if(!ps.value)return; n++;
          var pr=v(div,'print'), pos=checked(div,'.item-pos'), ink=v(div,'ink'), ex=checked(div,'.item-extras');
          var printing=pr?pr+(pos?' on '+pos.toLowerCase():'')+(ink?', ink '+ink:''):'';
          var desc=[opt(ps).text,v(div,'size'),v(div,'ring'),v(div,'material'),v(div,'colour'),printing,ex].filter(function(x){return x&&!/^Choose/.test(x);}).join(', ');
          lines.push('',n+'. Qty '+(v(div,'qty')||'not given'));
          lines.push('   '+desc);
          var xr=xeroRef(opt(ps).getAttribute('data-slug'),v(div,'size'),v(div,'ring'),ex);
          if(xr)lines.push('   Xero: '+xr.code+'  |  Quote tool: '+xr.tool);
          if(v(div,'notes'))lines.push('   Notes: '+v(div,'notes'));
        });
        if(!n)lines.push('No product chosen');
        head.push(F.plural(n,'item'));
        subject=(kind==='order'?'Order: ':kind==='general'?'Enquiry: ':'Quote request: ')+who+(n?', '+F.plural(n,'item'):'');
      }
      if(needed){head.push('needed by '+needed);subject+=', needed '+needed;}
      L.push(head.join(' · '));
      F.contact(L,{org:val('company'),name:val('name'),email:val('email'),phone:val('phone'),more:[
        ['Delivery suburb and postcode',val('postcode')],['Customer PO',val('reference')],
        ['Prefers',val('contact_pref')],['Ordered before',val('past')]]});
      L=L.concat(lines);
      var other=[]; F.row(other,'File link',val('file_link')); F.row(other,'Notes',val('details')); F.row(other,'News opt-in',val('news_optin'));
      if(other.length)L=L.concat(['','OTHER'],other);
      F.finish(f,subject,L);
    });
  }

  // ---- /hospital/order: fill order lines from chosen Sov products ----
  var ord=document.querySelector('form[name=hospital-order]');
  if(ord){
    var lines=[].slice.call(ord.querySelectorAll('tr.order-line')), addLine=document.getElementById('add-line');
    var MAP={}; try{MAP=JSON.parse(document.getElementById('order-map').textContent);}catch(e){}
    function refreshAdd(){if(addLine)addLine.hidden=lines.every(function(r){return !r.hidden;});}
    function freeLine(){for(var i=0;i<lines.length;i++){var s=lines[i].querySelector('.ol-item');if(!s.value){lines[i].hidden=false;refreshAdd();return s;}}return null;}
    function pick(sel,text){for(var j=0;j<sel.options.length;j++){if(sel.options[j].text===text||sel.options[j].text.indexOf(text)===0){sel.selectedIndex=j;return true;}}return false;}
    if(addLine)addLine.addEventListener('click',function(){var r=lines.filter(function(x){return x.hidden;})[0];if(r){r.hidden=false;r.querySelector('.ol-item').focus();}refreshAdd();});
    var left=[], wanted=[];
    var it=new URLSearchParams(location.search).get('item'); if(it&&MAP[it])wanted.push({text:MAP[it]});
    list.filter(function(x){return x.key.indexOf('sov:')===0;}).forEach(function(x){
      var id=x.key.slice(4); if(id===it)return;
      wanted.push(MAP[id]?{text:MAP[id]}:{name:x.name});
    });
    wanted.forEach(function(w){
      if(!w.text){left.push(w.name);return;}
      var s=freeLine(); if(!s||!pick(s,w.text))left.push(w.text);
    });
    if(left.length){var n=ord.querySelector('#notes'); if(n&&!n.value)n.value='Also: '+left.join('; ');}
    refreshAdd();
  }
})();

// Products page finder: filter cards by name, description or item code
(function(){
  var q=document.getElementById('prod-search'); if(!q)return;
  var cards=[].slice.call(document.querySelectorAll('.pgroup li')), count=document.getElementById('prod-count');
  q.addEventListener('input',function(){
    var t=q.value.trim().toLowerCase(), n=0;
    cards.forEach(function(li){var hit=!t||li.textContent.toLowerCase().indexOf(t)>=0;li.hidden=!hit;if(hit)n++;});
    [].forEach.call(document.querySelectorAll('.pgroup'),function(s){s.hidden=t&&!s.querySelector('li:not([hidden])');});
    count.textContent=t?(n+' matching product'+(n===1?'':'s')):'';
    clearTimeout(q._t); q._t=setTimeout(function(){var f=document.querySelector('.pgroup:not([hidden])');
      if(t&&f){var r=f.getBoundingClientRect(); if(r.top>window.innerHeight*0.6)window.scrollBy({top:r.top-120,behavior:'smooth'});}},600);
  });
})();

// Long galleries: show the first 12 photos, then all on request
(function(){
  [].forEach.call(document.querySelectorAll('.show-photos'),function(b){
    b.addEventListener('click',function(){var g=b.closest('.wrap').querySelector('.gallery');
      [].forEach.call(g.querySelectorAll('.more-photo'),function(f){f.hidden=false;}); b.parentNode.remove();});
  });
})();

// Repeat orders: show the short repeat fields instead of the full item specification
(function(){
  var f=document.querySelector('form[name=quote-request]'); if(!f)return;
  var rep=f.querySelector('.repeat-fs'), items=f.querySelector('.items-fs'), ref=f.querySelector('#repeat_ref');
  var flag=f.querySelector('#repeat_same'), chg=f.querySelector('.repeat-changes');
  function upd(){
    var r=(f.querySelector('input[name=enquiry_type]:checked')||{}).value==='repeat';
    rep.hidden=!r; items.hidden=r; ref.required=r;
    chg.hidden=flag.value.indexOf('Some')<0;
  }
  f.addEventListener('change',function(e){if(e.target.name==='enquiry_type'||e.target===flag)upd();});
  upd();
})();

// Hospital order form: colour choices follow the item chosen on each line
(function(){
  var ord=document.querySelector('form[name=hospital-order]'); if(!ord)return;
  var FOLDER=['Oxford Blue 01','Red 02','Yellow 03','Purple 04','Navy 06','Grey 07','Orange 09','Pink 10','Apple Green 11','Sky Blue 13','Black (on request)'];
  function allowed(t){
    t=t.toLowerCase();
    if(!t)return null;
    if(t.indexOf('holder')>=0)return ['Black gloss','White gloss'];
    if(t.indexOf('clipboard')>=0)return ['White'];
    if(t.indexOf('chest support')>=0)return ['Clear'];
    if(t.indexOf('custom tab divider')>=0)return ['Standard colours (white, red, orange, green, yellow)','Another colour from the range (add it to the notes)'];
    if(t.indexOf('divider')>=0)return ['Not applicable'];
    return FOLDER;
  }
  [].forEach.call(ord.querySelectorAll('tr.order-line'),function(row){
    var item=row.querySelector('.ol-item'), col=row.querySelector('.ol-colour');
    var all=[].map.call(col.options,function(o){return o.text;});
    function upd(){
      var a=allowed(item.options[item.selectedIndex].value?item.options[item.selectedIndex].text:''), keep=col.value;
      col.innerHTML='';
      var list=a||all.slice(1);
      var o0=document.createElement('option');o0.value='';o0.text='Colour';col.add(o0);
      list.forEach(function(t){var o=document.createElement('option');o.text=t;col.add(o);});
      if(list.length===1)col.selectedIndex=1; else if(list.indexOf(keep)>=0)col.value=keep;
    }
    item.addEventListener('change',upd); upd();
  });
})();

// Hospital order form email
(function(){
  var f=document.querySelector('form[name=hospital-order]'); if(!f)return;
  f.addEventListener('submit',function(){
    var F=BPCF, val=function(id){return F.val(f,id);}, L=[], n=0, items=['','ITEMS (one Xero line each)'];
    [].forEach.call(f.querySelectorAll('tr.order-line'),function(r){
      var it=r.querySelector('.ol-item'); if(!it.value)return; n++;
      var c=r.querySelector('.ol-colour').value, pf=r.querySelector('.ol-front').value.trim(), ps=r.querySelector('.ol-spine').value.trim(), q=r.querySelector('.ol-qty').value.trim();
      items.push('',n+'. Qty '+(q||'not given'),'   '+[it.options[it.selectedIndex].text,c&&c!=='Not applicable'?c:'',pf?'front: '+pf:'',ps?'spine: '+ps:''].filter(Boolean).join(', '));
    });
    var type=F.radio(f,'order_type'), needed=F.dmy(val('needed_by'));
    L.push(['HOSPITAL ORDER',type,F.plural(n,'line'),needed?'needed by '+needed:''].filter(Boolean).join(' · '));
    F.contact(L,{org:val('facility'),name:val('name'),email:val('email'),phone:val('phone'),more:[
      ['Ward or department',val('ward')],['Delivery address',val('delivery').replace(/\s*\n\s*/g,', ')],['Customer PO',val('po')]]});
    L=L.concat(items);
    var other=[]; F.row(other,'Notes',val('notes')); F.row(other,'Send vendor details to supply team',val('new_supplier_details'));
    if(other.length)L=L.concat(['','OTHER'],other);
    var kind=(f.querySelector('input[data-group=order_type]:checked')||{}).value;
    F.finish(f,'Hospital '+(kind==='reorder'?'reorder':kind==='quote'?'quote':'order')+': '+[val('facility'),val('ward')].filter(Boolean).join(', ')+', '+F.plural(n,'line')+(needed?', needed '+needed:''),L);
  });
})();

// UV print quote email
(function(){
  var f=document.querySelector('form[name=print-quote]'); if(!f)return;
  f.addEventListener('submit',function(){
    var F=BPCF, val=function(id){return F.val(f,id);}, L=[], needed=F.dmy(val('pq-date'));
    var size=val('pq-size'), th=val('pq-thick');
    L.push(['UV PRINT QUOTE',F.radio(f,'customer_type').split(' (')[0],needed?'needed by '+needed:''].filter(Boolean).join(' · '));
    F.contact(L,{org:val('pq-company'),name:val('pq-name'),email:val('pq-email'),phone:val('pq-phone'),more:[['Delivery suburb and postcode',val('pq-post')]]});
    L.push('','JOB (Xero quote line)','','1. Qty '+(val('pq-qty')||'not given'),
      '   '+['UV print: '+val('pq-use'),size?size+' mm':'',th?th+' mm thick':'',val('pq-material'),'material: '+val('pq-supply').toLowerCase(),val('pq-sides'),val('pq-cut'),val('pq-where').toLowerCase()].filter(Boolean).join(', '));
    var other=[]; F.row(other,'Repeat work',val('pq-repeat')); F.row(other,'File link',val('file_link')); F.row(other,'Notes',val('pq-notes')); F.row(other,'News opt-in',val('news_optin')); F.row(other,'Form page',val('pq-page'));
    L=L.concat(['','OTHER'],other);
    F.finish(f,'UV print quote: '+(val('pq-company')||val('pq-name'))+', '+val('pq-use')+(needed?', needed '+needed:''),L);
  });
})();
