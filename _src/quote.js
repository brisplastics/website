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
  var STANDARD=__STANDARD__, HINTS=__HINTS__, GENERIC=__GENERIC__;
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
          var desc=[opt(ps).text,v(div,'size'),v(div,'material'),v(div,'colour'),printing,ex].filter(function(x){return x&&!/^Choose/.test(x);}).join(', ');
          lines.push('',n+'. Qty '+(v(div,'qty')||'not given'));
          lines.push('   '+desc);
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
