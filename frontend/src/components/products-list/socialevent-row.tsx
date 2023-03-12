import {
  Text,
  Heading,
  MultiplePartsCard,
  CardPart,
  Tag,
  TagsCollection,
} from "@python-italia/pycon-styleguide";
import { Icon } from "@python-italia/pycon-styleguide/dist/icons/types";
import { FormattedMessage } from "react-intl";

import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { TicketItem } from "~/types";

import { useCart } from "../tickets-page/use-cart";
import { AddRemoveRow } from "./ticket-row";

type Props = {
  ticket: TicketItem;
  openByDefault?: boolean;
};

export const SocialEventRow = ({ ticket, openByDefault }: Props) => {
  const {
    state: { selectedProducts },
    addProduct,
    removeProduct,
  } = useCart();
  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
  const icon = getIconForTicket(ticket);

  return (
    <MultiplePartsCard
      openByDefault={openByDefault}
      clickablePart={ticket.description ? "heading" : undefined}
      expandTarget={ticket.description ? "content" : undefined}
    >
      <CardPart
        iconBackground="coral"
        icon={icon}
        contentAlign="left"
        id="heading"
        openLabel={
          <FormattedMessage id="tickets.productsList.openDescription" />
        }
      >
        <Heading size={2}>{ticket.name}</Heading>
      </CardPart>
      {ticket.description && (
        <CardPart contentAlign="left" background="milk" id="content">
          <TagsCollection>
            {ticket.availableUntil && (
              <Tag color="success">
                <FormattedMessage
                  id="order.availableUntil"
                  values={{
                    date: dateFormatter.format(new Date(ticket.availableUntil)),
                  }}
                />
              </Tag>
            )}
            {ticket.quantityLeft > 0 ? (
              <Tag color="yellow">
                <FormattedMessage
                  id="order.ticketsLeft"
                  values={{
                    count: ticket.quantityLeft,
                  }}
                />
              </Tag>
            ) : null}
          </TagsCollection>

          <Text size={2}>{compile(ticket.description).tree}</Text>
        </CardPart>
      )}
      <AddRemoveRow
        price={Number(ticket.defaultPrice)}
        onIncrement={() => addProduct(ticket.id)}
        onDecrement={() => removeProduct(ticket.id)}
        soldOut={ticket.soldOut}
        quantity={selectedProducts[ticket.id]?.length ?? 0}
      />
    </MultiplePartsCard>
  );
};

const getIconForTicket = (ticket: TicketItem): Icon => {
  switch (ticket.name) {
    case "PyDrinks":
      return "drink";
    case "PyDinner":
      return "forks";
    default:
      return "star";
  }
};
