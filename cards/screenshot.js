const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const filePath = 'file://' + path.resolve(__dirname, 'cards.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);

  const ids = ['card-1', 'card-2', 'card-3', 'card-4', 'card-5', 'card-6'];
  for (const id of ids) {
    const el = await page.$('#' + id);
    await el.screenshot({ path: path.resolve(__dirname, 'output', id + '.png') });
    console.log('Saved', id);
  }

  await browser.close();
})();
