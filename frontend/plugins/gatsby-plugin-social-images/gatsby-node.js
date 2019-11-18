const puppeteer = require("puppeteer");
const path = require("path");

let pages = [];

exports.onPostBuild = async (args, pluginOptions) => {
  const rootDir = `public`;
  const browser = await puppeteer.launch({ headless: true });

  const renderingJobs = pages.map(async p => {
    const parts = [process.cwd(), rootDir, p];

    if (!p.endsWith(".html")) {
      parts.push("index.html");
    }

    const pagePath = path.join(...parts);
    const screenshotPath = path.join(
      ...parts.splice(0, parts.length - 1),
      "social.png",
    );

    console.log(pagePath);
    console.log(screenshotPath);

    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 630 });
    await page.goto(`file://${pagePath}`);
    await page.screenshot({ path: screenshotPath });
  });

  await Promise.all(renderingJobs);

  return await browser.close();
};

exports.onCreatePage = ({ page, actions }) => {
  console.log(page.path);

  if (page.path.endsWith("/social")) {
    pages.push(page.path);
  }
};
