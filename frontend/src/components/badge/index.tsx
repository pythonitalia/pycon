import { SnakeLongNeck } from "@python-italia/pycon-styleguide/illustrations";
import QRCode from "react-qr-code";
import Balancer from "react-wrap-balancer";

import {
  BADGE_INSIDE_HEIGHT_PX,
  BADGE_INSIDE_WIDTH_PX,
  CUT_LINE_SIZE_2_PX,
  CUT_LINE_SIZE_PX,
} from "~/pages/badge";
import { ConferenceRole } from "~/types";

const BADGE_TYPE_TO_COLOR = {
  [ConferenceRole.Attendee]: "#F17A5D",
  [ConferenceRole.Speaker]: "#34B4A1",
  [ConferenceRole.Sponsor]: "#9473B0",
  [ConferenceRole.Staff]: "#F8B03D",
  [ConferenceRole.Keynoter]: "#79CDE0",
  [ConferenceRole.DjangoGirls]: "#E94135",
};

const BADGE_TYPE_TO_NAME = {
  [ConferenceRole.Attendee]: "Attendee",
  [ConferenceRole.Speaker]: "Speaker",
  [ConferenceRole.Sponsor]: "Sponsor",
  [ConferenceRole.Staff]: "Staff",
  [ConferenceRole.Keynoter]: "Keynoter",
  [ConferenceRole.DjangoGirls]: "Django Girls",
};

type Props = {
  cutLines?: boolean;
  pronouns?: string;
  tagline?: string;
  name?: string;
  role?: ConferenceRole;
  hashedTicketId?: string;
  side?: "front" | "back";
  empty?: boolean;
};

export const Badge = ({
  cutLines = true,
  name = "Example",
  pronouns = "they/them",
  tagline = "Example tagline",
  role = ConferenceRole.Attendee,
  hashedTicketId = "",
  side = "front",
  empty = false,
}: Props) => {
  return (
    <div
      style={{
        backgroundColor: "#000000",
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          width: BADGE_INSIDE_WIDTH_PX,
          height: BADGE_INSIDE_HEIGHT_PX,
          background: "#000000",
          display: "flex",
          flexDirection: "column",
          textAlign: "left",
          paddingLeft: "25px",
          paddingRight: "25px",
          paddingBottom: "25px",
          position: "relative",
        }}
      >
        {cutLines && (
          <>
            <CutLines position="topLeft" />
            <CutLines position="topRight" />
            <CutLines position="bottomLeft" />
            <CutLines position="bottomRight" />
          </>
        )}

        {/* badge */}

        <img
          alt=""
          style={{
            width: "113px",
            height: "34px",
            marginBottom: "20px",
            marginTop: "25px",
          }}
          src="https://pythonit-email-assets.s3.eu-central-1.amazonaws.com/logo-pycon-2024.png"
        />
        <div
          style={{
            fontSize: "14px",
            fontWeight: 400,
            color: "#FCE8DE",
            marginBottom: "10px",
            opacity: pronouns ? 1 : 0,
          }}
        >
          {pronouns || "empty"}
        </div>
        {!empty && (
          <div
            style={{
              color: "#FAF5F3",
              // fontSize: "40px",
              // fontSize: "32px",
              fontWeight: 600,
              lineHeight: "38px",
              wordBreak: "break-word",
            }}
            className="!text-[32px] [&>span]:text-[32px]"
          >
            <Balancer ratio={0.3}>{name}</Balancer>
          </div>
        )}
        {empty && (
          <div
            style={{
              height: "150px",
              background: "#ffffff",
            }}
          />
        )}
        <div
          style={{
            width: "100%",
            marginTop: "20px",
            marginBottom: "15px",
            border: "1px solid #FAF5F3",
          }}
        />
        <div
          style={{
            fontSize: "32px",
            color: BADGE_TYPE_TO_COLOR[role],
            fontWeight: 600,
            textTransform: "capitalize",
          }}
        >
          {BADGE_TYPE_TO_NAME[role]}
        </div>
        <div
          style={{
            marginTop: "auto",
            width: "100%",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
          }}
        >
          <div
            style={{
              fontWeight: 400,
              color: "#FCE8DE",
              marginRight: "25px",
              maxWidth: "153px",
            }}
            className="!text-[13px] [&>span]:text-[13px]"
          >
            <Balancer>{tagline.substring(0, 400)}</Balancer>
          </div>

          {!empty && side === "front" && (
            <div className="p-[2px] bg-white">
              <QRCode
                className="shrink-0"
                value={`https://pycon.it/b/${hashedTicketId}`}
                size={70}
              />
            </div>
          )}
          {(empty || side === "back") && (
            <div className="p-[2px] relative">
              <div className="w-[70px] h-[70px]" />
              <SnakeLongNeck className="w-[70px] top-[-30px] absolute" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const CutLines = ({
  position,
}: {
  position: "topRight" | "topLeft" | "bottomRight" | "bottomLeft";
}) => {
  let container = {};
  let line1 = {};
  let line2 = {};

  switch (position) {
    case "topLeft":
      container = {
        top: 0,
        left: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,
        top: 0,
        left: 0,
        transform: "translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: "translateY(-100%)",
        top: 0,
        left: 0,
      };
      break;
    case "bottomLeft":
      container = {
        bottom: 0,
        left: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,
        bottom: 0,
        left: 0,
        transform: "translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: "translateY(100%)",
        bottom: 0,
        left: 0,
      };
      break;
    case "topRight":
      container = {
        top: 0,
        right: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,
        top: 0,
        left: 0,
        transform: "translateY(-100%) translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: "translateX(100%)",
        top: 0,
        right: 0,
      };
      break;
    case "bottomRight":
      container = {
        bottom: 0,
        right: 0,
      };
      line1 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,
        bottom: 0,
        left: 0,
        transform: "translateY(100%) translateX(-100%)",
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: "translateX(100%)",
        bottom: 0,
        right: 0,
      };
      break;
  }

  return (
    <div
      style={{
        position: "absolute",
        display: "flex",
        ...container,
      }}
    >
      {/* cut lines */}
      <div
        style={{
          position: "absolute",
          backgroundColor: "#ffffff",
          display: "flex",
          ...line1,
        }}
      />
      <div
        style={{
          position: "absolute",
          backgroundColor: "#ffffff",
          display: "flex",
          ...line2,
        }}
      />
    </div>
  );
};
