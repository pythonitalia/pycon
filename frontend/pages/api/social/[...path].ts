import { NowRequest, NowResponse } from "@now/node";
import puppeteer from "puppeteer";

export default async (req: NowRequest, res: NowResponse) => {
  const type = "png";
  const path = (req.query.path as string[]).join("/");
  const protocol = (req as any).protocol;
  const url = `${protocol}://${req.headers.host}/${path}/social`;

  try {
    const size = { height: 630, width: 1200 };

    const browser = await puppeteer.launch({ headless: true });
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
