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
  var TAWK_PROPERTY_ID='', TAWK_WIDGET_ID='default';
  if(!TAWK_PROPERTY_ID)return;
  window.Tawk_API=window.Tawk_API||{};window.Tawk_LoadStart=new Date();
  var s=document.createElement('script');
  s.async=true;s.src='https://embed.tawk.to/'+TAWK_PROPERTY_ID+'/'+TAWK_WIDGET_ID;
  s.charset='UTF-8';s.setAttribute('crossorigin','*');
  document.body.appendChild(s);
})();
