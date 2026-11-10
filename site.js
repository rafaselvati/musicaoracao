const reviews=window.SITE_CONFIG?.testimonials||[];
if(reviews.length){document.getElementById('testimonios').hidden=false;for(const review of reviews){const block=document.createElement('blockquote'),p=document.createElement('p'),cite=document.createElement('cite');p.textContent=review.text;cite.textContent=review.name;block.append(p,cite);document.getElementById('reviews').append(block)}}
const sticky=document.getElementById('sticky-buy'),offers=document.getElementById('ofertas');
function updateSticky(){const r=offers.getBoundingClientRect();sticky.classList.toggle('show',window.scrollY>500&&(r.bottom<0||r.top>innerHeight))}addEventListener('scroll',updateSticky,{passive:true});addEventListener('resize',updateSticky);updateSticky();
// Conservar atribución de campaña durante el paso al checkout.
const qs=new URLSearchParams(location.search);document.querySelectorAll('[data-plan]').forEach(a=>{const u=new URL(a.href);for(const [k,v] of qs)if(/^utm_/.test(k)||['fbclid','gclid'].includes(k))u.searchParams.set(k,v);a.href=u.href});
