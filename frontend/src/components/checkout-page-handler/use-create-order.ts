import { Heading, Section, Spacer } from "@python-italia/pycon-styleguide";
import type React from "react";
import { FormattedMessage } from "react-intl";

import {
  type CurrentUserQueryResult,
  type TicketItem,
  type TicketsQueryResult,
  useCreateOrderMutation,
} from "~/types";

import { useCurrentLanguage } from "~/locale/context";
import type { SelectedProducts } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";
import { BillingCard } from "./billing-card";
import { CreateOrderBar } from "./create-order-bar";
import { ProductsQuestions } from "./products-questions";
import { RecapCard } from "./recap-card";
import { VoucherCard } from "./voucher-card";

export const useCreateOrder = ({ userEmail }) => {
  const code = process.env.conferenceCode;
  const { state } = useCart();
  const [createOrder, { loading, data }] = useCreateOrderMutation();
  const language = useCurrentLanguage();

  const onCreateOrder = async (
    event: React.MouseEvent<HTMLButtonElement | HTMLAnchorElement>,
    method: string,
  ) => {
    const form = event.currentTarget.closest("form");
    if (form && !form.checkValidity()) {
      form.reportValidity();
      return;
    }

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

    const orderResult = await createOrder({
      variables: {
        conference: code,

        input: {
          paymentProvider: method,
          tickets: orderTickets,
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
      return;
    }

    const paymentUrl = orderResult.data.createOrder.paymentUrl;
    window.sessionStorage.removeItem("tickets-cart-v6");
    document.cookie =
      "tickets-cart-v6=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    window.location.href = paymentUrl;
  };

  const creationFailed = data?.createOrder.__typename === "CreateOrderErrors";

  return {
    createOrder: onCreateOrder,
    isCreatingOrder:
      loading || data?.createOrder.__typename === "CreateOrderResult",
    creationFailed,
    errors:
      data?.createOrder.__typename === "CreateOrderErrors"
        ? data?.createOrder.errors
        : null,
  };
};
