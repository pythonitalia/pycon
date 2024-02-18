import {
  BasicButton,
  BottomBar,
  Button,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { useMachine } from "@xstate/react";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useMoneyFormatter } from "~/helpers/formatters";
import { useCurrentLanguage } from "~/locale/context";
import { HotelRoom, TicketItem, useCreateOrderMutation } from "~/types";

import {
  calculateSavedAmount,
  calculateTotalAmount,
} from "../tickets-page/review/prices";
import { SelectedProducts } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";
import { createOrderMachine } from "./order-machine";

type Props = {
  productsById: Record<number, TicketItem>;
  hotelRoomsById: Record<number, HotelRoom>;
  userEmail: string;
  conferenceTimeZone: string;
};

export const CreateOrderBar = ({
  productsById,
  hotelRoomsById,
  userEmail,
  conferenceTimeZone,
}: Props) => {
  const { state } = useCart();
  const language = useCurrentLanguage();

  const code = process.env.conferenceCode;

  const [createOrder] = useCreateOrderMutation();

  const [createOrderState, createOrderSend] = useMachine(createOrderMachine, {
    services: {
      createOrder: async (context, event) => {
        const method = event.method;
        const orderTickets = Object.values(
          state.selectedProducts as SelectedProducts,
        )
          .flat()
          .map((product) => ({
            ticketId: product.id,
            variation: product.variation,
            attendeeName: product.attendeeName,
            attendeeEmail: product.attendeeEmail,
            voucher: product.voucher?.code ?? undefined,
            answers: Object.entries(product.answers).map(([key, value]) => ({
              questionId: key,
              value,
            })),
          }));

        const hotelRooms = Object.values(state.selectedHotelRooms)
          .flat()
          .map((selectedRoom) => ({
            roomId: selectedRoom.id,
            checkin: selectedRoom.checkin,
            checkout: selectedRoom.checkout,
            bedLayoutId: selectedRoom.beds,
          }));

        const orderResult = await createOrder({
          variables: {
            conference: code,

            input: {
              paymentProvider: method,
              tickets: orderTickets,
              hotelRooms,
              email: userEmail,
              locale: language,
              invoiceInformation: {
                isBusiness: state.invoiceInformation.isBusiness,
                company: state.invoiceInformation.companyName,
                name: state.invoiceInformation.name,
                street: state.invoiceInformation.address,
                zipcode: state.invoiceInformation.zipCode,
                city: state.invoiceInformation.city,
                country: state.invoiceInformation.country,
                vatId: state.invoiceInformation.vatId,
                fiscalCode: state.invoiceInformation.fiscalCode,
                pec: state.invoiceInformation.pec,
                sdi: state.invoiceInformation.sdi,
              },
            },
          },
        });

        if (orderResult.data.createOrder.__typename !== "CreateOrderResult") {
          return Promise.reject();
        }

        return Promise.resolve(orderResult.data.createOrder.paymentUrl);
      },
    },
  });

  const moneyFormatter = useMoneyFormatter();

  const onCreateOrder = (
    event: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>,
    method: string,
  ) => {
    const form = event.currentTarget.closest("form");
    if (form && !form.checkValidity()) {
      form.reportValidity();
      return;
    }

    createOrderSend({
      type: "createOrder",
      method,
    });
  };

  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);
  const savedAmount = calculateSavedAmount(state, productsById);

  return (
    <BottomBar
      action={
        <div>
          <div className="flex flex-col-reverse lg:flex-row">
            <BasicButton
              disabled={createOrderState.matches("creating")}
              onClick={(e) => {
                onCreateOrder(e, "banktransfer");
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
              disabled={createOrderState.matches("creating")}
              onClick={(e) => {
                onCreateOrder(e, "stripe");
              }}
              fullWidth="mobile"
            >
              <FormattedMessage id="tickets.checkout.payWithCard" />
            </Button>
          </div>
          <div>
            {createOrderState.matches("failed") && (
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
