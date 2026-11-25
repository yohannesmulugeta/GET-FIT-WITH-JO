// Read-only production smoke test for Get Fit with JO; never sends forms or payments.
// Usage: SITE_URL=https://jofitcoach.com/ CHROME_PATH=/usr/bin/google-chrome-stable node tests/browser-smoke.mjs
import assert from 'node:assert/strict';
import { chromium } from 'playwright-core';

const url = process.env.SITE_URL || 'https://jofitcoach.com/';
const executablePath = process.env.CHROME_PATH || '/usr/bin/google-chrome-stable';
const browser = await chromium.launch({ executablePath, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
let passed = 0;
const check = (description, condition) => {
  assert.ok(condition, description);
  console.log('PASS', description);
  passed += 1;
};

try {
  const page = await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});
  // Stop accidental external form requests: the test must never send an email or WhatsApp message.
  await page.route(/formsubmit\.co|wa\.me/, route => route.abort());
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const response = await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
  check('Production homepage responds successfully', response?.ok());
  await page.waitForSelector('#consultation');
  check('Services navigation and consultation are present',
    await page.getByRole('navigation',{name:'Primary navigation'}).getByText('Services',{exact:true}).count()===1 &&
    await page.locator('#consultation').count()===1);
  check('Eleven training videos are present', await page.locator('#training video').count()===11);
  check('No payment account details are published', await page.locator('#payments,.jo-payment-card').count()===0);
  check('Contact number is callable', await page.locator('a[href="tel:+251986890425"]').count()>0);

  const faq = page.locator('.jo-faq-items details').first();
  await faq.locator('summary').click();
  check('FAQ disclosure works',await faq.evaluate(element=>element.open));
  await faq.locator('summary').click();

  const quickBook = page.locator('.service-quick-book').first();
  check('Quick-book button is provided on services',await quickBook.count()>0);
  await quickBook.click();
  check('Services preselect the consultation form', (await page.locator('#enquiry-service').inputValue()).length>0);

  const date = page.locator('#enquiry-date');
  const todayAddis = await page.evaluate(() => {
    const parts = new Intl.DateTimeFormat('en-GB',{timeZone:'Africa/Addis_Ababa',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    const val = type => parts.find(part => part.type===type)?.value;
    return [val('year'),val('month'),val('day')].join('-');
  });
  check('Consultation dates use Addis Ababa local calendar day',await date.getAttribute('min')===todayAddis);
  await date.fill('2020-01-01');
  check('Outdated appointment dates are rejected',await date.evaluate(element=>!element.validity.valid));
  await date.fill('');
  check('Email and WhatsApp request actions are present',await page.locator('#enquiry-email-button').count()===1 &&
    await page.locator('#enquiry-whatsapp-button').count()===1);

  const enlarge = page.locator('.gallery-view-button').first();
  check('Gallery photo lightbox can be opened',await enlarge.count()>0);
  await enlarge.click();
  check('Gallery lightbox is accessible',await page.locator('dialog.jo-lightbox').evaluate(element=>element.open));
  await page.keyboard.press('Escape');
  check('Gallery lightbox closes with Escape',await page.locator('dialog.jo-lightbox').evaluate(element=>!element.open));

  const expand = page.locator('.video-gallery-toggle');
  check('Extra videos can be expanded',await expand.count()===1);
  await expand.click();
  check('Video gallery expansion updates accessibility state',await expand.getAttribute('aria-expanded')==='true');
  check('No uncaught JavaScript errors on desktop',errors.length===0);

  const mobile = await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
  mobile.on('pageerror',error=>errors.push(error.message));
  await mobile.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
  check('Mobile call and WhatsApp actions exist',await mobile.locator('.jo-mobile-actions a').count()===2);
  const toggle=mobile.locator('.menu-toggle');
  console.log('MOBILE_MENU_DIAGNOSTIC',JSON.stringify(await mobile.evaluate(()=>{
    const button=document.querySelector('.menu-toggle');
    const box=button?.getBoundingClientRect();
    const x=box?box.x+box.width/2:0;
    const y=box?box.y+box.height/2:0;
    const hit=document.elementFromPoint(x,y);
    const shell=document.querySelector('.nav-shell');
    return {x,y,button:box?.toJSON(),hit:hit?.outerHTML?.slice(0,230),
      shell:shell?.getBoundingClientRect()?.toJSON(),
      buttonStyles:button?{position:getComputedStyle(button).position,zIndex:getComputedStyle(button).zIndex,display:getComputedStyle(button).display}:null,
      width:innerWidth,scrollWidth:document.documentElement.scrollWidth};
  })));
  await toggle.click({timeout:6000});
  check('Mobile menu expands',await toggle.getAttribute('aria-expanded')==='true');
  await mobile.locator('#site-nav a[href="#programs"]').click();
  check('Mobile menu closes after navigation',await toggle.getAttribute('aria-expanded')==='false');
  check('No horizontal mobile overflow',await mobile.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2));
  check('No uncaught JavaScript errors on mobile',errors.length===0);
  console.log('BROWSER_QA_PASS',passed,'checks against',url);
} finally {
  await browser.close();
}
