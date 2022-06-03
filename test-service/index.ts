const puppeteer = require("puppeteer");

const screenshots = [
  // {
  //   day: "2022-06-03",
  //   states: [
  //     {
  //       title: "mattina",
  //       scroll: 0,
  //     },
  //     {
  //       title: "pomeriggio",
  //       scroll: 1050,
  //     },
  //     {
  //       title: "sera",
  //       scroll: 1050,
  //     },
  //   ],
  // },
  {
    day: "2022-06-04",
    states: [
      {
        title: "mattina",
        scroll: 0,
      },
      {
        title: "pomeriggio",
        scroll: 1050,
      },
      // {
      //   title: "sera",
      //   scroll: 1050,
      // },
    ],
  },
];

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });

  for (const screenshot of screenshots) {
    await page.goto(`https://pycon.it/en/schedule/${screenshot.day}?photo=1`, {
      waitUntil: "networkidle2",
    });
    for (const state of screenshot.states) {
      // @ts-ignore
      await page.evaluate((value) => {
        // @ts-ignore
        window.scrollBy(0, 0);
        // @ts-ignore
        window.requestAnimationFrame(() => {
          // @ts-ignore
          window.scrollBy(0, value);
        });
        // @ts-ignore
      }, state.scroll);
      await page.screenshot({
        path: `programma-${screenshot.day}-${state.title}.jpeg`,
      });
    }
  }

  await browser.close();
})();
