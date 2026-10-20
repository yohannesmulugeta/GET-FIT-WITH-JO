const menuButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('#site-nav');
const header=document.querySelector('.site-header');
function setMenu(open){
  if(!menuButton||!navigation)return;
  menuButton.setAttribute('aria-expanded',String(open));
  menuButton.setAttribute('aria-label',open?'Close navigation menu':'Open navigation menu');
  navigation.classList.toggle('is-open',open);
  document.body.classList.toggle('menu-open',open);
}
if(menuButton&&navigation){
  menuButton.addEventListener('click',()=>setMenu(menuButton.getAttribute('aria-expanded')!=='true'));
  navigation.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>setMenu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')setMenu(false)});
  document.addEventListener('click',e=>{if(!header.contains(e.target))setMenu(false)});
  window.addEventListener('resize',()=>{if(window.innerWidth>1050)setMenu(false)});
}
if(navigation&&document.querySelector('#programs')){
  const links=[...navigation.querySelectorAll('a[href^="#"]')];
  const sections=[...document.querySelectorAll('main section[id]')];
  const group={audiences:'programs',training:'gallery',enquiry:'consultation'};
  function updateCurrentSection(){
    const threshold=(header?.offsetHeight||0)+100;
    const visible=sections.filter(section=>section.getBoundingClientRect().top<=threshold).pop();
    const current=group[visible?.id]||visible?.id;
    links.forEach(link=>{
      if(link.hash==='#'+current)link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }
  window.addEventListener('scroll',updateCurrentSection,{passive:true});
  window.addEventListener('resize',updateCurrentSection);
  updateCurrentSection();
}
const copyright=document.querySelector('#copyright-year');
if(copyright)copyright.textContent=String(new Date().getFullYear());
// Avoid multiple competing audio sources when browsing the training clips.
const videos=[...document.querySelectorAll('.video-stage video')];
videos.forEach(v=>v.addEventListener('play',()=>videos.forEach(other=>{if(other!==v)other.pause()})));

// Media posters load only as each clip approaches the viewport, saving early mobile requests.
const deferredPosters = document.querySelectorAll('video[data-poster]');
function displayPoster(video) {
  if (video.dataset.poster) { video.poster = video.dataset.poster; delete video.dataset.poster; }
}
if ('IntersectionObserver' in window) {
  const posterObserver = new IntersectionObserver(entries => {
    entries.forEach(({target,isIntersecting}) => {
      if (isIntersecting) { displayPoster(target); posterObserver.unobserve(target); }
    });
  }, {rootMargin:'350px 0px'});
  deferredPosters.forEach(video => {
    posterObserver.observe(video);
    video.addEventListener('pointerdown', () => displayPoster(video), {once:true});
    video.addEventListener('focus', () => displayPoster(video), {once:true});
  });
} else deferredPosters.forEach(displayPoster);


// Shared form for email and WhatsApp. Contact data is never stored locally.
const coachingForm=document.querySelector('#coach-enquiry-form');
if(coachingForm){
  const status=coachingForm.querySelector('#enquiry-status');
  const emailButton=coachingForm.querySelector('#enquiry-email-button');
  const whatsappButton=coachingForm.querySelector('#enquiry-whatsapp-button');
  const fields={
    name:coachingForm.querySelector('#enquiry-name'),
    phone:coachingForm.querySelector('#enquiry-phone'),
    email:coachingForm.querySelector('#enquiry-email'),
    service:coachingForm.querySelector('#enquiry-service'),
    location:coachingForm.querySelector('#enquiry-location'),
    goal:coachingForm.querySelector('#enquiry-goal'),
    preferredDate:coachingForm.querySelector('#enquiry-date'),
    preferredTime:coachingForm.querySelector('#enquiry-time'),
  };
  function setEnquiryStatus(message,state='info'){
    status.textContent=message;
    status.dataset.state=state;
  }
  function validateEnquiry(needsReplyContact){
    if(!coachingForm.reportValidity())return false;
    if(needsReplyContact&&!fields.email.value.trim()&&!fields.phone.value.trim()){
      setEnquiryStatus('Please provide an email address or phone number so Joseph can reply.','error');
      fields.email.focus();
      return false;
    }
    return true;
  }
  // The requested time is a preference; availability is confirmed by Joseph.
  if(fields.preferredDate){const d=new Date();fields.preferredDate.min=[d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');}
  whatsappButton.addEventListener('click',event=>{
    if(!validateEnquiry(false)){
      event.preventDefault();
      return;
    }
    const message=[
      'Hello Joseph! I would like to request a personal consultation.',
      '',
      'Name: '+fields.name.value.trim(),
      'Phone: '+(fields.phone.value.trim()||'I will message you here'),
      'Email: '+(fields.email.value.trim()||'Not provided'),
      'Program: '+fields.service.value,
      'Coaching preference: '+fields.location.value,
      'Preferred date: '+(fields.preferredDate.value||'Flexible'),
      'Preferred time: '+(fields.preferredTime.value||'Flexible'),
      'My goals: '+fields.goal.value.trim(),
    ].join('\n');
    whatsappButton.href='https://wa.me/251986890425?text='+encodeURIComponent(message);
    setEnquiryStatus('WhatsApp will open with your prepared message. Please press Send inside WhatsApp to finish.','info');
  });
  // Standard form POST is more reliable than cross-origin AJAX for first-use
  // activation and supports the provider's anti-spam CAPTCHA flow.
  coachingForm.addEventListener('submit', event=>{
    if(!validateEnquiry(true)){
      event.preventDefault();
      return;
    }
    if(coachingForm.querySelector('[name="_honey"]').value){
      event.preventDefault();
      return;
    }
    setEnquiryStatus('Complete the secure email submission page that opens. You may need to finish CAPTCHA. Joseph must confirm the receiving email address before delivery is active.','info');
  });
}


// Copy-on-click for bank sample cards and Joseph's displayed phone number.
// All bank numbers are explicitly non-payable demonstration values.
const paymentCopyStatus=document.querySelector('#payment-copy-status');
document.querySelectorAll('.jo-payment-card').forEach(card=>{
  card.addEventListener('click',async()=>{
    const number=card.dataset.copyNumber;
    if(!number)return;
    let copied=false;
    try{
      if(navigator.clipboard&&window.isSecureContext){
        await navigator.clipboard.writeText(number);
        copied=true;
      }else{
        const input=document.createElement('textarea');
        input.value=number;
        input.style.position='fixed';
        input.style.left='-9999px';
        document.body.appendChild(input);
        input.focus();
        input.select();
        copied=document.execCommand('copy');
        input.remove();
      }
    }catch(error){copied=false;}
    card.classList.add('is-revealed');
    const label=card.dataset.paymentLabel||'Payment';
    const demo=card.classList.contains('is-demo');
    if(paymentCopyStatus)paymentCopyStatus.textContent=copied
      ?(label+(demo?' sample number copied. Not valid for payments.':' number copied. Verify the recipient before paying.'))
      :'Could not copy. Please select the displayed number manually.';
  });
});
