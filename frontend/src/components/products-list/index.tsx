import {
  Heading,
  Link,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import {
  CheckoutCategory,
  type CurrentUserQueryResult,
  type TicketItem,
  TicketType,
  type TicketsQuery,
} from "~/types";

import { MembershipRow } from "./membership-row";
import { SocialEventRow } from "./socialevent-row";
import { TicketRow } from "./ticket-row";

type Props = {
  products: TicketItem[];
  conference: TicketsQuery["conference"];
  me: CurrentUserQueryResult["data"]["me"];
  business: boolean;
  ignoreSoldOut: boolean;
  visibleCategories: CheckoutCategory[];
  showHeadings: boolean;
};

export const ProductsList = ({
  products,
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
  const tshirts = products.filter((product) => product.category === "Gadget");
  const socialEvents = products.filter(
    (product) => product.type === TicketType.SocialEvent,
  );
  const guidedTours = products.filter(
    (product) => product.categoryInternalName === "Guided Tours",
  );

  return (
    <Section>
      {visibleCategories.includes(CheckoutCategory.Tickets) && (
        <>
          <Text size={2}>
            <FormattedMessage
              id="tickets.description"
              values={{
                page: (
                  <Text size="inherit" decoration="underline">
                    <Link href="/hotels" target="_blank">
                      <FormattedMessage id="tickets.description.page" />
                    </Link>
                  </Text>
                ),
              }}
            />
          </Text>

          <Spacer size="small" />

          {tickets.map((ticket) => (
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
        </>
      )}

      {visibleCategories.includes(CheckoutCategory.Gadgets) && tshirts && (
        <>
          {showHeadings && (
            <GroupHeading>
              <FormattedMessage id="tickets.productsList.tshirtTitle" />
            </GroupHeading>
          )}
          {tshirts.map((tshirt) => (
            <Fragment key={tshirt.id}>
              <TicketRow
                key={tshirt.id}
                icon="tshirt"
                iconBackground="yellow"
                ticket={tshirt}
              />
              <Spacer size="small" />
            </Fragment>
          ))}
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
