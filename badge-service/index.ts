import * as puppeteer from "puppeteer";
import { Client } from "pg";
import { exec } from "node:child_process";

const DB_PASSWORD = process.env.PYCON_DB;
const PRETIX_TOKEN = process.env.PRETIX_TOKEN;

(async () => {
  const keynotesVouchersIds = [275, 273, 278, 277, 274, 276];
  const conferenceID = 2;
  const allItems = [];
  let next =
    "https://tickets.pycon.it/api/v1/organizers/python-italia/events/pycon12/checkinlists/14/positions/";

  while (next !== null) {
    const request = await fetch(next, {
      headers: {
        Authorization: `Token ${PRETIX_TOKEN}`,
      },
    });

    const data = await request.json();
    allItems.push(...data.results);

    next = data.next;
    // next = null;
  }

  const pyconDB = new Client({
    user: "root",
    host: "localhost",
    database: "productionbackend",
    password: DB_PASSWORD,
    port: 7777,
  });

  const usersDB = new Client({
    user: "root",
    host: "localhost",
    database: "users",
    password: DB_PASSWORD,
    port: 7777,
  });

  pyconDB.connect();
  usersDB.connect();

  const schedule = await pyconDB.query(
    `SELECT submission.speaker_id AS user_id
    FROM schedule_scheduleitem AS scheduleitem
    INNER JOIN submissions_submission AS submission ON submission.id = scheduleitem.submission_id
    WHERE scheduleitem.conference_id = $1`,
    [conferenceID],
  );

  const additionalSpeakers = await pyconDB.query(
    `SELECT additional_speaker.user_id AS user_id
    FROM schedule_scheduleitem_additional_speakers AS additional_speaker
    INNER JOIN schedule_scheduleitem AS scheduleitem ON additional_speaker.scheduleitem_id = scheduleitem.id
    WHERE scheduleitem.conference_id = $1`,
    [conferenceID],
  );

  const speakersIds = schedule.rows.map((row) => row.user_id);
  const additionalSpeakersIds = additionalSpeakers.rows.map(
    (row) => row.user_id,
  );

  const allSpeakersIds = [...speakersIds, ...additionalSpeakersIds];

  const speakersQuery = await usersDB.query(
    `SELECT email, full_name, name
    FROM users
    WHERE id = ANY($1)`,
    [allSpeakersIds],
  );
  // const speakersData = speakersQuery.rows;
  const speakersEmails: string[] = speakersQuery.rows.map(
    (row: { email: string }) => row.email.toLowerCase(),
  );

  const counter = {
    speaker: 0,
    keynoter: 0,
    participant: 0,
    staff: 0,
  };

  const browser = await puppeteer.launch();
  exec("mkdir badges/");

  try {
    const badgeNameQuestionId = "77SLGY9Q";
    const taglineQuestionId = "83HY8DTB";

    const page = await browser.newPage();
    await page.goto("http://127.0.0.1:3000/en/badge", {
      waitUntil: "networkidle2",
    });
    await page.waitForTimeout(100);

    for (const item of allItems) {
      const attendeeName: string = item.attendee_name;
      const tagline = item.answers.filter(
        (answer) => answer.question_identifier === taglineQuestionId,
      )[0]?.answer;
      const badgeNameAnswer = item.answers.filter(
        (answer) => answer.question_identifier === badgeNameQuestionId,
      )[0]?.answer;
      const badgeName = badgeNameAnswer || attendeeName;
      const attendeeEmail: string = item.attendee_email.toLowerCase();

      let variant = "participant";
      if (keynotesVouchersIds.indexOf(item.voucher) !== -1) {
        variant = "keynoter";
      } else if (speakersEmails.indexOf(attendeeEmail) !== -1) {
        variant = "speaker";
      }

      counter[variant] = counter[variant] + 1;

      await page.evaluate(
        (badgeName, tagline, variant) => {
          // @ts-ignore
          window.changeBadgeData({
            name: badgeName,
            tagline: tagline,
            variant: variant,
          });
        },
        badgeName,
        tagline,
        variant,
      );
      await page.pdf({
        path: `badges/${item.order}-${item.id}.pdf`,
        printBackground: true,
        width: "10cm",
        height: "10cm",
        preferCSSPageSize: false,
      });
    }

    exec("zip -r badges.zip badges/");
    console.log(
      `Created badges: ${counter.participant} participants, ${counter.speaker} speakers, ${counter.keynoter} keynoters, ${counter.staff} staff`,
    );
  } finally {
    await browser.close();

    pyconDB.end();
    usersDB.end();
  }
})();
