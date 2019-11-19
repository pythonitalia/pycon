/** @jsx jsx */

import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import Img from "gatsby-image";
import { useState } from "react";
import { jsx } from "theme-ui";

import { KeynotesSectionQuery } from "../../generated/graphql";
import { useSSRResponsiveValue } from "../../helpers/use-ssr-responsive-value";
import { ArrowIcon } from "../icons/arrow";

type KeynoteProps = KeynotesSectionQuery["backend"]["conference"]["keynotes"][0];

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
        backgroundColor: color,
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
  page,
  showArrows,
  increase,
  decrease,
}: {
  page: KeynotesSectionQuery["backend"]["conference"]["keynotes"];
  showArrows: boolean;
  increase: () => void;
  decrease: () => void;
}) => (
  <Grid
    sx={{
      justifyContent: "center",
      gridTemplateColumns: ["1fr", "100px minmax(200px, 1200px) 100px"],
    }}
    gap={0}
  >
    <Flex
      onClick={decrease}
      sx={{
        display: ["none", "flex"],
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {showArrows && <ArrowIcon sx={{ width: 40 }} />}
    </Flex>

    <Grid columns={[1, 3]} gap={0}>
      {page.map((keynote, i) => (
        <Keynote
          color={keynote.highlightColor || "cindarella"}
          key={keynote.id}
          {...keynote}
        />
      ))}
    </Grid>

    <Flex
      onClick={increase}
      sx={{
        display: ["none", "flex"],
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {showArrows && <ArrowIcon sx={{ width: 40 }} direction="right" />}
    </Flex>
  </Grid>
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
            additionalSpeakers {
              fullName
            }
          }
        }
      }
    }
  `);

  const columns = useSSRResponsiveValue([1, 3]);
  const showArrows = keynotes.length > columns;
  const [page, increase, decrease] = useSlider(keynotes, columns);

  return (
    <Box sx={{ borderBottom: "primary", borderTop: "primary" }}>
      <Box sx={{ borderBottom: "primary", py: 4 }}>
        <Heading
          as="h1"
          sx={{
            px: 2,
            display: "flex",
            maxWidth: "container",
            mx: "auto",
          }}
        >
          Keynoters
          <Box
            sx={{
              marginLeft: "auto",
              flex: "0 0 60px",
              display: ["block", "none"],
            }}
          >
            <ArrowIcon
              onClick={decrease}
              sx={{ width: 20, height: 20, mr: 2 }}
            />
            <ArrowIcon
              onClick={increase}
              sx={{ width: 20, height: 20 }}
              direction="right"
            />
          </Box>
        </Heading>
      </Box>

      <KeynotesList
        page={page}
        showArrows={showArrows}
        increase={increase}
        decrease={decrease}
      />
    </Box>
  );
};
