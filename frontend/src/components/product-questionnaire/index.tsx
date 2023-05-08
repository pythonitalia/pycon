import {
  Grid,
  Input,
  InputWrapper,
  Select,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { TicketItem } from "~/types";

import { ProductState } from "../tickets-page/types";

type Props = {
  index: number;
  product: Omit<TicketItem, "variations">;
  productUserInformation: ProductState;
  updateTicketInfo: ({ id, index, key, value }) => void;
  updateQuestionAnswer: ({ id, index, question, answer }) => void;
  hideAttendeeEmail?: boolean;
  cols?: number;
};

export const ProductQuestionnaire = ({
  product,
  productUserInformation,
  index,
  updateTicketInfo,
  updateQuestionAnswer,
  hideAttendeeEmail = false,
  cols = 3,
}: Props) => {
  const answers = productUserInformation.answers;
  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  return (
    <Grid cols={cols} alignItems="end">
      {product.admission && (
        <InputWrapper
          key="attendeeName"
          required={true}
          title={<FormattedMessage id="orderQuestions.attendeeName" />}
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
            placeholder={inputPlaceholder}
            value={productUserInformation.attendeeName}
            errors={
              productUserInformation?.errors && [
                productUserInformation?.errors?.attendeeName,
              ]
            }
          />
        </InputWrapper>
      )}

      {product.admission && !hideAttendeeEmail && (
        <InputWrapper
          key="attendeeEmail"
          required={true}
          title={<FormattedMessage id="orderQuestions.attendeeEmail" />}
        >
          <Input
            required={true}
            type="email"
            placeholder={inputPlaceholder}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              updateTicketInfo({
                id: productUserInformation.id,
                index,
                key: "attendeeEmail",
                value: e.target.value,
              })
            }
            value={productUserInformation.attendeeEmail}
            errors={
              productUserInformation?.errors && [
                productUserInformation?.errors?.attendeeEmail,
              ]
            }
          />
        </InputWrapper>
      )}

      {product.questions.map((question) => (
        <InputWrapper
          key={question.id}
          required={question.required}
          title={question.name}
        >
          {question.options.length === 0 ? (
            <Input
              required={question.required}
              placeholder={inputPlaceholder}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                updateQuestionAnswer({
                  id: productUserInformation.id,
                  index,
                  question: question.id,
                  answer: e.target.value,
                })
              }
              value={answers[question.id]}
              errors={
                productUserInformation?.errors && [
                  productUserInformation?.errors[question.id],
                ]
              }
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
