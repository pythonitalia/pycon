import {
  CardPart,
  CardPartIncrements,
  CardPartTwoSides,
  Heading,
  MultiplePartsCard,
  Spacer,
  Tag,
  TagsCollection,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { TicketItem } from "~/types";

import { useCart } from "../tickets-page/use-cart";

type Props = {
  ticket: TicketItem;
  icon: Parameters<typeof CardPart>[0]["icon"];
  iconBackground: Parameters<typeof CardPart>[0]["iconBackground"];
  openByDefault?: boolean;
  ignoreSoldOut?: boolean;
};

export const TicketRow = ({
  ticket,
  icon,
  iconBackground,
  openByDefault,
  ignoreSoldOut = false,
}: Props) => {
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
  const hasTags = ticket.availableUntil || ticket.quantityLeft;

  return (
    <MultiplePartsCard
      openByDefault={openByDefault}
      clickablePart={ticket.description ? "heading" : undefined}
      expandTarget={ticket.description ? "content" : undefined}
    >
      <CardPart
        iconBackground={iconBackground}
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
          {hasTags && <Spacer size="xs" />}

          <Text size={2}>{compile(ticket.description).tree}</Text>
        </CardPart>
      )}

      {!ticket.variations.length && (
        <AddRemoveRow
          price={Number(ticket.defaultPrice)}
          onIncrement={() => addProduct(ticket.id, undefined, ticket.admission)}
          onDecrement={() => removeProduct(ticket.id)}
          soldOut={ignoreSoldOut ? false : ticket.soldOut}
          quantity={selectedProducts[ticket.id]?.length ?? 0}
        />
      )}

      {ticket.variations.length > 1 &&
        ticket.variations.map((variation) => (
          <AddRemoveRow
            key={variation.id}
            price={Number(variation.defaultPrice)}
            label={variation.value}
            soldOut={variation.soldOut}
            onIncrement={() => addProduct(ticket.id, variation.id)}
            onDecrement={() => removeProduct(ticket.id, variation.id)}
            quantity={
              selectedProducts[ticket.id]?.filter(
                (p) => p.variation === variation.id,
              ).length ?? 0
            }
          />
        ))}
    </MultiplePartsCard>
  );
};

export const AddRemoveRow = ({
  onIncrement,
  onDecrement,
  price,
  quantity,
  label,
  soldOut,
}: {
  onIncrement: () => void;
  onDecrement: () => void;
  price: number;
  quantity: number;
  label?: string;
  soldOut: boolean;
}) => {
  const moneyFormatter = useMoneyFormatter();

  const leftSide = (
    <div className="h-full flex flex-col-reverse md:flex-row items-start justify-center md:justify-start md:items-end md:gap-6">
      <Heading size={2} className="flex items-end gap-2">
        {moneyFormatter.format(price * (quantity || 1))}

        {quantity > 0 && (
          <Text size="label4" weight="strong" className="md:hidden">
            {moneyFormatter.format(price)} x{quantity}
          </Text>
        )}
      </Heading>
      {label && (
        <Text size="label3" color="grey-500" weight="strong" uppercase>
          {label}
        </Text>
      )}
      {quantity > 0 && (
        <Text
          size="label3"
          weight="strong"
          className="-order-[1] md:order-3 hidden md:block"
        >
          {moneyFormatter.format(price)} x{quantity}
        </Text>
      )}
    </div>
  );

  if (soldOut) {
    return (
      <CardPartTwoSides
        rightSide={
          <div className="w-full flex md:items-center md:justify-center">
            <Tag color="red">
              <FormattedMessage id="tickets.productsList.soldOut" />
            </Tag>
          </div>
        }
      >
        {leftSide}
      </CardPartTwoSides>
    );
  }

  return (
    <CardPartIncrements
      onIncrement={onIncrement}
      onDecrement={onDecrement}
      value={quantity}
    >
      {leftSide}
    </CardPartIncrements>
  );
};
