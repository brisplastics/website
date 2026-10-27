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

    function ddmmyyyy(s){var m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s);return m?m[3]+'/'+m[2]+'/'+m[1]:s;}
    // On send: one plain summary of every item goes in the email
    form.addEventListener('submit',function(){
      var rep=(form.querySelector('input[name=enquiry_type]:checked')||{}).value==='repeat', out=[];
      function add(k,val){if(val)out.push('  '+k+': '+val);}
      function g(id){var e=form.querySelector('#'+id);return e?e.value.trim():'';}
      if(rep){
        out.push('REPEAT ORDER');
        add('Previous job, invoice or PO',g('repeat_ref')); add('Product',g('repeat_product'));
        add('Quantity',g('repeat_qty')); add('Changes',g('repeat_same')); add('What has changed',g('repeat_changes'));
      } else {
        var n=0;
        items.forEach(function(div){
          if(div.hidden)return; var ps=div.querySelector('.item-product'); if(!ps.value)return; n++;
          var o=opt(ps), std=STANDARD[o.getAttribute('data-slug')];
          out.push('ITEM '+n+': '+o.text);
          if(std)add('Comes with',std.desc);
          add('Size',v(div,'size')); add('Material',v(div,'material')); add('Colour',v(div,'colour'));
          var pr=v(div,'print'), pos=checked(div,'.item-pos'), ink=v(div,'ink');
          if(pr||pos||ink)add('Printing',[pr,pos?'on '+pos:'',ink?'ink '+ink:''].filter(Boolean).join(', '));
          add('Extras',checked(div,'.item-extras'));
          add('Quantity',v(div,'qty')); add('Notes',v(div,'notes'));
          out.push('');
        });
        if(!n)out.push('No product chosen');
      }
      form.querySelector('[name=quote_summary]').value=out.join('\n').trim();
    });
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
