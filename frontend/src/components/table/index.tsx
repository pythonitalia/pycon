/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment } from "react";
import { Box, Grid, jsx } from "theme-ui";

type Props<T> = {
  headers: string[];
  mobileHeaders?: string[];
  data: T[];
  rowGetter: (item: T) => any[];
  keyGetter: (item: T) => string;
  colorful?: boolean;
};

const COLORS = ["violet", "keppel", "orange"];

const getHeaderColor = (index: number, colorful: boolean) => {
  if (!colorful) {
    return "orange";
  }

  return COLORS[index % COLORS.length];
};

export const Table = <T,>({
  headers,
  data,
  rowGetter,
  keyGetter,
  mobileHeaders,
  colorful = false,
}: Props<T>) => (
  <Grid
    gap={0}
    sx={{
      width: "100%",
      fontSize: 2,
      rowGap: [1, 0],
      gridTemplateColumns: [
        "repeat(1, minmax(0, 1fr))",
        `repeat(${headers.length}, minmax(0, 1fr))`,
      ],
    }}
  >
    {headers.map((header, index) => (
      <Box
        key={index}
        as="div"
        sx={{
          display: ["none", "inline-block"],
          color: getHeaderColor(index, colorful),
          textTransform: "uppercase",
          textAlign: "left",
          pb: 3,
          fontWeight: "bold",
        }}
      >
        {header}
      </Box>
    ))}
    {data.map((item, index) => {
      const row = rowGetter(item);

      return (
        <Fragment key={index}>
          {row.map((content, index) => {
            const mobileHeader = (mobileHeaders ?? headers)[index];
            return (
              <Box
                key={keyGetter(content)}
                sx={{
                  display: "flex",
                  alignItems: "center",
                  borderTop: [null, "primary"],
                  py: [0, 3],
                  pr: [0, 3],
                  wordBreak: "break-word",
                  "&:before": mobileHeader
                    ? {
                        content: `'${mobileHeader}:'`,
                        color: "orange",
                        textTransform: "uppercase",
                        textAlign: "left",
                        fontWeight: "bold",
                        mr: 2,
                        display: ["inline-block", "none"],
                      }
                    : {},
                }}
              >
                {content}
              </Box>
            );
          })}
        </Fragment>
      );
    })}
  </Grid>
);
