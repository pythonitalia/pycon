require("dotenv").config();
const chunk = require("lodash.chunk");
const puppeteer = require("puppeteer");
const assert = require("assert");
const fs = require("fs");
const archiver = require("archiver");

const EMPTY_BADGES_COUNT = {
  ATTENDEE: 100,
  SPEAKER: 25,
  STAFF: 20,
  SPONSOR: 20,
  KEYNOTER: 5,
  DJANGO_GIRLS: 25,
};

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

const getConferenceRoleForTicketData = async (orderPosition) => {
  const request = await fetch("https://beri.python.it/graphql", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Backend-Token": process.env.BERI_API_TOKEN,
    },
    body: JSON.stringify({
      query: `query ConferenceRole($ticketData: String!, $conferenceCode: String!) {
          conferenceRoleForTicketData(
            rawTicketData: $ticketData
            conferenceCode: $conferenceCode
          ) {
            role
            ticketHashid
          }
        }`,
      variables: {
        ticketData: JSON.stringify(orderPosition),
        conferenceCode: "pycon2023",
      },
    }),
  });
  const response = await request.json();
  return response.data.conferenceRoleForTicketData;
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
  }

  return positions;
};

const createEmptyBadgeOrderPositions = () => {
  return Object.entries(EMPTY_BADGES_COUNT).flatMap(([role, count]) => {
    return Array.from({ length: count }, (_, i) => ({
      attendee_name: "",
      empty: true,
      role,
      answers: [],
    }));
  });
};

(async () => {
  fs.rmSync("generated-badges", { recursive: true });
  fs.mkdirSync("generated-badges");

  const allOrderPositions = [
    ...(await getAllOrderPositions()),
    ...createEmptyBadgeOrderPositions(),
  ];

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

  const createBadgeData = async (orderPosition, side) => {
    if (!orderPosition) {
      return {
        name: "",
        pronouns: "",
        tagline: "",
        empty: true,
        role: "ATTENDEE",
        side,
      };
    }

    if (orderPosition.empty) {
      return {
        name: "",
        pronouns: "",
        tagline: "",
        empty: true,
        role: orderPosition.role,
        side,
      };
    }

    const answers = orderPosition.answers;
    let pronouns =
      answers.find((a) => a.question === pronounsQuestion.id)?.answer ?? "";

    if (pronouns === "--") {
      pronouns = "";
    }

    const tagline =
      answers.find((a) => a.question === taglineQuestion.id)?.answer ?? "";

    const { role, ticketHashid } =
      await getConferenceRoleForTicketData(orderPosition);
    return {
      name: orderPosition.attendee_name,
      pronouns,
      tagline,
      role,
      hashedTicketId: ticketHashid,
      side,
      empty: false,
    };
  };

  await page.goto("https://pycon.it/en/badge");
  await page.waitForNetworkIdle();
  await page.setViewport({ width: 1080, height: 2000 });

  const archive = archiver("zip", {
    zlib: { level: 9 },
  });
  const output = fs.createWriteStream("badges.zip");

  output.on("close", () => {
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
      const item1 = await createBadgeData(group[0], side);
      const item2 = await createBadgeData(group[1], side);
      const item3 = await createBadgeData(group[2], side);
      const item4 = await createBadgeData(group[3], side);

      const badgeData =
        side === "front"
          ? [item1, item2, item3, item4]
          : [item2, item1, item4, item3];

      await page.evaluate((badgeData) => {
        window.setBadgeData(badgeData);
      }, badgeData);

      const filename = `${String(counter).padStart(3, "0")}-${
        side === "front" ? "fronte" : "retro"
      }.pdf`;
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
