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
