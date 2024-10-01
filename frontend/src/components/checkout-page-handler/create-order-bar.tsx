import {
  BasicButton,
  BottomBar,
  Button,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import type { HotelRoom, TicketItem } from "~/types";

import {
  calculateSavedAmount,
  calculateTotalAmount,
} from "../tickets-page/review/prices";
import { useCart } from "../tickets-page/use-cart";

type Props = {
  productsById: Record<number, TicketItem>;
  hotelRoomsById: Record<number, HotelRoom>;
  createOrder: (event: any, method: string) => void;
  isCreatingOrder: boolean;
  creationFailed: boolean;
};

export const CreateOrderBar = ({
  productsById,
  hotelRoomsById,
  createOrder,
  creationFailed,
  isCreatingOrder,
}: Props) => {
  const moneyFormatter = useMoneyFormatter();
  const { state } = useCart();

  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);
  const savedAmount = calculateSavedAmount(state, productsById);

  const checkoutIsDisabled = isCreatingOrder || !state.acceptedPrivacyPolicy;

  return (
    <BottomBar
      action={
        <div>
          <div className="flex flex-col-reverse lg:flex-row">
            <BasicButton
              disabled={checkoutIsDisabled}
              onClick={(e) => {
                createOrder(e, "banktransfer");
              }}
            >
              <FormattedMessage id="tickets.checkout.payWithBankTransfer" />
            </BasicButton>
            <Spacer size="xs" showOnlyOn="mobile" />
            <Spacer size="medium" showOnlyOn="tablet" />
            <Spacer
              size="large"
              showOnlyOn="desktop"
              orientation="horizontal"
            />
            <Button
              variant="secondary"
              disabled={checkoutIsDisabled}
              onClick={(e) => {
                createOrder(e, "stripe");
              }}
              fullWidth="mobile"
            >
              <FormattedMessage id="tickets.checkout.payWithCard" />
            </Button>
          </div>
          <div>
            {creationFailed && (
              <>
                <Spacer size="small" />
                <Text size="label3" color="red">
                  <FormattedMessage
                    id="tickets.checkout.orderCreationFailed"
                    values={{ br: <br /> }}
                  />
                </Text>
              </>
            )}
          </div>
        </div>
      }
    >
      <Heading size="display2">{moneyFormatter.format(totalAmount)}</Heading>
      <Spacer size="small" />
      {savedAmount > 0 && (
        <Text size="label3" color="coral">
          <FormattedMessage
            id="tickets.checkout.savedAmount"
            values={{
              amount: moneyFormatter.format(savedAmount),
            }}
          />
        </Text>
      )}
    </BottomBar>
  );
};
