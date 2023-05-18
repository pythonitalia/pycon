require("dotenv").config();
const chunk = require("lodash.chunk");
const puppeteer = require("puppeteer");

const getAllOrderPositions = async () => {
  let next =
    "https://tickets.pycon.it/api/v1/organizers/python-italia/events/pyconit2023/checkinlists/24/positions/";
  const positions = [];
  while (next) {
    const request = await fetch(next, {
      headers: {
        Authorization: `Token ${process.env.PRETIX_API_TOKEN}`,
      },
    });
    const response = await request.json();
    next = response.next;

    positions.push(...response.results);
  }

  console.log("response", positions.length);
  return positions;
};

const createBadgeData = (position, side) => ({
  name: position.attendee_name,
  pronouns: "he/him",
  tagline: "My tag line says something about you!",
  role: "Staff",
  hashedTicketId: "1",
  side,
});

(async () => {
  const allOrderPositions = await getAllOrderPositions();
  const browser = await puppeteer.launch({
    headless: "new",
  });
  const page = await browser.newPage();

  await page.goto("https://pycon.it/en/badge");
  await page.waitForNetworkIdle();
  await page.setViewport({ width: 1080, height: 2000 });

  for (const group of chunk(allOrderPositions, 4)) {
    for (const side of ["front", "back"]) {
      const item1 = createBadgeData(group[0], side);
      const item2 = createBadgeData(group[1], side);
      const item3 = createBadgeData(group[2], side);
      const item4 = createBadgeData(group[3], side);

      const badgeData =
        side === "front"
          ? [item1, item2, item3, item4]
          : [item2, item1, item4, item3];

      await page.evaluate((badgeData) => {
        window.setBadgeData(badgeData);
      }, badgeData);
      await page.pdf({
        path: `test-${side}.pdf`,
        width: "25cm",
        height: "35cm",
      });
    }

    break;
  }

  await browser.close();
})();
