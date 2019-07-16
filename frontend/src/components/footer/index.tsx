import { Box, Column, Columns, Input } from "fannypack";
import React from "react";
import styled from "styled-components";
import { theme } from "../../config/theme";
import { Button } from "../button";

const Wrapper = styled.div`
  background-color: ${theme.palette.primary};
  color: ${theme.palette.white};
  h3 {
    margin-top: 0;
  }
`;

export const Footer = () => {
  return (
    <Wrapper>
      <Columns padding="major-4">
        <Column spread={12}>
          <Columns>
            <Column spread={6}>
              <Box marginRight={"major-2"}>
                <h3>keep up to date</h3>
                <p>
                  Stay in the loop, sign up for email updates about events, news
                  and offers.
                </p>
                <div>
                  <form action="">
                    <Input
                      placeholder="Email"
                      marginTop="major-1"
                      marginBottom="major-2"
                      type="email"
                    />
                    <Button palette={"white"}>Sign up</Button>
                  </form>
                </div>
              </Box>
            </Column>
            <Column spread={6}>
              <Box marginLeft={"major-2"}>
                <h3>Donations</h3>
                <p>
                  Stay in the loop, sign up for email updates about events, news
                  and offers.
                </p>
                <Button palette={"white"}>Donate now</Button>
              </Box>
            </Column>
          </Columns>
        </Column>
        <Column spread={12}>lol</Column>
        <Column spread={12}>lol</Column>
      </Columns>
    </Wrapper>
  );
};
