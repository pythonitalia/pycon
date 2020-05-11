import { NowRequest, NowResponse } from "@now/node";
import chromium from "chrome-aws-lambda";
import puppeteer from "puppeteer-core";

export default async (req: NowRequest, res: NowResponse) => {
  const type = "png";
  const path = (req.query.path as string[]).join("/");
  const url = `https://${req.headers.host}/${path}/social`;

  console.log("Taking screenshot of", url);

  try {
    const size = { height: 630, width: 1200 };

    const browser = await puppeteer.launch({
      // Required
      executablePath: await chromium.executablePath,

      // Optional
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      headless: true,
    });

    const page = await browser.newPage();
    await page.setViewport({ ...size, deviceScaleFactor: 2 });
    await page.goto(url);

    const file = await page.screenshot();

    res.statusCode = 200;
    res.setHeader("Content-Type", `image/${type}`);
    res.end(file);
  } catch (e) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "text/html");
    res.end("<h1>Server Error</h1><p>Sorry, there was a problem</p>");
    console.error(e.message);
  }
};
