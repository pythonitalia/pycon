import React, { Component } from "react";

import { Box, Column, Columns, Heading, Input, Text } from "fannypack";
import { Link } from "gatsby";
import { STANDARD_CUSTOM_COLUMNS_PADDING } from "../../config/spacing";
import { Button } from "../button";
import { CustomColumns } from "../columns";
import { GOOGLE_MAPS_URL } from "./constants";
import { LinksWrapper } from "./links-wrapper";
import { MapWrapper } from "./map-wrapper";
import { Wrapper } from "./wrapper";

export class Footer extends Component {
  render() {
    return (
      <Wrapper>
        <CustomColumns
          paddingTop={{ desktop: 4, tablet: 4, mobile: 3 }}
          paddingBottom={{ desktop: 4, tablet: 4, mobile: 3 }}
          paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
          paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
        >
          <Column spread={6} spreadMobile={12}>
            <Box className="margin-mobile-0-r">
              <Heading use="h3">keep up to date</Heading>
              <Text>
                Stay in the loop, sign up for email updates about events, news
                and offers.
              </Text>
              <div>
                <form action="">
                  <Columns marginTop="major-3">
                    <Column spread={9}>
                      <Input placeholder="Email" type="email" />
                    </Column>
                    <Column spread={3}>
                      <Button margin="0" palette={"white"}>
                        Sign up
                      </Button>
                    </Column>
                  </Columns>
                </form>
              </div>
            </Box>
          </Column>
          <Column spread={6} spreadMobile={12}>
            <Box className="margin-mobile-0-l">
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
            </Box>
          </Column>
        </CustomColumns>

        <Columns>
          <Column spread={12}>
            <Box>
              <MapWrapper>
                <a href="https://www.google.com/maps/place/hotel+mediterraneo+firenze/">
                  <img
                    src={GOOGLE_MAPS_URL}
                    alt="Google Map of hotel Mediterraneo Firenze"
                  />
                </a>
              </MapWrapper>
            </Box>
          </Column>
        </Columns>

        <CustomColumns
          paddingTop={{ desktop: 4, tablet: 4, mobile: 3 }}
          paddingBottom={{ desktop: 4, tablet: 4, mobile: 3 }}
          paddingLeft={{ desktop: 2, tablet: 2, mobile: 3 }}
          paddingRight={{ desktop: 2, tablet: 2, mobile: 3 }}
        >
          <Column spreadMobile={12} spread={3} spreadDesktop={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spreadMobile={12} spread={3} spreadDesktop={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spreadMobile={12} spread={3} spreadDesktop={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spreadMobile={12} spread={3} spreadDesktop={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
        </CustomColumns>
      </Wrapper>
    );
  }
}
