/** @jsxRuntime classic */
/** @jsx jsx */
import Image from "next/image";
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import { useKeynotesSectionQuery } from "~/types";

import { GridSlider } from "../grid-slider";

type KeynoteProps = {
  title: string;
  speakers: { fullName: string }[];
  image?: string | null;
  highlightColor?: string | null;
};

const Keynote = ({ title, speakers, image, highlightColor }: KeynoteProps) => (
  <Box
    sx={{
      position: "relative",
      borderLeft: "primary",
      borderRight: "primary",
    }}
  >
    <Box sx={{ display: "inline-block", pt: "100%" }} />
    {image && (
      <Image
        sx={{
          position: "absolute",
          top: 0,
          left: 0,
          filter: "grayscale(1)",
          objectFit: "cover",
        }}
        layout="fill"
        src={image}
      />
    )}
    <Box
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: highlightColor || "cinderella",
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
        {speakers.map((speaker) => speaker.fullName).join(" & ")}
      </Heading>
      <Text>{title}</Text>
    </Flex>
  </Box>
);

export const KeynotersSection = () => {
  const { data } = useKeynotesSectionQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });

  if (!data) {
    return null;
  }

  const {
    conference: { keynotes },
  } = data;

  return <GridSlider title="Keynoters" items={keynotes} Component={Keynote} />;
};
