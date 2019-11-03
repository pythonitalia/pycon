import { Heading, Text } from "fannypack";
import { graphql, Link, useStaticQuery } from "gatsby";
import { Column, Row } from "grigliata";
import React from "react";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { FooterQuery } from "../../generated/graphql";
import { Button } from "../button";
import { MaxWidthWrapper } from "../max-width-wrapper";
import { NewsletterSection } from "../newsletter";
import { LinksWrapper } from "./links-wrapper";
import { MapWrapper } from "./map-wrapper";
import { Wrapper } from "./wrapper";

export const Footer = () => {
  const MARGIN_TOP_ROW = {
    mobile: 1,
    tabletPortrait: 5,
    tabletLandscape: 5,
    desktop: 5,
  };

  const {
    backend: {
      conference: { map },
    },
  } = useStaticQuery<FooterQuery>(graphql`
    query Footer {
      backend {
        conference {
          map {
            image(width: 1280, height: 400, zoom: 15)
            link
          }
        }
      }
    }
  `);

  return (
    <Wrapper>
      <MaxWidthWrapper>
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
          paddingTop={MARGIN_TOP_ROW}
        >
          <Column
            paddingRight={{
              mobile: 0,
              tabletPortrait: 3,
              tabletLandscape: 3,
              desktop: 3,
            }}
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
            <NewsletterSection />
          </Column>
          <Column
            paddingRight={{
              mobile: 0,
              tabletPortrait: 3,
              tabletLandscape: 3,
              desktop: 3,
            }}
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
            <Heading use="h3">donations</Heading>
            <div>
              <Text>
                Stay in the loop, sign up for email updates about events, news
                and offers.
              </Text>
            </div>

            <Button marginTop="major-2" palette={"white"}>
              Donate now
            </Button>
          </Column>
        </Row>
      </MaxWidthWrapper>

      {map && (
        <Row marginTop={MARGIN_TOP_ROW}>
          <MapWrapper style={{ width: "100%" }}>
            <a href={map.link || ""} target="_blank" rel="noopener">
              <img src={map.image} />
            </a>
          </MapWrapper>
        </Row>
      )}

      <MaxWidthWrapper>
        <Row
          paddingLeft={STANDARD_ROW_PADDING}
          paddingRight={STANDARD_ROW_PADDING}
          marginTop={MARGIN_TOP_ROW}
          marginBottom={MARGIN_TOP_ROW}
        >
          {[1, 2, 3, 4].map((o, i) => (
            <Column
              key={i}
              columnWidth={{
                mobile: 12,
                tabletPortrait: 6,
                tabletLandscape: 3,
                desktop: 3,
              }}
            >
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Column>
          ))}
        </Row>
      </MaxWidthWrapper>
    </Wrapper>
  );
};
