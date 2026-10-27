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

  // ---- /contact: item blocks ----
  var ORDEROPT=__ORDEROPT__;
  var FOLDER=['Oxford Blue 01','Red 02','Yellow 03','Purple 04','Navy 06','Grey 07','Orange 09','Pink 10','Apple Green 11','Sky Blue 13','Black (on request)'];
  function sovColours(t){t=(t||'').toLowerCase(); if(!t)return null;
    if(t.indexOf('holder')>=0)return ['Black gloss','White gloss']; if(t.indexOf('clipboard')>=0)return ['White'];
    if(t.indexOf('custom tab divider')>=0)return ['Standard colours (white, red, orange, green, yellow)','Another colour from the range (add it to the notes)']; if(t.indexOf('divider')>=0)return ['Not applicable']; return FOLDER;}
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
    if(t.indexOf('custom tab divider')>=0)return ['Standard colours (white, red, orange, green, yellow)','Another colour from the range (add it to the notes)'];
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
