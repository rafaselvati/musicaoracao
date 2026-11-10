/* GA4: no access tokens, Stripe session IDs, email or payment details are sent. */
(()=>{
 const measurementId='G-8D1Y6BW9VN';
 const products={esencial:{item_id:'septimo_esencial',item_name:'Edición Esencial',price:9.90},completa:{item_id:'septimo_completa',item_name:'Experiencia Completa',price:19.90},audios:{item_id:'septimo_audios',item_name:'Frecuencias de Contemplación',price:29.90}};
 let active=false;const seen=new Set();
 const disabled=()=>window.SITE_PREVIEW||['localhost','127.0.0.1',''].includes(location.hostname)||location.hostname.endsWith('.chatgpt.site');
 function safeURL(raw,campaign=false){try{const u=new URL(raw,location.origin),clean=new URL(u.origin+u.pathname);if(campaign)for(const key of ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','plan']){const v=u.searchParams.get(key);if(v)clean.searchParams.set(key,v.slice(0,100))}return clean.href}catch{return ''}}
 function event(name,details={}){if(!active)return;try{window.gtag('event',name,{...details,page_location:safeURL(location.href,true),page_referrer:safeURL(document.referrer||location.origin),transport_type:'beacon'})}catch{}}
 function offer(name,plan,once=false){if(!Object.hasOwn(products,plan))return;const key=name+':'+plan;if(once&&seen.has(key))return;seen.add(key);const item=products[plan];event(name,{currency:'USD',value:item.price,offer_plan:plan,items:[{...item,quantity:1}]})}
 function init(){if(active||disabled())return;active=true;window.dataLayer=window.dataLayer||[];window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
 window.gtag('js',new Date());window.gtag('config',measurementId,{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:safeURL(location.href,true),page_referrer:safeURL(document.referrer||location.origin)});
 const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id='+measurementId;document.head.append(script);
 event('page_view',{page_title:document.title});
 if(location.pathname.endsWith('/checkout.html'))offer('checkout_view',new URLSearchParams(location.search).get('plan')||'esencial',true);
 document.addEventListener('click',e=>{const link=e.target.closest?.('a[href]');if(!link)return;try{const u=new URL(link.href,location.origin);if(u.origin===location.origin&&u.pathname.endsWith('/checkout.html'))offer('select_item',u.searchParams.get('plan')||'esencial')}catch{}});
 }
 function purchase(data){if(!active||!data||data.live!==true||!/^order_[a-f0-9]{32}$/.test(data.transaction_id)||!Object.hasOwn(products,data.plan)||data.currency!=='USD'||data.value!==products[data.plan].price)return;
 const key='septimo_ga_purchase_'+data.transaction_id;if(seen.has(key))return;try{if(localStorage.getItem(key))return}catch{}seen.add(key);
 event('purchase',{transaction_id:data.transaction_id,currency:'USD',value:data.value,offer_plan:data.plan,items:[{...products[data.plan],quantity:1}]});try{localStorage.setItem(key,'1')}catch{}
 }
 window.SiteAnalytics={init,offer,purchase};
 // Delivery removes private query credentials before loading any third-party analytics.
 if(!location.pathname.endsWith('/entrega.html'))init();
})();
