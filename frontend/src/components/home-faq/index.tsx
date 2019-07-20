import React from "react";

import { Heading, Text } from "fannypack";
import { Column, Row } from "grigliata";
import styled from "styled-components";
import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div`
  margin-top: 2rem;
`;

export const Faq = () => {
  const PADDING_RIGHT = {
    mobile: 0,
    tabletPortrait: 3,
    tabletLandscape: 3,
    desktop: 3,
  };

  return (
    <Wrapper>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          colWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <SectionTitle>FAQ</SectionTitle>
        </Column>
      </Row>
      <Row
        marginTop={{
          desktop: -4,
          tabletLandscape: -3,
          tabletPortrait: 0,
          mobile: 0,
        }}
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          paddingRight={PADDING_RIGHT}
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">How can I contribute?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </Column>
        <Column
          paddingRight={PADDING_RIGHT}
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">Where is the venue?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </Column>
        <Column
          paddingRight={PADDING_RIGHT}
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">When will the event take place?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </Column>
        <Column
          paddingRight={PADDING_RIGHT}
          colWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 6,
            desktop: 6,
          }}
        >
          <Heading use="h3">Where is the venue?</Heading>
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quibusdam
            numquam inventore laboriosam quisquam nobis maxime reiciendis a
            consectetur nisi temporibus. Quo autem magni eaque suscipit
            obcaecati ad excepturi iste ab!
          </Text>
        </Column>
      </Row>
    </Wrapper>
  );
};
