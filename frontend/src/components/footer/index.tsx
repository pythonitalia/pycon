import { Box, Column, Columns, Heading, Input, Text } from "fannypack";
import { Link } from "gatsby";
import React, { Component } from "react";
import styled from "styled-components";
import { theme } from "../../config/theme";
import { Button } from "../button";
import { CustomColumns } from "../columns";
import { GOOGLE_MAPS_URL } from "./constants";

const Wrapper = styled.div`
  margin-top: 3rem;
  background-color: ${theme.palette.primary};
  color: ${theme.palette.white};
  position: relative;
  display: block;
  padding-bottom: 0.5rem;
  h3 {
    margin-top: 0;
  }
  .margin-mobile-0-r {
    margin-bottom: 4rem;
  }
  @media only screen and (min-width: 578px) {
    .margin-mobile-0-r,
    .margin-mobile-0-l {
      margin: 0;
      margin-bottom: 4rem;
    }
  }
  @media only screen and (min-width: 992px) {
    .margin-mobile-0-r {
      margin-right: 4rem;
    }
    .margin-mobile-0-l {
      margin-left: 4rem;
      margin-bottom: 0;
    }
  }
`;

const LinksWrapper = styled.div`
  a {
    display: block;
    color: ${theme.palette.white};
    margin-bottom: 0.5rem;
  }
`;

const MapWrapper = styled.div`
  position: relative;
  img {
    width: 100%;
  }
`;

export class Footer extends Component {
  render() {
    return (
      <Wrapper>
        <CustomColumns
          responsivePadding={{
            top: { desktop: 4, mobile: 3 },
            bottom: { desktop: 4, mobile: 3 },
            left: { desktop: 2, mobile: 3 },
            right: { desktop: 2, mobile: 3 },
          }}
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
          responsivePadding={{
            top: { desktop: 4, mobile: 3 },
            bottom: { desktop: 4, mobile: 3 },
            left: { desktop: 2, mobile: 3 },
            right: { desktop: 2, mobile: 3 },
          }}
        >
          <Column spread={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spread={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spread={3}>
            <Box>
              <Heading use="h4">our venues</Heading>
              <LinksWrapper>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
                <Link to="/">Link</Link>
              </LinksWrapper>
            </Box>
          </Column>
          <Column spread={3}>
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
