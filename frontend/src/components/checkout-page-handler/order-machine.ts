import { createMachine, assign } from "xstate";

type Context = {
  paymentUrl?: string;
};

export const createOrderMachine = createMachine<Context>(
  {
    id: "create-order",
    initial: "idle",
    context: {},
    on: {
      createOrder: {
        target: "creating",
      },
    },
    states: {
      idle: {},
      creating: {
        invoke: {
          id: "createOrder",
          src: "createOrder",
          onDone: {
            target: "created",
            actions: assign((context, event) => ({
              paymentUrl: event.data,
            })),
          },
          onError: "failed",
        },
      },
      failed: {},
      created: {
        entry: "redirectToPayment",
      },
    },
  },
  {
    actions: {
      redirectToPayment: (context) => {
        if (!context.paymentUrl) {
          return;
        }
        window.sessionStorage.removeItem("tickets-cart-v4");
        window.location.href = context.paymentUrl;
      },
    },
  },
);
