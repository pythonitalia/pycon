import { BottomBar, Button, Heading } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import type { HotelRoom, TicketItem } from "~/types";

import { calculateTotalAmount } from "./review/prices";
import { useCart } from "./use-cart";

type Props = {
  products: TicketItem[];
  onCheckout: () => void;
};

export const CheckoutBar = ({ products, onCheckout }: Props) => {
  const { state } = useCart();

  const productsById = Object.fromEntries(
    products!.map((product) => [product.id, product]),
  );

  const totalAmount = calculateTotalAmount(state, productsById);
  const moneyFormatter = useMoneyFormatter();

  if (totalAmount === 0) {
    return null;
  }

  return (
    <BottomBar
      action={
        <Button onClick={onCheckout} variant="secondary">
          <FormattedMessage id="tickets.checkoutBar.cta" />
        </Button>
      }
    >
      <Heading size="display2">{moneyFormatter.format(totalAmount)}</Heading>
    </BottomBar>
  );
};
