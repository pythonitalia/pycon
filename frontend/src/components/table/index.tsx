/** @jsxRuntime classic */
/** @jsx jsx */
import React from "react";
import { Box, jsx } from "theme-ui";

type Props = {
  headers: string[];
  mobileHeaders: string[];
  data: any[];
  rowGetter: (item: any) => any[];
};

export const Table: React.FC<Props> = ({
  headers,
  data,
  rowGetter,
  mobileHeaders,
}) => (
  /* @ts-ignore */
  <Box cellSpacing={0} as="table" sx={{ width: "100%", fontSize: 2 }}>
    <tr sx={{ display: ["none", "table-row"] }}>
      {headers.map((header, index) => (
        <Box
          key={index}
          as="th"
          sx={{
            color: "orange",
            textTransform: "uppercase",
            textAlign: "left",
            pb: 3,
          }}
        >
          {header}
        </Box>
      ))}
    </tr>
    {data.map((item, index) => {
      const row = rowGetter(item);

      return (
        <Box
          key={index}
          as="tr"
          sx={{
            display: ["flex", "table-row"],
            flexDirection: "column",
            pb: [3, 0],
            "&:last-child": {
              pb: 0,
            },
          }}
        >
          {row.map((content, index) => (
            <td
              key={content}
              sx={{
                borderTop: [null, "primary"],
                py: [0, 3],
                "&:before": {
                  content: `'${mobileHeaders[index]}:'`,
                  color: "orange",
                  textTransform: "uppercase",
                  textAlign: "left",
                  fontWeight: "bold",
                  mr: 2,
                  display: ["inline-block", "none"],
                },
              }}
            >
              {content}
            </td>
          ))}
        </Box>
      );
    })}
  </Box>
);
