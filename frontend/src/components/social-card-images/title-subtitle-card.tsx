import {
  SnakeHead,
  SnakeTail,
} from "@python-italia/pycon-styleguide/illustrations";
import { ImageResponse } from "@vercel/og";

import type { NextRequest } from "next/server";

import { createClient } from "~/apollo/create-client";
import { queryTalk } from "~/types";

export const TitleSubtitleCard = ({
  title,
  subtitle,
}: {
  title: string;
  subtitle: string;
}) => (
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
      {subtitle}
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
  </div>
);
