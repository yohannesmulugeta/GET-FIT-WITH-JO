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
  window.addEventListener('resize',()=>{if(window.innerWidth>900)setMenu(false)});
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
  whatsappButton.addEventListener('click',event=>{
    if(!validateEnquiry(false)){
      event.preventDefault();
      return;
    }
    const message=[
      'Hello Joseph! I would like to enquire about Get Fit with JO coaching.',
      '',
      'Name: '+fields.name.value.trim(),
      'Phone: '+(fields.phone.value.trim()||'I will message you here'),
      'Email: '+(fields.email.value.trim()||'Not provided'),
      'Program: '+fields.service.value,
      'Coaching preference: '+fields.location.value,
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
