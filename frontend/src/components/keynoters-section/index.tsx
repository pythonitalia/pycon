/** @jsx jsx */

import { Box, Flex, Heading, Text } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { KeynotesSectionQuery } from "../../generated/graphql";
import { GridSlider } from "../grid-slider";

type KeynoteProps = KeynotesSectionQuery["backend"]["conference"]["keynotes"][0];

const Keynote = ({
  title,
  speakers,
  imageFile,
  highlightColor,
}: KeynoteProps) => (
  <Box
    sx={{
      position: "relative",
      borderLeft: "primary",
      borderRight: "primary",
    }}
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
        {speakers.map(speaker => speaker.fullName).join(" & ")}
      </Heading>
      <Text>{title}</Text>
    </Flex>
  </Box>
);

export const KeynotersSection = () => {
  const {
    backend: {
      conference: { keynotes },
    },
  } = useStaticQuery<KeynotesSectionQuery>(graphql`
    query KeynotesSection {
      backend {
        conference {
          keynotes {
            id
            title
            highlightColor
            image
            imageFile {
              childImageSharp {
                fixed(grayscale: true, width: 600, height: 600) {
                  ...GatsbyImageSharpFixed
                }
              }
            }
            speakers {
              fullName
            }
          }
        }
      }
    }
  `);

  return <GridSlider title="Keynoters" items={keynotes} Component={Keynote} />;
};
