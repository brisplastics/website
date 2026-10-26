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
    var sov=list.filter(function(x){return x.key.indexOf('sov:')===0;}), left=[];
    sov.forEach(function(x,i){
      var sel=ord.querySelector('select[name=item_'+(i+1)+']'); if(!sel){left.push(x.name);return;}
      var code=x.name.split(' ')[0], hit=false;
      for(var j=0;j<sel.options.length;j++){if(sel.options[j].text.indexOf(code)===0){sel.selectedIndex=j;hit=true;break;}}
      if(!hit)left.push(x.name);
    });
    if(left.length){var n=ord.querySelector('textarea[name=notes]'); if(n&&!n.value)n.value='Also: '+left.join('; ');}
  }
})();
