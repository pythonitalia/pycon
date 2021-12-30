/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import Image from "next/image";

import { Link } from "~/components/link";
import { Keynote, useKeynotesSectionQuery } from "~/types";

import { GridSlider } from "../grid-slider";

const KeynoteSlide = ({ keynoteTitle: title, slug, speakers }: Keynote) => {
  const image = speakers[0].photo;
  const highlightColor = speakers[0].highlightColor;
  return (
    <Link
      path="/keynote/[slug]"
      params={{
        slug,
      }}
    >
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
            alt="Speaker photo"
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
            {speakers.map((speaker) => speaker.name).join(" & ")}
          </Heading>
          <Text>{title}</Text>
        </Flex>
      </Box>
    </Link>
  );
};

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

  return (
    <GridSlider title="Keynoters" items={keynotes} Component={KeynoteSlide} />
  );
};
