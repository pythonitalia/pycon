/** @jsxRuntime classic */
/** @jsx jsx */
import React, { Fragment } from "react";
import { Box, Grid, jsx } from "theme-ui";

type Props<T> = {
  headers: string[];
  mobileHeaders: string[];
  data: T[];
  rowGetter: (item: T) => any[];
  keyGetter: (item: T) => string;
};

export const Table = <T,>({
  headers,
  data,
  rowGetter,
  keyGetter,
  mobileHeaders,
}: Props<T>) => (
  <Grid
    gap={0}
    columns={[1, headers.length]}
    sx={{
      width: "100%",
      fontSize: 2,
    }}
  >
    {headers.map((header, index) => (
      <Box
        key={index}
        as="th"
        sx={{
          display: ["none", "inline-block"],
          color: "orange",
          textTransform: "uppercase",
          textAlign: "left",
          pb: 3,
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
            const mobileHeader = mobileHeaders[index];
            return (
              <Box
                key={keyGetter(content)}
                sx={{
                  borderTop: [null, "primary"],
                  py: [0, 3],
                  pr: [0, 2],
                  wordBreak: "break-word",
                  [`&:nth-of-type(${headers.length}n)`]: {
                    pb: [3, 0],
                  },
                  "&:last-child": {
                    pb: 0,
                  },
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
