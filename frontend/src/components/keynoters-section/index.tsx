/** @jsx jsx */

import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { KeynotesSectionQuery } from "../../generated/graphql";

type KeynoteProps = KeynotesSectionQuery["backend"]["conference"]["keynotes"][0];

const Keynote = ({ title, additionalSpeakers, imageFile }: KeynoteProps) => (
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
        background: "#79CDE0",
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
            image
            imageFile {
              childImageSharp {
                fixed(grayscale: true, width: 600, height: 600) {
                  ...GatsbyImageSharpFixed
                }
              }
            }
            additionalSpeakers {
              fullName
            }
          }
        }
      }
    }
  `);

  return (
    <Box sx={{ borderBottom: "primary", borderTop: "primary" }}>
      <Box sx={{ borderBottom: "primary", py: 4 }}>
        <Heading
          as="h1"
          sx={{
            px: 2,
            maxWidth: "container",
            mx: "auto",
          }}
        >
          Keynote speakers
        </Heading>
      </Box>

      <Grid
        columns={[1, 3]}
        gap={0}
        sx={{
          maxWidth: "container",
          mx: "auto",
        }}
      >
        {keynotes.map(keynote => (
          <Keynote {...keynote} key={keynote.id} />
        ))}
      </Grid>
    </Box>
  );
};
