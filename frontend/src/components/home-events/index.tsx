import React from "react";

import { Heading, Text } from "fannypack";
import styled from "styled-components";
import { STANDARD_CUSTOM_COLUMNS_PADDING } from "../../config/spacing";
import { CustomColumn } from "../column";
import { CustomColumns } from "../columns";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div``;

const EventsContainer = styled.div`
  overflow-x: scroll;
  width: 100%;
  white-space: nowrap;

  .event_card {
    display: inline-block;
    margin-right: 16px;
    &:first-child {
      margin-left: 15rem;
    }
  }
`;

const EventCard = styled.div`
  background: linear-gradient(
    29.43deg,
    #0c67ff 0%,
    rgba(12, 103, 255, 0.0001) 125.98%
  );
  box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  height: 200px;
  width: 300px;
`;

export const Events = () => {
  return (
    <Wrapper>
      <CustomColumns
        paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
        paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
      >
        <CustomColumn>
          <SectionTitle>EVENTS</SectionTitle>
        </CustomColumn>
      </CustomColumns>
      <CustomColumns
        marginTop={{ desktop: -4, tablet: -4, mobile: -1 }}
        paddingLeft={STANDARD_CUSTOM_COLUMNS_PADDING}
        paddingRight={STANDARD_CUSTOM_COLUMNS_PADDING}
      >
        <CustomColumn
          paddingRight={{ desktop: 3, tablet: 2, mobile: 0 }}
          spreadMobile={12}
          spread={6}
          spreadDesktop={12}
        >
          <Text>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit maxime
            reiciendis a consectetur nisi temporibus!
          </Text>
        </CustomColumn>
      </CustomColumns>
      <CustomColumns marginTop={{ desktop: 2, tablet: 2, mobile: 1 }}>
        <EventsContainer>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
          <EventCard className="event_card">asdf</EventCard>
        </EventsContainer>
      </CustomColumns>
    </Wrapper>
  );
};
