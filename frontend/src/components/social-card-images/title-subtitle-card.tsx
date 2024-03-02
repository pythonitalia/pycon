import { colors } from "@python-italia/pycon-styleguide/config-parts";
import {
  SnakeHead,
  SnakeTail,
} from "@python-italia/pycon-styleguide/illustrations";
import { getTagColor } from "../schedule-event-detail/event-tag";

const bgForTag = (tag: string) => {
  const colorName = getTagColor(tag);
  return colors[colorName].light;
};

export const TitleSubtitleCard = ({
  title,
  subtitle,
  tag,
}: {
  title: string;
  subtitle: string;
  tag?: string;
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
    {tag && (
      <div
        style={{
          border: "3px solid #0E1116",
          paddingTop: "8px",
          paddingBottom: "8px",
          paddingRight: "16px",
          paddingLeft: "16px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: bgForTag(tag),
          textTransform: "uppercase",
          fontWeight: "semibold",
          marginBottom: "16px",
        }}
      >
        {tag}
      </div>
    )}
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
