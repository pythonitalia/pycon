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

    const size = { width: 1200, height: 630 };

    if (pagePath.endsWith("square/index.html")) {
      size.height = size.width;
    }

    if (pagePath.endsWith("twitter/index.html")) {
      size.height = 600;
    }

    const page = await browser.newPage();
    await page.setViewport({ ...size, deviceScaleFactor: 2 });

    try {
      await page.goto(`file://${pagePath}`);
    } catch (e) {
      console.log(`Unable to go to {pagePath}, error: ${e}`);
    }
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

  if (page.path.endsWith("/social-square")) {
    pages.push(page.path);
  }

  if (page.path.endsWith("/social-twitter")) {
    pages.push(page.path);
  }
};
