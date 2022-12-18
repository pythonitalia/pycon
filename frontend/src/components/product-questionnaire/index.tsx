import { Grid } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";
import { Select } from "theme-ui";

import { TicketItem } from "~/types";

import { InputWrapper } from "../input-wrapper";
import { Input } from "../inputs";
import { ProductState } from "../tickets-page/types";

type Props = {
  index: number;
  product: TicketItem;
  productUserInformation: ProductState;
  updateTicketInfo: ({ id, index, key, value }) => void;
  updateQuestionAnswer: ({ id, index, question, answer }) => void;
};

export const ProductQuestionnaire = ({
  product,
  productUserInformation,
  index,
  updateTicketInfo,
  updateQuestionAnswer,
}: Props) => {
  const answers = productUserInformation.answers;

  return (
    <Grid cols={3} alignItems="end">
      {product.admission && (
        <InputWrapper
          sx={{ mb: 0 }}
          key="attendeeName"
          isRequired={true}
          label={<FormattedMessage id="orderQuestions.attendeeName" />}
          errors={
            productUserInformation?.errors && [
              productUserInformation?.errors?.attendeeName,
            ]
          }
        >
          <Input
            required={true}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              updateTicketInfo({
                id: productUserInformation.id,
                index,
                key: "attendeeName",
                value: e.target.value,
              })
            }
            value={productUserInformation.attendeeName}
          />
        </InputWrapper>
      )}

      {product.admission && (
        <InputWrapper
          sx={{ mb: 0 }}
          key="attendeeEmail"
          isRequired={true}
          label={<FormattedMessage id="orderQuestions.attendeeEmail" />}
          errors={
            productUserInformation?.errors && [
              productUserInformation?.errors?.attendeeEmail,
            ]
          }
        >
          <Input
            required={true}
            type="email"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              updateTicketInfo({
                id: productUserInformation.id,
                index,
                key: "attendeeEmail",
                value: e.target.value,
              })
            }
            value={productUserInformation.attendeeEmail}
          />
        </InputWrapper>
      )}

      {product.questions.map((question) => (
        <InputWrapper
          key={question.id}
          sx={{ mb: 0 }}
          isRequired={question.required}
          label={question.name}
          errors={
            productUserInformation?.errors && [
              productUserInformation?.errors[question.id],
            ]
          }
        >
          {question.options.length === 0 ? (
            <Input
              required={question.required}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                updateQuestionAnswer({
                  id: productUserInformation.id,
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
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
                updateQuestionAnswer({
                  id: productUserInformation.id,
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
      ))}
    </Grid>
  );
};
