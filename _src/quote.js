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
  var form=document.querySelector('form[name=quote-request]');
  if(form){
    var items=[].slice.call(form.querySelectorAll('.item')), addBtn=document.getElementById('add-item');
    function opt(sel){return sel.options[sel.selectedIndex];}
    function syncHidden(div){
      div.querySelector('.item-extras-value').value=[].map.call(div.querySelectorAll('.item-extras input:checked'),function(c){return c.value;}).join(', ');
      div.querySelector('.item-pos-value').value=[].map.call(div.querySelectorAll('.item-pos input:checked'),function(c){return c.value;}).join(', ');
    }
    function routes(){
      var groups=items.filter(function(d){return !d.hidden;}).map(function(d){var o=opt(d.querySelector('.item-product'));return o?o.getAttribute('data-group'):'';});
      document.getElementById('route-sov').hidden=groups.indexOf('sov')<0;
      document.getElementById('route-print').hidden=groups.indexOf('print')<0;
    }
    function onProduct(div){
      var o=opt(div.querySelector('.item-product')), slug=o?o.getAttribute('data-slug'):'', g=o?o.getAttribute('data-group'):'';
      var std=STANDARD[slug], p=div.querySelector('.item-std'), wrap=div.querySelector('.item-extras-wrap'), box=div.querySelector('.item-extras');
      if(std){p.textContent='Comes with: '+std[0]; p.hidden=false;} else {p.textContent=''; p.hidden=true;}
      box.innerHTML='';
      if(std&&std[1].length){
        std[1].forEach(function(x){var l=document.createElement('label');var c=document.createElement('input');c.type='checkbox';c.value=x;l.appendChild(c);l.appendChild(document.createTextNode(' '+x));box.appendChild(l);});
        wrap.hidden=false;
      } else wrap.hidden=true;
      div.querySelector('.item-notes').placeholder=HINTS[g]||GENERIC;
      syncHidden(div); routes();
    }
    function show(div){div.hidden=false; addBtn.hidden=items.every(function(d){return !d.hidden;});}
    function nextFree(){for(var i=0;i<items.length;i++){if(items[i].hidden||!items[i].querySelector('.item-product').value){if(i===0||items[i].hidden||!items[i].querySelector('.item-product').value)return items[i];}}return null;}
    function selectSlug(div,slug){var s=div.querySelector('.item-product');for(var i=0;i<s.options.length;i++){if(s.options[i].getAttribute('data-slug')===slug){s.selectedIndex=i;break;}}onProduct(div);}
    function selectGroup(div,g){var s=div.querySelector('.item-product');for(var i=0;i<s.options.length;i++){if(s.options[i].getAttribute('data-group')===g){s.selectedIndex=i;break;}}onProduct(div);}
    items.forEach(function(div){
      div.querySelector('.item-product').addEventListener('change',function(){onProduct(div);});
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
      else {selectGroup(div,'sov'); div.querySelector('.item-notes').value=x.name;}
    });
    items.forEach(function(d){if(!d.hidden)onProduct(d);});
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
