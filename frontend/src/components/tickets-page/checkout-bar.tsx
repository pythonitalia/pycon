import { BottomBar, Button, Heading } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
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

  const productsById = Object.fromEntries(
    products!.map((product) => [product.id, product]),
  );

  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map((room) => [room.id, room]),
  );

  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);
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
