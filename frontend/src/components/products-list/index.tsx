import { Heading, Section, Spacer } from "@python-italia/pycon-styleguide";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import {
  CurrentUserQueryResult,
  HotelRoom,
  TicketItem,
  TicketsQuery,
  TicketType,
} from "~/types";

import { HotelRow } from "./hotel-row";
import { MembershipRow } from "./membership-row";
import { SocialEventRow } from "./socialevent-row";
import { TicketRow } from "./ticket-row";

type Props = {
  products: TicketItem[];
  hotelRooms: HotelRoom[];
  conference: TicketsQuery["conference"];
  me: CurrentUserQueryResult["data"]["me"];
  business: boolean;
};

export const ProductsList = ({
  products,
  hotelRooms,
  conference,
  business,
  me,
}: Props) => {
  const ticketType = business ? TicketType.Business : TicketType.Standard;
  const tickets = products.filter(
    (product) => product.admission && product.type === ticketType,
  );
  const membership = products.filter(
    (product) => product.type === TicketType.Association,
  )[0];
  const tshirt = products.filter((product) => product.category === "Gadget")[0];
  const sortedHotelRooms = [...hotelRooms].sort(
    (a, b) => Number(a.price) - Number(b.price),
  );
  const socialEvents = products.filter(
    (product) => product.type === TicketType.SocialEvent,
  );

  return (
    <div>
      <Section>
        {tickets.map((ticket, index) => (
          <Fragment key={ticket.id}>
            <TicketRow
              openByDefault={index === 0}
              icon="tickets"
              iconBackground="pink"
              ticket={ticket}
            />
            <Spacer size="xs" />
          </Fragment>
        ))}

        <GroupHeading>
          <FormattedMessage id="tickets.productsList.tshirtTitle" />
        </GroupHeading>

        {tshirt && (
          <>
            <TicketRow
              key={tshirt.id}
              icon="tshirt"
              iconBackground="yellow"
              ticket={tshirt}
            />
            <Spacer size="xs" />
          </>
        )}

        <GroupHeading>
          <FormattedMessage id="tickets.productsList.socialEventsTitle" />
        </GroupHeading>

        {socialEvents.map((socialEvent, index) => (
          <Fragment key={socialEvent.id}>
            <SocialEventRow ticket={socialEvent} openByDefault={index === 0} />
            <Spacer size="xs" />
          </Fragment>
        ))}

        <GroupHeading>
          <FormattedMessage id="tickets.productsList.hotelRoomsTitle" />
        </GroupHeading>

        {sortedHotelRooms.map((hotelRoom, index) => (
          <Fragment key={hotelRoom.id}>
            <HotelRow openByDefault={index === 0} hotelRoom={hotelRoom} />
            <Spacer size="xs" />
          </Fragment>
        ))}

        <GroupHeading>
          <FormattedMessage id="tickets.productsList.joinPythonItalia" />
        </GroupHeading>

        <MembershipRow membership={membership} me={me} />
      </Section>
    </div>
  );
};

type GroupHeadingProps = {
  children: React.ReactNode;
};
const GroupHeading = ({ children }: GroupHeadingProps) => {
  return (
    <>
      <Spacer size="xl" />
      <Heading size={2}>{children}</Heading>
      <Spacer size="medium" />
    </>
  );
};
