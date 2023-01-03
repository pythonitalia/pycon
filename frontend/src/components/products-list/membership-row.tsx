import {
  MultiplePartsCard,
  CardPart,
  Heading,
  Text,
  CardPartAddRemove,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { compile } from "~/helpers/markdown";
import { useCurrentLanguage } from "~/locale/context";
import { CurrentUserQueryResult, TicketItem } from "~/types";

import { useCart } from "../tickets-page/use-cart";

type Props = {
  me: CurrentUserQueryResult["data"]["me"];
  membership: TicketItem;
};

export const MembershipRow = ({ me, membership }: Props) => {
  const isPythonItaliaMember = me?.isPythonItaliaMember ?? false;
  const {
    state: { selectedProducts },
    addProduct,
    removeProduct,
  } = useCart();
  const added = selectedProducts[membership.id]?.length > 0;
  const language = useCurrentLanguage();
  const moneyFormatter = new Intl.NumberFormat(language, {
    style: "currency",
    currency: "EUR",
  });

  return (
    <MultiplePartsCard
      openByDefault={false}
      clickablePart={membership.description ? "heading" : undefined}
      expandTarget={membership.description ? "content" : undefined}
    >
      <CardPart
        iconBackground="blue"
        title={membership.name}
        icon="star"
        contentAlign="left"
        id="heading"
        openLabel={
          <FormattedMessage id="tickets.productsList.openDescription" />
        }
      />
      {membership.description && (
        <CardPart id="content" contentAlign="left" noBg>
          <Text size={2}>{compile(membership.description).tree}</Text>
        </CardPart>
      )}

      {!isPythonItaliaMember && (
        <CardPartAddRemove
          onAdd={() => addProduct(membership.id)}
          onRemove={() => removeProduct(membership.id)}
          action={added ? "remove" : "add"}
        >
          <Heading size={2}>
            {moneyFormatter.format(Number(membership.defaultPrice))}
          </Heading>
        </CardPartAddRemove>
      )}

      {isPythonItaliaMember && (
        <CardPart contentAlign="left">
          <Text size={2}>
            <FormattedMessage id="order.userAlreadyMember" />
          </Text>
        </CardPart>
      )}
    </MultiplePartsCard>
  );
};
