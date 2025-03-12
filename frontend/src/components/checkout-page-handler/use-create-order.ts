import type React from "react";

import { useCreateOrderMutation } from "~/types";

import { useCurrentLanguage } from "~/locale/context";
import type { SelectedProducts } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

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
        attendeeName: {
          parts: {
            given_name: product.attendeeGivenName,
            family_name: product.attendeeFamilyName,
          },
          scheme: "given_family",
        },
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
