import { assign, createMachine } from "xstate";

import { getApolloClient } from "~/apollo/client";
import { GetVoucherDocument, GetVoucherQuery } from "~/types";

type Context = {
  code: string;
  voucher?: GetVoucherQuery["conference"]["voucher"];
};

const invokeFetchVoucher = async (context: Context) => {
  const code = context.code;

  const apolloClient = getApolloClient();
  const {
    data: {
      conference: { voucher },
    },
  } = await apolloClient.query<GetVoucherQuery>({
    fetchPolicy: "no-cache",
    query: GetVoucherDocument,
    variables: {
      conference: process.env.conferenceCode,
      code,
    },
  });

  if (voucher) {
    return Promise.resolve(voucher);
  }

  return Promise.reject();
};

export const voucherMachine = createMachine<Context>({
  id: "voucher",
  initial: "idle",
  context: {
    code: "",
    voucher: undefined,
  },
  on: {
    changeCode: {
      target: "applying",
      actions: assign({
        code: (_, event) => event.value,
      }),
    },
  },
  states: {
    idle: {},
    notFound: {
      entry: "removeVoucher",
    },
    applying: {
      after: {
        500: {
          target: "fetching",
          cond: (context) => context.code.length > 0,
        },
        501: {
          target: "idle",
          actions: "removeVoucher",
        },
      },
    },
    applied: {
      entry: "applyVoucher",
    },
    fetching: {
      invoke: {
        id: "fetchVoucher",
        src: invokeFetchVoucher,
        onDone: {
          target: "applied",
          actions: assign((context, event) => ({
            voucher: event.data,
          })),
        },
        onError: "notFound",
      },
    },
  },
});
