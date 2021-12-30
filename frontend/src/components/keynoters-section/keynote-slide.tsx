/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import Image from "next/image";

import { Link } from "~/components/link";
import { KeynoteSpeaker } from "~/types";

type KeynoteSlide = {
  keynoteTitle: string;
  slug: string | null;
  speakers: KeynoteSpeaker[];
  standalone?: boolean;
}

export const KeynoteSlide = ({
  keynoteTitle: title,
  slug,
  speakers,
  standalone = false,
}: KeynoteSlide) => {
  const image = speakers[0].photo;
  const highlightColor = speakers[0].highlightColor;
  const Wrapper = slug ? Link : Box;
  return (
    <Wrapper
      path="/keynotes/[slug]"
      params={{
        slug,
      }}
      sx={
        !standalone
          ? {
              "&:last-child": {
                borderRight: "primary",
              },
            }
          : undefined
      }
    >
      <Box
        sx={{
          position: "relative",
          borderLeft: "primary",
          paddingBottom: '100%',
          ...(standalone
            ? {
                borderRight: "primary",
                borderTop: "primary",
                borderBottom: "primary",
              }
            : {
              height: '100%',
            }),
        }}
      >
        {image && (
          <Image
            sx={{
              position: "absolute",
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
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
          {title && <Text>{title}</Text>}
        </Flex>
      </Box>
    </Wrapper>
  );
};
