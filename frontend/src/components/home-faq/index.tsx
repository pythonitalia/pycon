import { Heading, Text } from "fannypack";
import { Column, Row } from "grigliata";
import React from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { MaxWidthWrapper } from "../max-width-wrapper";
import { SectionTitle } from "../section-title";

type FAQ = {
  question: string;
  answer: string;
};

const Wrapper = styled.div`
  margin-top: 2rem;
`;

export const Faqs = ({ faqs }: { faqs: FAQ[] }) => {
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
          columnWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <SectionTitle>FAQ</SectionTitle>
        </Column>
      </Row>
      <MaxWidthWrapper>
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
          {faqs.map((faq, i) => (
            <Column
              key={i}
              paddingRight={PADDING_RIGHT}
              columnWidth={{
                mobile: 12,
                tabletPortrait: 6,
                tabletLandscape: 6,
                desktop: 6,
              }}
            >
              <Heading use="h3">{faq.question}</Heading>
              <Text>{faq.answer}</Text>
            </Column>
          ))}
        </Row>
      </MaxWidthWrapper>
    </Wrapper>
  );
};
