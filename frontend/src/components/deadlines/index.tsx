import { Column, Container, Row } from "grigliata";
import React from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { theme } from "../../config/theme";
import { SectionTitle } from "../section-title";

export const StyledDeadlines = styled.div`
  padding: 4rem 0 0 0;
  .element {
  }
  .section__subtitle {
    margin-top: 0;
  }
  .description {
    @media (min-width: 768px) {
      min-height: 6rem;
    }
  }
  .title {
    @media (min-width: 768px) {
      min-height: 6rem;
    }
  }
  .date {
    font-size: 18px;
    font-weight: 700;
    color: ${theme.palette.primary};
    border-radius: 4rem;
    padding: 0.5rem 0;
  }
`;

export const Deadlines = (props: {}) => (
  <StyledDeadlines>
    <Row paddingLeft={STANDARD_ROW_PADDING} paddingRight={STANDARD_ROW_PADDING}>
      <Column
        columnWidth={{
          mobile: 12,
          tabletPortrait: 12,
          tabletLandscape: 12,
          desktop: 12,
        }}
      >
        <SectionTitle>Deadlines</SectionTitle>
      </Column>
    </Row>
    <Container>
      <Row
        paddingLeft={STANDARD_ROW_PADDING}
        paddingRight={STANDARD_ROW_PADDING}
      >
        <Column
          marginTop={{
            desktop: -4,
            tabletLandscape: -3,
            tabletPortrait: 0,
            mobile: 0,
          }}
          columnWidth={{
            mobile: 12,
            tabletPortrait: 12,
            tabletLandscape: 12,
            desktop: 12,
          }}
        >
          <p className="section__subtitle">
            Here are the next deadlines that are soon arriving
          </p>
        </Column>
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 4,
            desktop: 4,
          }}
        >
          <div className="element">
            <h2 className="title">
              Call for proposal <i>opening</i>
            </h2>
            <p className="description">
              Call for proposals is the place where everyone can submit their
              talks
            </p>
            <p className="date">1st November</p>
          </div>
        </Column>
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 4,
            desktop: 4,
          }}
        >
          <div className="element">
            <h2 className="title">
              Call for proposal <i>closure</i>
            </h2>
            <p className="description">
              It's the last day, game over. Everything it's up to the community
            </p>
            <p className="date">2rd November</p>
          </div>
        </Column>
        <Column
          columnWidth={{
            mobile: 12,
            tabletPortrait: 6,
            tabletLandscape: 4,
            desktop: 4,
          }}
        >
          <div className="element">
            <h2 className="title">Tickets Sale</h2>
            <p className="description">
              Here we are, you can buy the conference tickets
            </p>
            <p className="date">1st November</p>
          </div>
        </Column>
      </Row>
    </Container>
  </StyledDeadlines>
);
