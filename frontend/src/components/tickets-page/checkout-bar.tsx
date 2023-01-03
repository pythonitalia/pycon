import { Heading, Button, BottomBar } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { HotelRoom, TicketItem } from "~/types";

import { calculateTotalAmount } from "./review/prices";
import { useCart } from "./use-cart";

type Props = {
  products: TicketItem[];
  hotelRooms: HotelRoom[];
  onCheckout: () => void;
};

export const CheckoutBar = ({ products, hotelRooms, onCheckout }: Props) => {
  const { state } = useCart();
  const language = useCurrentLanguage();

  const productsById = Object.fromEntries(
    products!.map((product) => [product.id, product]),
  );

  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map((room) => [room.id, room]),
  );

  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);

  if (totalAmount === 0) {
    return null;
  }

  const moneyFormatter = new Intl.NumberFormat(language, {
    style: "currency",
    currency: "EUR",
  });

  return (
    <BottomBar
      action={
        <Button onClick={onCheckout} role="secondary">
          <FormattedMessage id="tickets.checkoutBar.cta" />
        </Button>
      }
    >
      <Heading size="display2">{moneyFormatter.format(totalAmount)}</Heading>
    </BottomBar>
  );
};
