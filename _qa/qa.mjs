// Usage: node _qa/qa.mjs <baseUrl> <outDir>
import { chromium } from "/Users/russlanyes/Dev/Dental-Clinic/node_modules/playwright/index.mjs";
const base = process.argv[2].replace(/\/?$/, "/");
const out = process.argv[3];
const pages = [["home-en", ""], ["home-es", "es/"], ["lawn-en", "lawn/"], ["pest-en", "pest/"], ["lawn-es", "es/jardineria/"], ["pest-es", "es/plagas/"]];
const pairs = { "": "es/", "es/": "", "lawn/": "es/jardineria/", "es/jardineria/": "lawn/", "pest/": "es/plagas/", "es/plagas/": "pest/" };
const browser = await chromium.launch();
let fails = 0;
const fail = (m) => { fails++; console.log("FAIL", m); };
for (const [w, h, tag] of [[1440, 900, "desktop"], [390, 844, "mobile"]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  for (const [name, path] of pages) {
    const page = await ctx.newPage();
    const errs = [];
    page.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
    page.on("pageerror", (e) => errs.push(String(e)));
    page.on("requestfailed", (r) => errs.push("reqfail " + r.url()));
    const resp = await page.goto(base + path, { waitUntil: "networkidle" });
    if (resp.status() !== 200) fail(`${name} status ${resp.status()}`);
    await page.evaluate(() => document.fonts.ready);
    const ov = await page.evaluate(() => {
      const sw = document.documentElement.scrollWidth, cw = document.documentElement.clientWidth;
      const wide = [...document.querySelectorAll("body *")].filter(e => { const r = e.getBoundingClientRect(); return r.right > cw + 1 && getComputedStyle(e).position !== "fixed"; }).slice(0, 5).map(e => e.tagName + "." + e.className);
      return { sw, cw, wide };
    });
    if (ov.sw > ov.cw) fail(`${name}@${w} overflow ${ov.sw}>${ov.cw} ${ov.wide}`);
    const wa = await page.$$eval('a[href*="wa.me"]', as => [...new Set(as.map(a => a.href.match(/wa\.me\/(\d+)/)[1]))]);
    for (const n of wa) if (!["50498350265", "50488695915"].includes(n)) fail(`${name} bad wa ${n}`);
    if (name.startsWith("home") && wa.length !== 2) fail(`${name} expected both WA numbers, got ${wa}`);
    const bad = await page.evaluate(() => /claude|anthropic|\bjoru\b|\bAI\b|lorem/i.test(document.documentElement.outerHTML.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/, "")));
    if (bad) fail(`${name} forbidden word`);
    // language toggle
    const toggle = await page.$('.lang a');
    const href = await toggle.getAttribute("href");
    if (tag === "desktop") {
      await Promise.all([page.waitForNavigation(), toggle.click()]);
      const now = page.url().replace(base, "");
      if (now !== pairs[path]) fail(`${name} toggle went to '${now}' expected '${pairs[path]}'`);
      await page.goBack({ waitUntil: "networkidle" });
    }
    if (errs.length) fail(`${name}@${w} console: ${errs.join(" | ")}`);
    if (tag === "mobile") await page.screenshot({ path: `${out}/${name}-${tag}-fold.png` });
    await page.addStyleTag({ content: ".wa-bar{position:static!important}.site-footer{padding-bottom:28px!important}" });
    await page.screenshot({ path: `${out}/${name}-${tag}.png`, fullPage: true });
    console.log("ok", name, tag, "wa:", wa.join(","), "toggle->", href);
    await page.close();
  }
  // mobile menu
  if (tag === "mobile") {
    const page = await ctx.newPage();
    await page.goto(base, { waitUntil: "networkidle" });
    await page.click(".nav-toggle");
    await page.screenshot({ path: `${out}/home-en-mobile-menu.png` });
    const vis = await page.isVisible("#nav-menu");
    if (!vis) fail("mobile menu not visible");
    await page.close();
  }
  await ctx.close();
}
// 404
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const r = await page.goto(base + "nope-xyz/", { waitUntil: "networkidle" });
  console.log("404 status", r.status());
  await page.screenshot({ path: `${out}/404-mobile.png` });
  await ctx.close();
}
await browser.close();
console.log(fails ? `${fails} FAILURES` : "ALL CHECKS PASSED");
