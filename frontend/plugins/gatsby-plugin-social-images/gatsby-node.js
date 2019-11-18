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

    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 2 });
    await page.goto(`file://${pagePath}`);
    await page.evaluate(
      (cwd, root) => {
        const images = Array.from(
          document.querySelectorAll('img[src^="/static"]'),
        );

        images.forEach(x => {
          const src = x.getAttribute("src");
          const newSrc = `${cwd}/${root}${src}`;

          x.setAttribute("src", `file://${newSrc}`);
        });
      },
      process.cwd(),
      rootDir,
    );
    await page.screenshot({ path: screenshotPath });
  });

  await Promise.all(renderingJobs);

  return await browser.close();
};

exports.onCreatePage = ({ page, actions }) => {
  if (page.path.endsWith("/social")) {
    pages.push(page.path);
  }
};
