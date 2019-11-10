/** @jsx jsx */
import { jsx } from "theme-ui";

export const SocialCircle: React.SFC<{ color: string; variant?: string }> = ({
  children,
  color,
  variant,
}) => (
  <li
    sx={{
      width: "40px",
      height: "40px",
      borderRadius: "100%",
      border: variant === "header" ? "3px solid black" : "",
      backgroundColor: color,
      flexShrink: 0,
      cursor: "pointer",
      a: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
      },
      svg: {
        path: {
          fill: "white",
        },
      },
    }}
  >
    {children}
  </li>
);
