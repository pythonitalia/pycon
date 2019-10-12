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

  dd {
    font-size: 18px;
    font-weight: 700;
    color: ${theme.palette.primary};
    border-radius: 4rem;
    padding: 0.5rem 0;
  }
`;

type Props = {
  deadlines: {
    name: string;
    description: string;
    start: string;
    end: string;
  }[];
};

const formatDeadlineDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("default", {
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return formatter.format(d);
};

export const Deadlines = (props: Props) => (
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

        {props.deadlines.map((deadline, index) => (
          <Column
            key={index}
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 4,
              desktop: 4,
            }}
          >
            <div className="element">
              <h2 className="title">{deadline.name}</h2>
              <p className="description">{deadline.description}</p>
              {
                // TODO: show timezone
              }
              <dl>
                <dt>Start:</dt>
                <dd>{formatDeadlineDate(deadline.start)}</dd>
                <dt>End:</dt>
                <dd>{formatDeadlineDate(deadline.end)}</dd>
              </dl>
            </div>
          </Column>
        ))}
      </Row>
    </Container>
  </StyledDeadlines>
);
