import {
  SnakeHead,
  SnakeTail,
} from "@python-italia/pycon-styleguide/illustrations";
import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { queryTalk } from "~/types";

export const config = {
  runtime: "edge",
};

const regularFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Regular.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());
const boldFont = fetch(
  new URL(
    "../../../../../social-card-font/GeneralSans-Bold.otf",
    import.meta.url,
  ),
).then((res) => res.arrayBuffer());

export const handler = async (req: NextRequest) => {
  const regularFontData = await regularFont;
  const boldFontData = await boldFont;
  const client = createClient();
  const { searchParams } = new URL(req.url);

  const language = searchParams.get("lang");
  const slug = searchParams.get("slug");

  const {
    data: { conference },
  } = await queryTalk(client, {
    slug,
    language,
    code: process.env.conferenceCode,
  });
  const talk = conference?.talk;

  const title = talk.title;
  const speakers = talk.speakers.map((speaker) => speaker.fullName).join(", ");

  return new ImageResponse(
    <div
      style={{
        background: "#F17A5D",
        width: "100%",
        height: "100%",
        display: "flex",
        textAlign: "left",
        alignItems: "flex-start",
        justifyContent: "center",
        flexDirection: "column",
        paddingLeft: "64px",
        paddingRight: "64px",
        fontFamily: '"GeneralSans"',
      }}
    >
      <div
        style={{
          fontSize: "64px",
          fontWeight: 700,
          color: "#0E1116",
          paddingBottom: "16px",
        }}
      >
        {title}
      </div>
      <div
        style={{
          fontSize: "32px",
          color: "#FAF5F3",
          paddingRight: 220,
          fontWeight: 500,
        }}
      >
        {speakers}
      </div>
      <div
        style={{
          display: "flex",
          position: "absolute",
          bottom: 0,
          right: 160,
        }}
      >
        <SnakeHead />
      </div>
      <div
        style={{
          display: "flex",
          position: "absolute",
          bottom: 0,
          right: 20,
          transform: "rotate(180deg)",
        }}
      >
        <SnakeTail />
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
          data: boldFontData,
          style: "normal",
          weight: 700,
        },
      ],
    },
  );
};

export default handler;
