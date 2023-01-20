/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, Flex, Heading, jsx, Text } from "theme-ui";

import { Link } from "~/components/link";

type Props = {
  title: string;
  slug: string | null;
  speakers: any[];
  standalone?: boolean;
};

export const KeynoteSlide = ({
  title,
  slug,
  speakers,
  standalone = false,
}: Props) => {
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
          paddingBottom: "100%",
          ...(standalone
            ? {
                borderRight: "primary",
                borderTop: "primary",
                borderBottom: "primary",
              }
            : {
                height: "100%",
              }),
        }}
      >
        {image && (
          <img
            sx={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              filter: "grayscale(1)",
              objectFit: "cover",
            }}
            loading="lazy"
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
            {speakers.map((speaker) => speaker.fullName).join(" & ")}
          </Heading>
          {title && <Text>{title}</Text>}
        </Flex>
      </Box>
    </Wrapper>
  );
};
