import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { Logo } from "~/components/logo";
import type { Language } from "~/locale/languages";
import { querySocialCard } from "~/types";

export const config = {
  runtime: "edge",
  unstable_allowDynamic: ["/node_modules/.pnpm/**"],
};

const getDays = ({ start, end }: { start: string; end: string }) => {
  // assuming the same month
  const startDate = new Date(start);
  const endDate = new Date(end);

  return `${startDate.getUTCDate()} - ${endDate.getUTCDate()}`;
};

const getMonth = ({ end }: { end: string }, language: Language) => {
  const endDate = new Date(end);

  const formatter = new Intl.DateTimeFormat(language, {
    month: "long",
  });

  return formatter.format(endDate);
};

const getYear = ({ end }: { end: string }) => {
  const endDate = new Date(end);

  return endDate.getFullYear();
};

const handler = async (req: NextRequest) => {
  const regularFont = fetch(
    new URL(
      "./social-card-font/GeneralSans-Regular.otf",
      req.url.substring(0, req.url.lastIndexOf("/api")),
    ),
  ).then((res) => res.arrayBuffer());
  const semiBoldFont = fetch(
    new URL(
      "./social-card-font/GeneralSans-Semibold.otf",
      req.url.substring(0, req.url.lastIndexOf("/api")),
    ),
  ).then((res) => res.arrayBuffer());
  const mainIllustration = fetch(
    new URL(
      "./images/main-illustration.png",
      req.url.substring(0, req.url.lastIndexOf("/api")),
    ),
  ).then((res) => res.arrayBuffer());

  const [regularFontData, semiBoldFontData, mainIllustrationData] =
    await Promise.all([regularFont, semiBoldFont, mainIllustration]);
  const client = createClient();
  const { data } = await querySocialCard(client, {
    code: process.env.conferenceCode,
  });
  const { searchParams } = new URL(req.url);

  const language = searchParams.get("lang") as Language;

  return new ImageResponse(
    <div
      style={{
        background: "#000000",
        width: "100%",
        height: "100%",
        display: "flex",
        fontFamily: '"GeneralSans"',
      }}
    >
      <img
        width={600}
        height={"100%"}
        src={mainIllustrationData as unknown as string}
        alt=""
      />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Logo
          style={{
            width: 1200 - 600 - 8,
            marginTop: "7px",
            marginBottom: "7px",
          }}
        />
        <div
          style={{
            background: "#34B4A1",
            display: "flex",
            width: 1200 - 600 - 14 - 6,
            height: 630 - 180 - 14 * 2,
            marginLeft: "7px",
            flexDirection: "column",
            justifyContent: "center",
            padding: "50px",
          }}
        >
          <div
            style={{
              fontSize: "48px",
              fontWeight: "semibold",
              marginBottom: "10px",
              display: "flex",
              textTransform: "uppercase",
            }}
          >
            Bologna
          </div>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "semibold",
              marginBottom: "10px",
              display: "flex",
              textTransform: "uppercase",
            }}
          >
            {getDays(data.conference)}
          </div>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "semibold",
              display: "flex",
              marginBottom: "10px",
              textTransform: "uppercase",
            }}
          >
            {getMonth(data.conference, language)} {getYear(data.conference)}
          </div>
          <div
            style={{
              fontSize: "32px",
              fontWeight: "semibold",
              display: "flex",
              color: "#ffffff",
              textTransform: "uppercase",
              marginTop: "auto",
            }}
          >
            {data.conference.name}
          </div>
        </div>
      </div>
    </div>,
    {
      width: 1200,
      height: 630,
      fonts: [
        {
          name: "GeneralSans",
          data: regularFontData,
          style: "normal",
          weight: 500,
        },
        {
          name: "GeneralSans",
          data: semiBoldFontData,
          style: "normal",
          weight: 600,
        },
      ],
    },
  );
};

export default handler;
