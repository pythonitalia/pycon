/** @jsx jsx */

import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import Img from "gatsby-image";
import { useState } from "react";
import { jsx } from "theme-ui";

import { KeynotesSectionQuery } from "../../generated/graphql";
import { ArrowIcon } from "../icons/arrow";

type KeynoteProps = KeynotesSectionQuery["backend"]["conference"]["keynotes"][0];

const colors = ["#79CDE0", "#34B4A1", "#F17A5D"];

const Keynote = ({
  title,
  additionalSpeakers,
  imageFile,
  color,
}: KeynoteProps & { color: string }) => (
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

const useSlider = <T extends any>(
  objects: T[],
  perPage: number,
): [T[], () => void, () => void] => {
  const [index, setIndex] = useState(0);

  // TODO: fix the increase to find the last page
  const increase = () =>
    setIndex(Math.min(index + perPage, objects.length - 1));
  const decrease = () => setIndex(Math.max(index - perPage, 0));

  return [objects.slice(index, index + perPage), increase, decrease];
};

const KeynotesList = ({
  keynotes,
}: {
  keynotes: KeynotesSectionQuery["backend"]["conference"]["keynotes"];
}) => {
  const showArrows = keynotes.length > 3;
  const [page, increase, decrease] = useSlider(keynotes, 3);

  return (
    <Grid
      sx={{
        justifyContent: "center",
        gridTemplateColumns: "100px minmax(200px, 1200px) 100px",
      }}
      gap={0}
    >
      <Flex
        onClick={decrease}
        sx={{
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {showArrows && <ArrowIcon />}
      </Flex>

      <Grid columns={3} gap={0}>
        {page.map((keynote, i) => (
          <Keynote
            color={colors[i % colors.length]}
            key={keynote.id}
            {...keynote}
          />
        ))}
      </Grid>

      <Flex
        onClick={increase}
        sx={{
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {showArrows && <ArrowIcon direction="right" />}
      </Flex>
    </Grid>
  );
};

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

      <KeynotesList keynotes={keynotes} />
    </Box>
  );
};
