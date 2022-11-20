/** @jsxRuntime classic */

/** @jsx jsx */
import React, { FormEvent, useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, Input, jsx, Select } from "theme-ui";

import { InputWrapper } from "~/components/input-wrapper";
import { TicketItem } from "~/types";

import { Button } from "../button/button";
import { SelectedProducts } from "./types";

type Props = {
  tickets: TicketItem[];
  selectedProducts: SelectedProducts;
  onNextStep: () => void;
  nextStepMessageId?: string;
  nextStepLoading?: boolean;
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
  showHeading?: boolean;
};

export const QuestionsSection = ({
  tickets,
  selectedProducts,
  onNextStep,
  updateQuestionAnswer,
  updateTicketInfo,
  nextStepMessageId = "order.nextStep",
  showHeading = true,
  nextStepLoading = false,
}: Props) => {
  const productsById = Object.fromEntries(
    tickets.map((product) => [product.id, product]),
  );

  const onSubmit = useCallback((e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onNextStep();
  }, []);

  useEffect(() => {
    Object.values(selectedProducts).forEach((products) => {
      products.forEach((selectedProductInfo, index) => {
        const product = productsById[selectedProductInfo.id];
        product.questions
          .filter((question) => question.options.length > 0)
          .forEach((question) => {
            if (!selectedProductInfo.answers[question.id]) {
              updateQuestionAnswer({
                id: selectedProductInfo.id,
                index,
                question: question.id,
                answer: question.options[0].id,
              });
            }
          });
      });
    });
  }, []);

  return (
    <React.Fragment>
      {showHeading && (
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
      )}

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <form onSubmit={onSubmit}>
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

                    {product.admission && (
                      <InputWrapper
                        key="attendeeName"
                        isRequired={true}
                        label={
                          <FormattedMessage id="orderQuestions.attendeeName" />
                        }
                        errors={
                          selectedProductInfo?.errors && [
                            selectedProductInfo?.errors?.attendeeName,
                          ]
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
                    )}

                    {product.admission && (
                      <InputWrapper
                        key="attendeeEmail"
                        isRequired={true}
                        label={
                          <FormattedMessage id="orderQuestions.attendeeEmail" />
                        }
                        errors={
                          selectedProductInfo?.errors && [
                            selectedProductInfo?.errors?.attendeeEmail,
                          ]
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
                    )}

                    {product.questions.map((question) => (
                      <Box key={question.id}>
                        <InputWrapper
                          isRequired={question.required}
                          label={question.name}
                          errors={
                            selectedProductInfo?.errors && [
                              selectedProductInfo?.errors[question.id],
                            ]
                          }
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
                                e: React.ChangeEvent<HTMLSelectElement>,
                              ) => {
                                updateQuestionAnswer({
                                  id: selectedProductInfo.id,
                                  index,
                                  question: question.id,
                                  answer: e.target.value,
                                });
                              }}
                            >
                              {question.options.map((option) => (
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

          <Button loading={nextStepLoading}>
            <FormattedMessage id={nextStepMessageId} />
          </Button>
        </form>
      </Box>
    </React.Fragment>
  );
};
