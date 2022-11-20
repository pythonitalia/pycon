/** @jsxRuntime classic */

/** @jsx jsx */
import { jsx } from "theme-ui";

export const SocialCircle = ({
  children,
  color,
  variant,
}: {
  color: string;
  variant?: string;
  children: any;
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
      paddingLeft: 0,
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
