import React from "react";

import { Heading, Input, Text } from "fannypack";
import { Link } from "gatsby";
import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { Button } from "../button";
import { Column } from "../column";
import { Row } from "../row";
import { GOOGLE_MAPS_URL } from "./constants";
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

  return (
    <Wrapper>
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
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">keep up to date</Heading>
          <Text>
            Stay in the loop, sign up for email updates about events, news and
            offers.
          </Text>
          <div>
            <form action="">
              <Row
                marginLeft={{
                  mobile: -0.5,
                  tabletPortrait: -0.5,
                  tabletLandscape: -0.5,
                  desktop: -0.5,
                }}
                marginRight={{
                  mobile: -0.5,
                  tabletPortrait: -0.5,
                  tabletLandscape: -0.5,
                  desktop: -0.5,
                }}
                paddingRight={STANDARD_ROW_PADDING}
              >
                <Column
                  colWidth={{
                    mobile: 12,
                    tabletPortrait: 9,
                    tabletLandscape: 9,
                    desktop: 9,
                  }}
                >
                  <Input placeholder="Email" type="email" />
                </Column>
                <Column
                  colWidth={{
                    mobile: 12,
                    tabletPortrait: 3,
                    tabletLandscape: 3,
                    desktop: 3,
                  }}
                >
                  <Button margin="0" palette={"white"}>
                    Sign up
                  </Button>
                </Column>
              </Row>
            </form>
          </div>
        </Column>
        <Column
          paddingRight={{
            mobile: 0,
            tabletPortrait: 3,
            tabletLandscape: 3,
            desktop: 3,
          }}
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">donations</Heading>
          <div>
            <Text>
              Stay in the loop, sign up for email updates about events, news and
              offers.
            </Text>
          </div>

          <Button marginTop="major-2" palette={"white"}>
            Donate now
          </Button>
        </Column>
      </Row>

      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
        marginTop={MARGIN_TOP_ROW}
      >
        <Column
          colWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <MapWrapper>
            <a href="https://www.google.com/maps/place/hotel+mediterraneo+firenze/">
              <img
                src={GOOGLE_MAPS_URL}
                alt="Google Map of hotel Mediterraneo Firenze"
              />
            </a>
          </MapWrapper>
        </Column>
      </Row>

      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
        marginTop={MARGIN_TOP_ROW}
        marginBottom={MARGIN_TOP_ROW}
      >
        {[1, 2, 3, 4].map((o, i) => {
          return (
            <Column
              key={i}
              colWidth={{
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
          );
        })}
      </Row>
    </Wrapper>
  );
};
