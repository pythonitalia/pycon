import * as React from "react";
import styled from "styled-components";

import { BackgroundImage } from "./background-image";
import { PyConEvent } from "./types";

const formatEventDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("default", {
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return formatter.format(d);
};

const EventCardContent = ({ event }: { event: PyConEvent }) => (
  <>
    {event.imageFile && (
      <BackgroundImage {...event.imageFile.childImageSharp} alt="" />
    )}
    <div className="event_card_content">
      {event.locationName && (
        <p className="event_card_content__location">{event.locationName}</p>
      )}
      <p className="event_card_content__title">{event.title}</p>
      <p className="event_card_content__date">{formatEventDate(event.start)}</p>
    </div>
  </>
);

type EventCardProps = {
  event: PyConEvent;
};

const BaseCard = ({ event, ...props }: EventCardProps) => (
  <div {...props}>
    <EventCardContent event={event} />
  </div>
);

export const EventCard = styled(BaseCard)`
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
  overflow: hidden;
`;
