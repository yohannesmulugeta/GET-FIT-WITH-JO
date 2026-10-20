/* Get Fit With JO premium motion — optional enhancement, no external dependencies */
(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const isStill = () => reduced.matches;
  const header = document.querySelector('.site-header');
  const portrait = document.querySelector('.hero-visual');
  let frame = false;
  const refreshScroll = () => {
    frame = false;
    const top = Math.max(0, window.scrollY);
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    if (header) {
      header.classList.toggle('is-scrolled', top > 25);
      header.style.setProperty('--scroll-progress', String(Math.min(1, top / max)));
    }
    if (portrait) portrait.style.setProperty('--photo-shift',
      !isStill() && innerWidth > 700 ? String(Math.min(800, top) * .025) + 'px' : '0px');
  };
  const onScroll = () => {
    if (frame) return;
    frame = true;
    requestAnimationFrame(refreshScroll);
  };
  addEventListener('scroll', onScroll, {passive:true});
  addEventListener('resize', onScroll, {passive:true});
  refreshScroll();

  if (!isStill()) {
    const selector = [
      '.section-heading','.about-visual','.about-content','.program-cards',
      '.specialized-services','.audience-grid','.jo-gallery-videos',
      '.jo-gallery-grid','.results-main','.results-aside','.social-layout',
      '.jo-faq-intro','.jo-faq-items','.jo-consultation-info',
      '.jo-consultation-form','.jo-payment-grid','.story-layout',
      '.about-credential-grid'
    ].join(',');
    const items = [...document.querySelectorAll(selector)];
    items.forEach((item, i) => {
      item.classList.add('motion-reveal');
      item.style.setProperty('--motion-delay', String(i % 3 * 50) + 'ms');
    });
    document.documentElement.classList.add('motion-ready');
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        });
      }, {threshold:.06,rootMargin:'0px 0px -25px 0px'});
      items.forEach(item => observer.observe(item));
    } else items.forEach(item => item.classList.add('is-visible'));
  }

  if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
    document.querySelectorAll('.program-card').forEach(card => {
      card.addEventListener('pointermove', event => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--hover-x', ((event.clientX-rect.left)/rect.width*100).toFixed(1)+'%');
        card.style.setProperty('--hover-y', ((event.clientY-rect.top)/rect.height*100).toFixed(1)+'%');
      }, {passive:true});
    });
  }

  const serviceField = document.querySelector('#enquiry-service');
  if (serviceField) {
    const choices = [...serviceField.options].map(option => option.value);
    document.querySelectorAll('.program-card,.special-service').forEach(card => {
      const title = card.querySelector('h3')?.textContent.trim();
      if (!choices.includes(title)) return;
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'service-quick-book';
      button.textContent = 'Choose for consultation ↗';
      button.setAttribute('aria-label', 'Choose '+ title +' for your consultation');
      button.addEventListener('click', () => {
        serviceField.value = title;
        serviceField.dispatchEvent(new Event('change', {bubbles:true}));
        document.querySelector('#consultation')?.scrollIntoView({
          behavior:isStill()?'auto':'smooth',block:'start'
        });
        serviceField.focus({preventScroll:true});
      });
      (card.querySelector('.program-body') || card).append(button);
    });
  }

  const enquiry = document.querySelector('#coach-enquiry-form');
  if (enquiry) {
    const progress = document.createElement('div');
    progress.className = 'jo-form-progress';
    progress.innerHTML = '<div class="jo-form-progress-copy"><span></span><small></small></div><div class="jo-form-progress-track" role="progressbar" aria-label="Required consultation details completed" aria-valuemin="0" aria-valuemax="4" aria-valuenow="0"><span class="jo-form-progress-fill"></span></div>';
    enquiry.querySelector('.enquiry-fields')?.before(progress);
    const checks = [
      () => (enquiry.querySelector('#enquiry-name')?.value.trim().length || 0)>=2,
      () => Boolean(enquiry.querySelector('#enquiry-service')?.value),
      () => (enquiry.querySelector('#enquiry-goal')?.value.trim().length || 0)>=10,
      () => Boolean(enquiry.querySelector('#enquiry-consent')?.checked)
    ];
    const update = () => {
      const done = checks.filter(fn => fn()).length;
      progress.querySelector('.jo-form-progress-copy span').textContent =
        done === 4 ? 'Required details ready — choose how to send' : 'Complete your consultation request';
      progress.querySelector('.jo-form-progress-copy small').textContent = String(done)+' / 4 essentials';
      progress.querySelector('[role="progressbar"]').setAttribute('aria-valuenow', String(done));
      progress.querySelector('.jo-form-progress-fill').style.width = String(done*25)+'%';
    };
    enquiry.addEventListener('input', update);
    enquiry.addEventListener('change', update);
    update();
  }

  const cards = [...document.querySelectorAll('.jo-gallery-card')];
  if (cards.length && typeof HTMLDialogElement !== 'undefined') {
    const dialog = document.createElement('dialog');
    dialog.className = 'jo-lightbox';
    dialog.setAttribute('aria-label','Training gallery');
    dialog.innerHTML = '<div class="jo-lightbox-head"><span aria-live="polite"></span><button type="button" class="jo-lightbox-close" aria-label="Close gallery">×</button></div><figure><img width="720" height="800" alt=""><figcaption class="jo-lightbox-foot"><div><strong></strong><p></p></div><div class="jo-lightbox-controls"><button type="button" class="jo-lightbox-prev" aria-label="Previous image">←</button><button type="button" class="jo-lightbox-next" aria-label="Next image">→</button></div></figcaption></figure>';
    document.body.append(dialog);
    const image = dialog.querySelector('figure img');
    const closer = dialog.querySelector('.jo-lightbox-close');
    let active = 0;
    const show = index => {
      active = (index+cards.length)%cards.length;
      const card = cards[active];
      const original = card.querySelector('.jo-gallery-image img');
      image.src = original.currentSrc || original.src;
      image.alt = original.alt;
      dialog.querySelector('figcaption strong').textContent = card.querySelector('figcaption strong')?.textContent || 'Training';
      dialog.querySelector('figcaption p').textContent = card.querySelector('figcaption span')?.textContent || '';
      dialog.querySelector('.jo-lightbox-head span').textContent = 'PHOTO '+String(active+1)+' / '+String(cards.length);
    };
    cards.forEach((card,index) => {
      const photo = card.querySelector('.jo-gallery-image');
      if (!photo) return;
      const button = document.createElement('button');
      button.type='button';
      button.className='gallery-view-button';
      button.setAttribute('aria-label','Enlarge photo '+String(index+1));
      const label=document.createElement('span');
      label.textContent='View photo ↗';
      button.append(label);
      button.addEventListener('click',()=>{show(index);dialog.showModal();closer.focus();});
      photo.append(button);
    });
    closer.addEventListener('click',()=>dialog.close());
    dialog.querySelector('.jo-lightbox-prev').addEventListener('click',()=>show(active-1));
    dialog.querySelector('.jo-lightbox-next').addEventListener('click',()=>show(active+1));
    dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
    dialog.addEventListener('keydown',event=>{
      if(event.key==='ArrowLeft'){event.preventDefault();show(active-1);}
      if(event.key==='ArrowRight'){event.preventDefault();show(active+1);}
    });
  }
})();
