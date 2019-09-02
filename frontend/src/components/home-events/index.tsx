import { Column, Row } from "grigliata";
import React, { useEffect } from "react";
import styled from "styled-components";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { theme } from "../../config/theme";
import { MaxWidthWrapper } from "../max-width-wrapper";
import { SectionTitle } from "../section-title";

const Wrapper = styled.div`
    @media (min-width: 1024px) {
      margin-top: 2rem;
    }
    p {
      margin-top: 0;
    }
  `,
  EventsContainer = styled.div`
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

    .event_card {
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
      .event_card_content__title {
        color: ${theme.palette.white};
        margin: 0;
      }
      .event_card_content__subtitle {
        color: ${theme.palette.white};
        margin: 0;
      }
    }
  `,
  EventCard = styled.div`
    background: linear-gradient(
      29.43deg,
      #0c67ff 0%,
      rgba(12, 103, 255, 0.0001) 125.98%
    );
    box-shadow: 0px 0px 1px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    height: 200px;
    width: 300px;
    position: relative;
  `,
  EventCardContent = () => (
    <div className="event_card_content">
      <p className="event_card_content__title">h. 21:00 Pub James Joyce</p>
      <p className="event_card_content__subtitle">PyBirra</p>
    </div>
  );

export const Events = () => {
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
            <p>
              Lorem ipsum, dolor sit amet consectetur adipisicing elit maxime
              reiciendis a consectetur nisi temporibus!
            </p>
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
          {[1, 2, 3, 4, 5, 6, 7].map((o, i) => (
            <EventCard key={i} className="event_card">
              <EventCardContent />
            </EventCard>
          ))}
        </EventsContainer>
      </Row>
    </Wrapper>
  );
};
