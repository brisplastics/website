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

// Quote request: "Add to quote request" buttons collect products (kept in this browser only).
// On /contact each chosen product becomes an item block with its standard inclusions and extras.
// On /hospital/order chosen Sov products fill the order lines.
(function(){
  var STANDARD={"ring-binders": {"desc": "Standard coloured PVC with a 2 D-ring from 15 to 65 mm, or a half or full lever arch.", "sizes": ["A4", "A5", "Custom size"], "extras": ["3 D-ring", "4 D-ring", "Half clear pocket inside front", "Half clear pockets inside front and back", "Welded business card pocket", "Welded CD pocket", "Clear overlay on front, back and spine", "Pen loop"]}, "glovebox-wallets": {"desc": "Standard PVC. Clear pocket inside front and back, and 4 business card pockets inside.", "sizes": ["250 × 350 mm open (standard)", "270 × 370 mm open", "270 × 405 mm open", "Custom size"], "extras": []}, "travel-wallets": {"desc": "Standard PVC. Clear pocket inside front and back.", "sizes": ["250 × 250 mm open", "240 × 240 mm open", "Custom size"], "extras": []}, "tab-wallets": {"desc": "Standard PVC. Clear pocket inside front and back.", "sizes": ["160 × 190 mm open", "Custom size"], "extras": []}, "id-tags": {"desc": "Conference ID tags in 0.2 mm clear PVC with a clear pocket on one side and 3 lanyard holes. Card wallets have a clear pocket inside front and back.", "sizes": ["Small ID tag 115 × 106 mm", "Large ID tag 115 × 170 mm", "Card wallet 100 × 130 mm open", "Custom size"], "extras": []}, "music-folders": {"desc": "Clear diagonal pocket inside front and back, and a business card pocket on the outside front, top right.", "sizes": ["555 × 355 mm open (standard)", "A4", "Custom size"], "extras": []}, "notebook-covers": {"desc": "Standard PVC.", "sizes": ["Top opening 257 × 85 mm open", "Side opening 125 × 200 mm open", "Side opening 140 × 190 mm open", "Custom size"], "extras": ["Hard cover (with board)", "Clear overlay front and back", "Clear pages", "Spine weld", "Double thickness PVC", "Notebooks supplied", "Notebooks supplied and inserted"]}, "tally-books": {"desc": "Hard cover with 1200 micron board and a clear pocket inside front and back. Notebook not included.", "sizes": ["Large 198 × 208 mm open", "Small 150 × 200 mm open"], "extras": ["Foam padding", "Swing pockets", "Exercise book cut down and inserted", "Wiro ruled notebook supplied and inserted"]}, "clipboard-folders": {"desc": "Clipboard clip riveted on the front at the top. Standard PVC with 2400 micron board, or 1.4 mm polypropylene with rounded corners.", "sizes": ["A4 320 × 224 mm", "A5 170 × 230 mm", "Custom size"], "extras": ["Folder that closes over the clipboard"]}, "certificate-pockets": {"desc": "Opaque PVC back with a clear PVC front.", "sizes": ["A4", "Custom size"], "extras": ["Cord supplied and assembled", "Gold cord"]}, "pvc-satchels": {"desc": "Standard PVC with a business card pocket.", "sizes": ["V-flap 305 × 390 mm plus flap", "Tear drop 250 × 383 mm plus flap", "Zip 285 × 405 mm plus flap", "Job bag 430 × 325 mm with 100 mm flap", "Custom size"], "extras": ["Velcro dot (22 mm)", "Job bag: A4 pocket one side", "Job bag: A4 pockets both sides"]}, "polypropylene-satchels": {"desc": "Slot closure, supplied flat. 0.38 mm polypropylene as standard.", "sizes": ["A4 box satchel 10 mm", "A4 box satchel 20 mm", "A4 box satchel 30 mm", "A4 box satchel 40 mm", "A4 envelope", "Custom size"], "extras": ["0.6 mm polypropylene", "0.8 mm polypropylene"]}, "luggage-tags": {"desc": "Standard PVC luggage tag.", "sizes": [], "extras": ["Name card supplied", "Name card supplied and inserted"]}, "noren-tags": {"desc": "Clear pocket with an 18 mm self-adhesive strip.", "sizes": ["Standard 75 × 100 mm", "Large 130 × 140 mm", "Small 70 × 70 mm"], "extras": []}, "presentation-folders": {"desc": "Diary and compendium covers in 0.6 or 0.8 mm polypropylene, clear frosted or coloured.", "sizes": ["242 × 170 mm", "148 × 212 mm", "255 × 210 mm", "296 × 210 mm", "296 × 225 mm", "Custom size"], "extras": ["0.8 mm polypropylene", "Clear pockets"]}, "promotional-products": {"desc": "Polypropylene business cards 55 × 90 mm, 0.6 mm white with rounded corners. Mouse mats 208 × 234 mm with a non-slip backing and clear pocket.", "sizes": ["Business card 55 × 90 mm", "Mouse mat 208 × 234 mm", "Custom size"], "extras": ["0.8 mm business cards"]}}, HINTS={"Binders and folders": "Ring type and size (e.g. 2 D-ring, 25 mm), spine width, pockets, pen loop, business card slot, printing inside or outside", "Covers and books": "The book or pad it must fit (size or brand), top or side opening, pockets, whether you need refill books", "Wallets and satchels": "Closure (press stud, zip, Velcro or flap), pockets and card slots, gusset or flat, what goes inside", "Tags and cards": "Hole or slot, numbering or variable text, how it attaches (tie, cable tie, lanyard), indoor or outdoor", "Hospitality and healthcare": "Number of rooms or sites, inserts or pages, how and where it is used", "Schools and education": "School logo and colours, year levels, pockets, name card or certificate size", "Other products": "What it is for, where it will be used, and a photo or sample of anything similar"}, GENERIC="Pockets, fittings, ring size, what it holds, where it will be used, delivery address, deadlines";
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

  // ---- /contact: item blocks ----
  var ORDEROPT={"a3-chart-holder": "SS-PCU-033 A3 chart holder, horizontal", "a4-chart-holder": "SS-PCU-034 A4 chart holder, vertical", "a4-wall-holder": "SS-PCU-038 A4 wall-mounted holder, horizontal", "a4-clipboard": "SS-CCB-010 A4 patient clipboard, vertical", "a3-clipboard": "SS-CCB-015 A3 patient clipboard, horizontal", "folder-unprinted": "SS-PCU-13 (30 mm spine)", "folder-ward-bed": "SS-PCU-03 (30 mm spine)", "folder-custom": "Custom printed chart folder", "folder-hanging": "SS-PCU-13 H (30 mm spine)", "folder-hanging-printed": "SS-PCU-03 H (30 mm spine)", "dividers-blank": "SS-PCU-043 5-tab divider, blank", "dividers-printed": "SS-PCU-045 5-tab divider, printed", "dividers-custom": "Custom tab dividers (1 to 10 tabs)"};
  var FOLDER=['Oxford Blue 01','Red 02','Yellow 03','Purple 04','Navy 06','Grey 07','Orange 09','Pink 10','Apple Green 11','Sky Blue 13','Black (on request)'];
  function sovColours(t){t=(t||'').toLowerCase(); if(!t)return null;
    if(t.indexOf('holder')>=0)return ['Black gloss','White gloss']; if(t.indexOf('clipboard')>=0)return ['White'];
    if(t.indexOf('divider')>=0)return ['Not applicable']; return FOLDER;}
  function fillColours(col,allowed){var keep=col.value; col.innerHTML='';var o0=document.createElement('option');o0.value='';o0.text='Colour';col.add(o0);
    (allowed||FOLDER.concat(['Black gloss','White gloss','White','Not applicable'])).forEach(function(t){var o=document.createElement('option');o.text=t;col.add(o);});
    if(allowed&&allowed.length===1)col.selectedIndex=1; else if(allowed&&allowed.indexOf(keep)>=0)col.value=keep;}
  window.BPC_sovColours=sovColours; window.BPC_fillColours=fillColours;
  var form=document.querySelector('form[name=quote-request]');
  if(form){
    var items=[].slice.call(form.querySelectorAll('.item')), addBtn=document.getElementById('add-item');
    function opt(sel){return sel.options[sel.selectedIndex];}
    function val(div,sel){var e=div.querySelector(sel);return e?e.value.trim():'';}
    function syncHidden(div){
      div.querySelector('.item-extras-value').value=[].map.call(div.querySelectorAll('.item-extras input:checked'),function(c){return c.value;}).join(', ');
      div.querySelector('.item-pos-value').value=[].map.call(div.querySelectorAll('.item-pos input:checked'),function(c){return c.value;}).join(', ');
    }
    function routes(){
      var groups=items.filter(function(d){return !d.hidden;}).map(function(d){var o=opt(d.querySelector('.item-product'));return o?o.getAttribute('data-group'):'';});
      document.getElementById('route-print').hidden=groups.indexOf('print')<0;
      document.getElementById('route-sov').hidden=true;
    }
    function onSov(div){var s=div.querySelector('.sov-item');fillColours(div.querySelector('.sov-colour'),sovColours(s.value?opt(s).text:''));}
    function onProduct(div){
      var o=opt(div.querySelector('.item-product')), slug=o?o.getAttribute('data-slug'):'', g=o?o.getAttribute('data-group'):'';
      var std=STANDARD[slug], p=div.querySelector('.item-std'), wrap=div.querySelector('.item-extras-wrap'), box=div.querySelector('.item-extras');
      var sov=g==='sov';
      div.querySelector('.sov-fields').hidden=!sov; div.querySelector('.pu-fields').hidden=sov;
      if(sov){p.textContent='Choose the item code, colour and ward print below.';p.hidden=false;}
      else if(std){p.textContent='Comes with: '+std.desc; p.hidden=false;} else {p.textContent=''; p.hidden=true;}
      var dl=div.querySelector('datalist'); dl.innerHTML=''; ((std&&std.sizes)||[]).forEach(function(x){var op=document.createElement('option');op.value=x;dl.appendChild(op);});
      var keep=[].map.call(box.querySelectorAll('input:checked'),function(c){return c.value;});
      box.innerHTML='';
      if(!sov&&std&&std.extras.length){
        std.extras.forEach(function(x){var l=document.createElement('label');var c=document.createElement('input');c.type='checkbox';c.value=x;c.checked=keep.indexOf(x)>=0;l.appendChild(c);l.appendChild(document.createTextNode(' '+x));box.appendChild(l);});
        wrap.hidden=false;
      } else wrap.hidden=true;
      div.querySelector('.item-notes').placeholder=sov?'Bed numbers, ward name wording, delivery to ward':(HINTS[g]||GENERIC);
      if(sov)onSov(div);
      syncHidden(div); routes();
    }
    function show(div){div.hidden=false; addBtn.hidden=items.every(function(d){return !d.hidden;});}
    function selectSlug(div,slug){var s=div.querySelector('.item-product');for(var i=0;i<s.options.length;i++){if(s.options[i].getAttribute('data-slug')===slug){s.selectedIndex=i;break;}}onProduct(div);}
    function selectGroup(div,g){var s=div.querySelector('.item-product');for(var i=0;i<s.options.length;i++){if(s.options[i].getAttribute('data-group')===g){s.selectedIndex=i;break;}}onProduct(div);}
    function pickText(sel,text){for(var j=0;j<sel.options.length;j++){if(sel.options[j].text===text){sel.selectedIndex=j;return true;}}return false;}
    items.forEach(function(div){
      div.querySelector('.item-product').addEventListener('change',function(){onProduct(div);});
      div.querySelector('.sov-item').addEventListener('change',function(){onSov(div);});
      div.addEventListener('change',function(e){if(e.target.type==='checkbox')syncHidden(div);});
      var r=div.querySelector('.item-remove');
      if(r)r.addEventListener('click',function(){
        var k=div.getAttribute('data-key'); if(k){drop(k);div.removeAttribute('data-key');renderButtons();}
        [].forEach.call(div.querySelectorAll('input,select,textarea'),function(f){if(f.type==='checkbox')f.checked=false;else if(f.tagName==='SELECT')f.selectedIndex=0;else f.value='';});
        onProduct(div); div.hidden=true; addBtn.hidden=false; routes();
      });
    });
    addBtn.addEventListener('click',function(){var d=items.filter(function(x){return x.hidden;})[0]; if(d){show(d); d.querySelector('.item-product').focus();}});
    // Fill from ?product= and from the chosen items
    var q=new URLSearchParams(location.search).get('product'), queue=list.slice();
    if(q&&!queue.some(function(x){return x.key==='pu:'+q;}))queue.unshift({key:'pu:'+q,name:'',fromLink:true});
    queue.slice(0,items.length).forEach(function(x,i){
      var div=items[i]; show(div);
      if(!x.fromLink)div.setAttribute('data-key',x.key);
      if(x.key.indexOf('pu:')===0)selectSlug(div,x.key.slice(3));
      else {selectGroup(div,'sov'); var id=x.key.slice(4), s=div.querySelector('.sov-item');
        if(!(ORDEROPT[id]&&pickText(s,ORDEROPT[id])))div.querySelector('.item-notes').value=x.name; onSov(div);}
    });
    items.forEach(function(d){if(!d.hidden)onProduct(d);});

    // On send: write a plain summary at the top of the email and leave out empty items
    form.addEventListener('submit',function(){
      var rep=(form.querySelector('input[name=enquiry_type]:checked')||{}).value==='repeat', out=[];
      function add(k,v){if(v)out.push('  '+k+': '+v);}
      if(rep){
        out.push('REPEAT ORDER');
        add('Previous job, invoice or PO',val(form,'#repeat_ref')); add('Product',val(form,'#repeat_product'));
        add('Quantity',val(form,'#repeat_qty')); add('Changes',val(form,'#repeat_same')); add('What has changed',val(form,'#repeat_changes'));
      } else {
        var n=0;
        items.forEach(function(div){
          if(div.hidden)return; var ps=div.querySelector('.item-product'); if(!ps.value)return; n++;
          var o=opt(ps), slug=o.getAttribute('data-slug'), sov=o.getAttribute('data-group')==='sov', std=STANDARD[slug];
          var N='[name=item_'+div.getAttribute('data-n')+'_';
          out.push('ITEM '+n+': '+(sov?'Sov Services: '+(val(div,'.sov-item')||'item not chosen'):o.text));
          if(sov){add('Colour',val(div,'.sov-colour')); add('Ward and bed print',val(div,N+'sov_print]'));}
          else {
            if(std)add('Comes with',std.desc);
            add('Size',val(div,N+'size]')); add('Material',val(div,N+'material]')); add('Colour',val(div,N+'colour]'));
            var pr=val(div,N+'print]'), pos=val(div,'.item-pos-value'), ink=val(div,N+'ink_colour]');
            if(pr)add('Printing',pr+(pos?', '+pos:'')+(ink?', ink '+ink:''));
            add('Extras',val(div,'.item-extras-value'));
          }
          add('Quantity',val(div,N+'quantity]')); add('Notes',val(div,'.item-notes'));
          out.push('');
        });
      }
      add('Needed by',val(form,'#needed_by')); add('Deliver to',val(form,'#postcode')); add('PO number',val(form,'#reference'));
      form.querySelector('[name=quote_summary]').value=out.join('\n');
      // Leave unused parts out of the email
      items.forEach(function(div){var used=!rep&&!div.hidden&&div.querySelector('.item-product').value;
        var sov=used&&opt(div.querySelector('.item-product')).getAttribute('data-group')==='sov';
        [].forEach.call(div.querySelectorAll('input,select,textarea'),function(f){f.disabled=!used;});
        if(used){[].forEach.call(div.querySelectorAll(sov?'.pu-fields input,.pu-fields select':'.sov-fields input,.sov-fields select'),function(f){f.disabled=true;});}
      });
      [].forEach.call(form.querySelectorAll('.repeat-fs input,.repeat-fs select,.repeat-fs textarea'),function(f){f.disabled=!rep;});
      [].forEach.call(form.querySelectorAll('input[type=hidden]'),function(f){if(!f.value&&f.name!=='form-name')f.disabled=true;});
    });
    window.addEventListener('pageshow',function(){[].forEach.call(form.querySelectorAll('[disabled]'),function(f){f.disabled=false;});});
  }

  // ---- /hospital/order: fill order lines from chosen Sov products ----
  var ord=document.querySelector('form[name=hospital-order]');
  if(ord){
    var lines=[].slice.call(ord.querySelectorAll('tr.order-line')), addLine=document.getElementById('add-line');
    var MAP={}; try{MAP=JSON.parse(document.getElementById('order-map').textContent);}catch(e){}
    function refreshAdd(){if(addLine)addLine.hidden=lines.every(function(r){return !r.hidden;});}
    function freeLine(){for(var i=0;i<lines.length;i++){var s=lines[i].querySelector('select');if(!s.value){lines[i].hidden=false;refreshAdd();return s;}}return null;}
    function pick(sel,text){for(var j=0;j<sel.options.length;j++){if(sel.options[j].text===text||sel.options[j].text.indexOf(text)===0){sel.selectedIndex=j;return true;}}return false;}
    if(addLine)addLine.addEventListener('click',function(){var r=lines.filter(function(x){return x.hidden;})[0];if(r){r.hidden=false;r.querySelector('select').focus();}refreshAdd();});
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
    if(left.length){var n=ord.querySelector('textarea[name=notes]'); if(n&&!n.value)n.value='Also: '+left.join('; ');}
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
    if(t.indexOf('divider')>=0)return ['Not applicable'];
    return FOLDER;
  }
  [].forEach.call(ord.querySelectorAll('tr.order-line'),function(row){
    var item=row.querySelector('select[name^=item_]'), col=row.querySelector('select[name^=colour_]');
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
