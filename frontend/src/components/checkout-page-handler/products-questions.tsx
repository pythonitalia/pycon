import {
  Checkbox,
  Heading,
  HorizontalStack,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentUser } from "~/helpers/use-current-user";
import { TicketItem } from "~/types";

import { ProductQuestionnaire } from "../product-questionnaire";
import { useLoginState } from "../profile/hooks";
import { useCart } from "../tickets-page/use-cart";
import { AnswersCard } from "./answers-card";

type Props = {
  productsById: { [id: number]: TicketItem };
};

export const ProductsQuestions = ({ productsById }: Props) => {
  const {
    state: { selectedProducts },
  } = useCart();
  const { updateTicketInfo, updateQuestionAnswer } = useCart();
  const [isLoggedIn] = useLoginState();
  const { user: me } = useCurrentUser({
    skip: !isLoggedIn,
  });

  return (
    <>
      {Object.entries(selectedProducts)
        .filter(([productId]) => productsById[productId].questions.length > 0)
        .map(([productId, selection]) => {
          return (
            <Fragment>
              <AnswersCard
                title={productsById[productId].name}
                openByDefault={true}
              >
                {selection.map((productUserInformation, index) => (
                  <>
                    <HorizontalStack justifyContent="spaceBetween">
                      <Heading size={4}>
                        {productsById[productId].name} #{index + 1}
                      </Heading>
                      {index === 0 && (
                        <>
                          <label className="flex items-center">
                            <Text size="label3" uppercase weight="strong">
                              <FormattedMessage id="productQuestions.thisIsMyTicket" />
                            </Text>
                            <Spacer size="small" orientation="horizontal" />
                            <Checkbox
                              size="small"
                              checked={productUserInformation.isMe}
                              onChange={() => {
                                const isMe = !productUserInformation.isMe;
                                updateTicketInfo({
                                  id: productUserInformation.id,
                                  index,
                                  key: "isMe",
                                  value: isMe,
                                });
                                if (isMe) {
                                  updateTicketInfo({
                                    id: productUserInformation.id,
                                    index,
                                    key: "attendeeEmail",
                                    value: me.email,
                                  });
                                }
                              }}
                            />
                          </label>
                        </>
                      )}
                    </HorizontalStack>
                    <Spacer size="2md" />
                    <ProductQuestionnaire
                      index={index}
                      productUserInformation={productUserInformation}
                      product={productsById[productId]}
                      updateTicketInfo={updateTicketInfo}
                      updateQuestionAnswer={updateQuestionAnswer}
                    />
                    {index !== selection.length - 1 && <Spacer size="large" />}
                  </>
                ))}
              </AnswersCard>
              <Spacer size="xs" />
            </Fragment>
          );
        })}
    </>
  );
};
