/** @jsx jsx */

import { Box, Flex, Heading, Text } from "@theme-ui/components";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { KeynotesSectionQuery } from "../../generated/graphql";

type KeynoteProps = KeynotesSectionQuery["backend"]["conference"]["keynotes"][0];

export const KeynoteCard = ({
  title,
  additionalSpeakers,
  imageFile,
  color,
  ...props
}: KeynoteProps & { color: string }) => (
  <Box
    sx={{
      position: "relative",
      borderLeft: "primary",
      borderRight: "primary",
    }}
    {...props}
  >
    <Box sx={{ display: "inline-block", pt: "100%" }} />
    {imageFile && (
      <Img
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
        {...imageFile.childImageSharp}
      />
    )}
    <Box
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background: color,
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
      <Heading variant="caps" as="h3">
        {additionalSpeakers.map(speaker => speaker.fullName).join(" & ")}
      </Heading>
      <Text>{title}</Text>
    </Flex>
  </Box>
);
