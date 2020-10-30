/** @jsx jsx */

import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/get-initial-locale";

import { PyConEvent } from "./types";

const formatEventDate = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return formatter.format(d);
};

export const EventCard = (props: PyConEvent) => {
  const language = useCurrentLanguage();
  return (
    <Box
      sx={{
        position: "relative",
        overflow: "hidden",
        borderLeft: "primary",
        borderRight: "primary",
      }}
    >
      <Box sx={{ paddingBottom: "100%", display: "inline-block" }} />

      {props.image && <img src={props.image} />}

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
        <Text>{formatEventDate(props.start, language)}</Text>
      </Flex>
    </Box>
  );
};
