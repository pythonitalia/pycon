import {
  SnakeHead,
  SnakeTail,
} from "@python-italia/pycon-styleguide/illustrations";
import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { Logo } from "~/components/logo";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import { queryNewsArticle, querySocialCard, useSocialCardQuery } from "~/types";

export const config = {
  runtime: "edge",
};

const regularFont = fetch(
  new URL("../../../social-card-font/GeneralSans-Regular.otf", import.meta.url),
).then((res) => res.arrayBuffer());
const boldFont = fetch(
  new URL("../../../social-card-font/GeneralSans-Bold.otf", import.meta.url),
).then((res) => res.arrayBuffer());
const mainIllustration = fetch(
  new URL("../../../../public/images/main-illustration.png", import.meta.url),
).then((res) => res.arrayBuffer());

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
  const regularFontData = await regularFont;
  const boldFontData = await boldFont;
  const client = createClient();
  const mainIllustrationResponse = await mainIllustration;
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
      {/* @ts-ignore */}
      <img width={600} height={600} src={mainIllustrationResponse} alt="" />
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
            height: 600 - 180 - 14 * 2,
            marginLeft: "6px",
            flexDirection: "column",
            justifyContent: "center",
            padding: "50px",
          }}
        >
          <div
            style={{
              fontSize: "48px",
              fontWeight: "bold",
              marginBottom: "10px",
              display: "flex",
              textTransform: "uppercase",
            }}
          >
            Florence
          </div>
          <div
            style={{
              fontSize: "48px",
              fontWeight: "bold",
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
              fontWeight: "bold",
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
              fontWeight: "bold",
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
      height: 600,
      fonts: [
        {
          name: "GeneralSans",
          data: regularFontData,
          style: "normal",
          weight: 500,
        },
        {
          name: "GeneralSans",
          data: boldFontData,
          style: "normal",
          weight: 700,
        },
      ],
    },
  );
};

export default handler;
