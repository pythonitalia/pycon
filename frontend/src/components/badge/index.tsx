import { Text } from "@python-italia/pycon-styleguide";

import {
  BADGE_INSIDE_WIDTH_PX,
  BADGE_INSIDE_HEIGHT_PX,
  CUT_LINE_SIZE_PX,
  CUT_LINE_SIZE_2_PX,
} from "~/pages/badge";

// import satori from 'satori'

export const Badge = () => {
  return (
    <div
      style={{
        backgroundColor: "#000000",
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
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
          paddingLeft: "20px",
          paddingRight: "20px",
          paddingBottom: "20px",
          position: "relative",
          // border: "1px solid blue",
        }}
      >
        <CutLines position="topLeft" />
        <CutLines position="topRight" />
        <CutLines position="bottomLeft" />
        <CutLines position="bottomRight" />

        {/* badge */}

        {/*<div
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <div
            style={{
              width: "16px",
              height: "16px",
              backgroundColor: "#ffffff",
              borderRadius: "100%",
            }}
          ></div>
          </div>*/}

        <img
          style={{
            width: "113px",
            height: "34px",
            marginBottom: "34px",
            marginTop: "50px",
          }}
          src="https://pythonit-email-assets.s3.eu-central-1.amazonaws.com/logo-pycon-2023.png"
        />
        <div
          style={{
            fontSize: "20px",
            fontWeight: 400,
            color: "#FAF5F3",
            marginBottom: "4px",
          }}
        >
          She/Her
        </div>
        <div
          style={{
            color: "#FAF5F3",
            fontSize: "40px",
            fontWeight: 600,
            lineHeight: "35px",
          }}
        >
          Jessica Bandini
        </div>
        <div
          style={{
            width: "100%",
            marginTop: "16px",
            marginBottom: "16px",
            border: "1px solid #FAF5F3",
          }}
        />
        <div
          style={{
            fontSize: "20px",
            fontWeight: 400,
            color: "#FAF5F3",
          }}
        >
          Guy with impostor syndrome during oce hours, DS in the remaining time
        </div>
        <div
          style={{
            marginTop: "auto",
            width: "100%",
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "flex-end",
          }}
        >
          <img
            style={{
              height: "70px",
              width: "70px",
            }}
            src="https://cdn.britannica.com/17/155017-050-9AC96FC8/Example-QR-code.jpg"
          />
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
        transform: `translateX(-100%)`,
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: `translateY(-100%)`,
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
        transform: `translateX(-100%)`,
      };
      line2 = {
        width: CUT_LINE_SIZE_2_PX,
        height: CUT_LINE_SIZE_PX,

        transform: `translateY(100%)`,
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
        transform: `translateY(-100%) translateX(-100%)`,
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: `translateX(100%)`,
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
        transform: `translateY(100%) translateX(-100%)`,
      };
      line2 = {
        width: CUT_LINE_SIZE_PX,
        height: CUT_LINE_SIZE_2_PX,

        transform: `translateX(100%)`,
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
      ></div>
      <div
        style={{
          position: "absolute",
          backgroundColor: "#ffffff",
          display: "flex",
          ...line2,
        }}
      ></div>
    </div>
  );
};
