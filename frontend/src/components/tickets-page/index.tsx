/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps, Router } from "@reach/router";
import { Box, Text } from "@theme-ui/components";
import React, { useCallback, useContext, useEffect, useReducer } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useLoginState } from "../../app/profile/hooks";
import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  TicketsQuery,
  TicketsQueryVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { MetaTags } from "../meta-tags";
import { InformationSection } from "./information";
import { QuestionsSection } from "./questions";
import { reducer } from "./reducer";
import { ReviewOrder } from "./review-order";
import { TicketsSection } from "./tickets";
import TICKETS_QUERY from "./tickets.graphql";
import { OrderState } from "./types";
import {
  hasAnsweredTicketsQuestions,
  hasOrderInformation,
  hasSelectedAtLeastOneProduct,
} from "./utils";

export const TicketsPage: React.SFC<RouteComponentProps> = props => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();
  const [isLoggedIn] = useLoginState();

  const { loading, error, data } = useQuery<
    TicketsQuery,
    TicketsQueryVariables
  >(TICKETS_QUERY, {
    variables: {
      conference: conferenceCode,
      language,
      isLogged: isLoggedIn,
    },
  });

  const emptyInitialCartReducer = {
    selectedProducts: {},
    invoiceInformation: {
      isBusiness: false,
      companyName: "",
      name: "",
      vatId: "",
      address: "",
      zipCode: "",
      city: "",
      country: "",
      fiscalCode: "",
    },
    selectedHotelRooms: {},
  };

  let storedCart = null;

  if (typeof window !== "undefined") {
    storedCart = JSON.parse(
      window.localStorage.getItem("tickets-cart")!,
    ) as OrderState | null;
  }

  const [state, dispatcher] = useReducer(
    reducer,
    storedCart || emptyInitialCartReducer,
  );

  useEffect(() => {
    window.localStorage.setItem("tickets-cart", JSON.stringify(state));
  }, [state]);

  const hotelRooms = data?.conference.hotelRooms || [];
  const tickets = data?.conference.tickets || [];

  const addProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "incrementProduct",
      id,
      variation,
    });

  const removeProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "decrementProduct",
      id,
      variation,
    });

  const updateQuestionAnswer = useCallback(
    ({ id, index, question, answer }) =>
      dispatcher({
        type: "updateTicketAnswer",
        id,
        index,
        question,
        answer,
      }),
    [],
  );

  const updateTicketInfo = useCallback(
    ({ id, index, key, value }) =>
      dispatcher({
        type: "updateTicketInfo",
        id,
        index,
        key,
        value,
      }),
    [],
  );

  const updateIsBusiness = useCallback(
    (isBusiness: boolean) =>
      dispatcher({
        type: "updateIsBusiness",
        isBusiness,
      }),
    [],
  );

  const addHotelRoom = useCallback((id, checkin, checkout) => {
    dispatcher({
      type: "addHotelRoom",
      id,
      checkin,
      checkout,
    });
  }, []);

  const removeHotelRoom = useCallback((id, index) => {
    dispatcher({
      type: "removeHotelRoom",
      id,
      index,
    });
  }, []);

  const goToQuestionsOrReview = () => {
    const productIds = Object.values(
      state.selectedProducts,
    ).flatMap(instances => instances.map(product => product.id));

    const selectedProductsInfo = tickets.filter(ticket =>
      productIds.includes(ticket.id),
    );

    const numberOfQuestions = selectedProductsInfo
      .map(info => info.questions.length)
      .reduce((sum, length) => sum + length, 0);

    if (numberOfQuestions > 0) {
      props.navigate!("questions");
    } else {
      props.navigate!("review");
    }
  };

  useEffect(() => {
    const isHome = location.pathname.endsWith("tickets/");

    if (isHome) {
      return;
    }

    if (!isLoggedIn) {
      props.navigate!(`/${language}/login`, { replace: true });
      return;
    }

    if (!hasSelectedAtLeastOneProduct(state)) {
      props.navigate!("", { replace: true });
      return;
    }

    if (!hasOrderInformation(state)) {
      props.navigate!("information", { replace: true });
      return;
    }

    if (tickets.length > 0 && !hasAnsweredTicketsQuestions(state, tickets)) {
      props.navigate!("questions", { replace: true });
      return;
    }
  }, [typeof location === "undefined" ? null : location.pathname, tickets]);

  if (error) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Alert variant="alert">{error.message}</Alert>
      </Box>
    );
  }

  return (
    <Box mb={5}>
      <FormattedMessage id="tickets.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Text>
            <FormattedMessage id="tickets.loading" />
          </Text>
        )}

        {!loading && (
          <Router>
            <TicketsSection
              default={true}
              state={state}
              conferenceStart={data?.conference.start}
              conferenceEnd={data?.conference.end}
              hotelRooms={hotelRooms}
              selectedHotelRooms={state.selectedHotelRooms}
              tickets={tickets}
              selectedProducts={state.selectedProducts}
              addProduct={addProduct}
              removeProduct={removeProduct}
              addHotelRoom={addHotelRoom}
              removeHotelRoom={removeHotelRoom}
              invoiceInformation={state.invoiceInformation}
              onUpdateIsBusiness={updateIsBusiness}
              onNextStep={() => {
                if (isLoggedIn) {
                  props.navigate!("information");
                } else {
                  props.navigate!(`/${language}/login`, {
                    state: {
                      next: `/${language}/tickets/information/`,
                    },
                  });
                }
              }}
            />
            <InformationSection
              path="information"
              onUpdateInformation={invoiceData =>
                dispatcher({
                  type: "updateInvoiceInformation",
                  data: invoiceData,
                })
              }
              invoiceInformation={state.invoiceInformation}
              onNextStep={goToQuestionsOrReview}
            />
            <QuestionsSection
              path="questions"
              tickets={tickets}
              updateTicketInfo={updateTicketInfo}
              updateQuestionAnswer={updateQuestionAnswer}
              selectedProducts={state.selectedProducts}
              onNextStep={() => props.navigate!("review")}
            />

            <ReviewOrder
              email={data?.me?.email!}
              tickets={tickets}
              hotelRooms={hotelRooms}
              state={state}
              path="review"
            />
          </Router>
        )}
      </Box>
    </Box>
  );
};
