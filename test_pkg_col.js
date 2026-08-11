const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    extraHTTPHeaders: { 'Authorization': 'token 8756169fc0adebe:29829b4810f0db2' },
    viewport: { width: 1400, height: 900 },
  });
  const page = await context.newPage();
  await page.goto('http://localhost:8000/app/garage-service-order', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'gso_list_pkg.png' });
  await browser.close();
})();
