import { Column, Row } from "grigliata";
import React, { useEffect } from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { theme } from "../../config/theme";
import { MaxWidthWrapper } from "../max-width-wrapper";
import { SectionTitle } from "../section-title";
import { EventCard } from "./event-card";
import { PyConEvent } from "./types";

const Wrapper = styled.div`
  @media (min-width: 1024px) {
    margin-top: 2rem;
  }
  p {
    margin-top: 0;
  }
`;

const EventsContainer = styled.div`
  overflow-x: scroll;
  width: 100%;
  white-space: nowrap;
  &:hover {
    cursor: pointer;
  }
  -ms-overflow-style: none; // IE 10+
  scrollbar-width: none; // Firefox
  &::-webkit-scrollbar {
    display: none; // Safari and Chrome
  }

  ${EventCard} {
    display: inline-block;
    margin-right: 16px;
    padding: 8px;
    color: ${theme.palette.white};
    &:first-child {
      margin-left: 2.5rem;
      @media (min-width: 1024px) {
        margin-left: 15rem;
      }
    }
    .event_card_content {
      position: absolute;
      left: 16px;
      bottom: 16px;
    }

    p {
      margin: 0;
      color: ${theme.palette.white};
    }

    .event_card_content__date {
      font-size: 0.8em;
    }

    .event_card_content__title {
      font-weight: bold;
    }
  }
`;

type EventsProps = { events: PyConEvent[]; text: string };

export const Events = ({ events, text }: EventsProps) => {
  useEffect(() => {
    const slider: HTMLDivElement | null = document.querySelector(".events");
    let isDown = false,
      startX = 0,
      scrollLeft = 0;
    if (slider) {
      slider.addEventListener("mousedown", (e: MouseEvent) => {
        isDown = true;
        slider.classList.add("active");
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
      });
      slider.addEventListener("mouseleave", () => {
        isDown = false;
        slider.classList.remove("active");
      });
      slider.addEventListener("mouseup", () => {
        isDown = false;
        slider.classList.remove("active");
      });
      slider.addEventListener("mousemove", (e: MouseEvent) => {
        if (!isDown) {
          return null;
        }
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft,
          walk = (x - startX) * 1.5;
        slider.scrollLeft = scrollLeft - walk;
      });
    }
    return () => {
      // return null
    };
  });

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
          <SectionTitle>EVENTS</SectionTitle>
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
          <Column
            columnWidth={{
              mobile: 12,
              tabletPortrait: 6,
              tabletLandscape: 6,
              desktop: 6,
            }}
          >
            <p>{text}</p>
          </Column>
        </Row>
      </MaxWidthWrapper>

      <Row
        marginTop={{
          desktop: 2,
          tabletLandscape: 2,
          tabletPortrait: 0,
          mobile: 0,
        }}
      >
        <EventsContainer className="events">
          {events.map((event, i) => (
            <EventCard key={i} event={event} />
          ))}
        </EventsContainer>
      </Row>
    </Wrapper>
  );
};
