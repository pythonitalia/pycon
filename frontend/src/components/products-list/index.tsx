import { Heading, Section, Spacer } from "@python-italia/pycon-styleguide";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import {
  CheckoutCategory,
  CurrentUserQueryResult,
  HotelRoom,
  TicketItem,
  TicketType,
  TicketsQuery,
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
  ignoreSoldOut: boolean;
  visibleCategories: CheckoutCategory[];
  showHeadings: boolean;
};

export const ProductsList = ({
  products,
  hotelRooms,
  conference,
  business,
  me,
  ignoreSoldOut,
  visibleCategories,
  showHeadings,
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
  const guidedTours = products.filter(
    (product) => product.categoryInternalName === "Guided Tours",
  );

  return (
    <Section>
      {visibleCategories.includes(CheckoutCategory.Tickets) &&
        tickets.map((ticket) => (
          <Fragment key={ticket.id}>
            <TicketRow
              openByDefault={true}
              icon="tickets"
              iconBackground="pink"
              ticket={ticket}
              ignoreSoldOut={ignoreSoldOut}
            />
            <Spacer size="small" />
          </Fragment>
        ))}

      {visibleCategories.includes(CheckoutCategory.Gadgets) && tshirt && (
        <>
          {showHeadings && (
            <GroupHeading>
              <FormattedMessage id="tickets.productsList.tshirtTitle" />
            </GroupHeading>
          )}
          <TicketRow
            key={tshirt.id}
            icon="tshirt"
            iconBackground="yellow"
            ticket={tshirt}
          />
          <Spacer size="small" />
        </>
      )}

      {visibleCategories.includes(CheckoutCategory.SocialEvents) &&
        socialEvents.length > 0 && (
          <>
            {showHeadings && (
              <GroupHeading>
                <FormattedMessage id="tickets.productsList.socialEventsTitle" />
              </GroupHeading>
            )}
            {socialEvents.map((socialEvent, index) => (
              <Fragment key={index}>
                <SocialEventRow
                  ticket={socialEvent}
                  openByDefault={index === 0}
                />
                <Spacer size="small" />
              </Fragment>
            ))}
          </>
        )}

      {visibleCategories.includes(CheckoutCategory.Tours) &&
        guidedTours.length > 0 && (
          <>
            {showHeadings && (
              <GroupHeading>
                <FormattedMessage id="tickets.productsList.guidedToursTitle" />
              </GroupHeading>
            )}

            {guidedTours.map((guidedTour) => (
              <Fragment key={guidedTour.id}>
                <TicketRow
                  openByDefault={true}
                  key={guidedTour.id}
                  icon="star"
                  iconBackground="neutral"
                  ticket={guidedTour}
                />
                <Spacer size="small" />
              </Fragment>
            ))}
          </>
        )}

      {visibleCategories.includes(CheckoutCategory.Hotel) &&
        sortedHotelRooms.length > 0 && (
          <>
            {showHeadings && (
              <GroupHeading>
                <FormattedMessage id="tickets.productsList.hotelRoomsTitle" />
              </GroupHeading>
            )}
            {sortedHotelRooms.map((hotelRoom, index) => (
              <Fragment key={hotelRoom.id}>
                <HotelRow openByDefault={index === 0} hotelRoom={hotelRoom} />
                <Spacer size="small" />
              </Fragment>
            ))}
          </>
        )}

      {visibleCategories.includes(CheckoutCategory.Membership) && (
        <>
          {showHeadings && (
            <GroupHeading>
              <FormattedMessage id="tickets.productsList.joinPythonItalia" />
            </GroupHeading>
          )}

          <MembershipRow membership={membership} me={me} />
        </>
      )}
    </Section>
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
