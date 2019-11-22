/** @jsx jsx */
import { Box, Flex, Heading, Text } from "@theme-ui/components";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { PyConEvent } from "./types";

const formatEventDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("default", {
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return formatter.format(d);
};

export const EventCard = (props: PyConEvent) => (
  <Box
    sx={{
      position: "relative",
      overflow: "hidden",
      borderLeft: "primary",
      borderRight: "primary",
    }}
  >
    <Box sx={{ paddingBottom: "100%", display: "inline-block" }} />

    {props.imageFile && (
      <Img
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
        {...props.imageFile.childImageSharp}
      />
    )}

    <Box
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background: "#F17A5D",
        mixBlendMode: "multiply",
      }}
    />

    <Flex
      sx={{
        p: 3,
        flexDirection: "column",
        justifyContent: "flex-end",
        color: "white",
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
      }}
    >
      <Heading variant="caps" sx={{ mb: "auto" }}>
        {props.title}
      </Heading>

      <Text>{props.locationName}</Text>
      <Text>{formatEventDate(props.start)}</Text>
    </Flex>
  </Box>
);
