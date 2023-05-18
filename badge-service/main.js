require("dotenv").config();
const chunk = require("lodash.chunk");
const puppeteer = require("puppeteer");
const assert = require("assert");
const fs = require("fs");
const archiver = require("archiver");

const getAllQuestions = async () => {
  const request = await fetch(
    "https://tickets.pycon.it/api/v1/organizers/python-italia/events/pyconit2023/questions/",
    {
      headers: {
        Authorization: `Token ${process.env.PRETIX_API_TOKEN}`,
      },
    },
  );
  const response = await request.json();
  return response.results;
};

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
    break;
  }

  console.log("response", positions.length);
  return positions;
};

(async () => {
  fs.rmSync("generated-badges", { recursive: true });
  fs.mkdirSync("generated-badges");

  const allOrderPositions = await getAllOrderPositions();
  const questions = await getAllQuestions();

  const pronounsQuestion = questions.find((q) => q.identifier === "SMZHLTGP");
  const taglineQuestion = questions.find((q) => q.identifier === "83HY8DTB");

  assert(pronounsQuestion);
  assert(taglineQuestion);

  const browser = await puppeteer.launch({
    headless: "new",
  });
  const page = await browser.newPage();
  let counter = 0;

  const createBadgeData = (orderPosition, side) => {
    if (!orderPosition) {
      return {};
    }

    const answers = orderPosition.answers;
    const pronouns =
      answers.find((a) => a.question === pronounsQuestion.id)?.answer ?? "";
    const tagline =
      answers.find((a) => a.question === taglineQuestion.id)?.answer ?? "";
    return {
      name: orderPosition.attendee_name,
      pronouns,
      tagline,
      role: "staff",
      hashedTicketId: "1",
      side,
    };
  };

  await page.goto("https://pycon.it/en/badge");
  await page.waitForNetworkIdle();
  await page.setViewport({ width: 1080, height: 2000 });

  const archive = archiver("zip", {
    zlib: { level: 9 },
  });
  const output = fs.createWriteStream("badges.zip");

  output.on("close", function () {
    console.log("Badges generated.");
  });

  archive.on("error", (err) => {
    throw err;
  });

  archive.on("warning", (err) => {
    if (err.code === "ENOENT") {
      // log warning
      console.log("warning:", err);
    } else {
      // throw error
      throw err;
    }
  });

  archive.pipe(output);

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

      const filename = `${String(counter).padStart(3, "0")}-${side}.pdf`;
      const buffer = await page.pdf({
        path: `generated-badges/${filename}`,
        width: "23cm",
        height: "33cm",
      });
      archive.append(buffer, { name: filename });
    }

    counter = counter + 1;
  }

  await browser.close();
  archive.finalize();
})();
