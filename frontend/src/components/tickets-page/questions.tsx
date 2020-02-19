/** @jsx jsx */
import { Box, Button, Heading, Input, Select } from "@theme-ui/components";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";
import { Ticket } from "../tickets-form/types";
import { SelectedProducts } from "./types";

type Props = {
  path: string;
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  onNextStep: () => void;
  updateQuestionAnswer: (data: {
    id: string;
    index: number;
    question: string;
    answer: string;
  }) => void;
  updateTicketInfo: (data: {
    id: string;
    index: number;
    key: string;
    value: string;
  }) => void;
};

export const QuestionsSection: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  onNextStep,
  updateQuestionAnswer,
  updateTicketInfo,
}) => {
  const productsById = Object.fromEntries(
    tickets.map(product => [product.id, product]),
  );

  const onSubmit = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    onNextStep();
  }, []);

  useEffect(() => {
    Object.values(selectedProducts).forEach(products => {
      products.forEach((selectedProductInfo, index) => {
        const product = productsById[selectedProductInfo.id];
        product.questions
          .filter(question => question.options.length > 0)
          .forEach(question => {
            updateQuestionAnswer({
              id: selectedProductInfo.id,
              index,
              question: question.id,
              answer: question.options[0].id,
            });
          });
      });
    });
  }, []);

  return (
    <React.Fragment>
      <Heading as="h1" sx={{ pb: 5, mb: 5, borderBottom: "primary" }}>
        <Box
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
          }}
        >
          <FormattedMessage id="orderQuestions.heading" />
        </Box>
      </Heading>
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Box as="form" onSubmit={onSubmit}>
          {Object.entries(selectedProducts).map(([id, products]) => (
            <Box key={id}>
              {products.map((selectedProductInfo, index) => {
                const product = productsById[selectedProductInfo.id];

                if (product.questions.length === 0) {
                  return null;
                }

                const answers = selectedProductInfo.answers;

                return (
                  <Box key={`${id}${index}`}>
                    <Heading as="h2" sx={{ mb: 2 }}>
                      {product.name}
                    </Heading>

                    <InputWrapper
                      isRequired={true}
                      label={
                        <FormattedMessage id="orderQuestions.attendeeName" />
                      }
                    >
                      <Input
                        required={true}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                          updateTicketInfo({
                            id: selectedProductInfo.id,
                            index,
                            key: "attendeeName",
                            value: e.target.value,
                          })
                        }
                        value={selectedProductInfo.attendeeName}
                      />
                    </InputWrapper>

                    <InputWrapper
                      isRequired={true}
                      label={
                        <FormattedMessage id="orderQuestions.attendeeEmail" />
                      }
                    >
                      <Input
                        required={true}
                        type="email"
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                          updateTicketInfo({
                            id: selectedProductInfo.id,
                            index,
                            key: "attendeeEmail",
                            value: e.target.value,
                          })
                        }
                        value={selectedProductInfo.attendeeEmail}
                      />
                    </InputWrapper>

                    {product.questions.map(question => (
                      <Box key={question.id}>
                        <InputWrapper
                          isRequired={question.required}
                          label={question.name}
                        >
                          {question.options.length === 0 ? (
                            <Input
                              required={question.required}
                              onChange={(
                                e: React.ChangeEvent<HTMLInputElement>,
                              ) =>
                                updateQuestionAnswer({
                                  id: selectedProductInfo.id,
                                  index,
                                  question: question.id,
                                  answer: e.target.value,
                                })
                              }
                              value={answers[question.id]}
                            />
                          ) : (
                            <Select
                              required={question.required}
                              value={answers[question.id]}
                              onChange={(
                                e: React.ChangeEvent<HTMLInputElement>,
                              ) =>
                                updateQuestionAnswer({
                                  id: selectedProductInfo.id,
                                  index,
                                  question: question.id,
                                  answer: e.target.value,
                                })
                              }
                            >
                              {question.options.map(option => (
                                <option key={option.id} value={option.id}>
                                  {option.name}
                                </option>
                              ))}
                            </Select>
                          )}
                        </InputWrapper>
                      </Box>
                    ))}
                  </Box>
                );
              })}
            </Box>
          ))}

          <Button>
            <FormattedMessage id="order.nextStep" />
          </Button>
        </Box>
      </Box>
    </React.Fragment>
  );
};
