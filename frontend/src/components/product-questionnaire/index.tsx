import {
  Grid,
  Input,
  InputWrapper,
  Select,
} from "@python-italia/pycon-styleguide";
import type React from "react";
import { FormattedMessage } from "react-intl";

import {
  getTranslatedMessage,
  useTranslatedMessage,
} from "~/helpers/use-translated-message";
import type { TicketItem } from "~/types";

import { useCurrentLanguage } from "~/locale/context";
import type { ProductState } from "../tickets-page/types";

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
  const language = useCurrentLanguage();
  const answers = productUserInformation.answers;
  const inputPlaceholder = useTranslatedMessage("input.placeholder");
  const getTranslatedString = (id) => getTranslatedMessage(id, language);

  return (
    <Grid cols={cols} alignItems="end">
      {product.admission && (
        <InputWrapper
          key="attendeeGivenName"
          required={true}
          title={<FormattedMessage id="orderQuestions.attendeeGivenName" />}
        >
          <Input
            required={true}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              updateTicketInfo({
                id: productUserInformation.id,
                index,
                key: "attendeeGivenName",
                value: e.target.value,
              })
            }
            autoComplete="none"
            placeholder={getTranslatedString(
              "orderQuestions.attendeeGivenName.placeholder",
            )}
            value={productUserInformation.attendeeGivenName}
            errors={
              productUserInformation?.errors && [
                productUserInformation?.errors?.attendeeName,
              ]
            }
          />
        </InputWrapper>
      )}
      {product.admission && (
        <InputWrapper
          key="attendeeFamilyName"
          required={true}
          title={<FormattedMessage id="orderQuestions.attendeeFamilyName" />}
        >
          <Input
            required={true}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              updateTicketInfo({
                id: productUserInformation.id,
                index,
                key: "attendeeFamilyName",
                value: e.target.value,
              })
            }
            placeholder={getTranslatedString(
              "orderQuestions.attendeeFamilyName.placeholder",
            )}
            autoComplete="none"
            value={productUserInformation.attendeeFamilyName}
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
            autoComplete="email"
            type="email"
            placeholder={inputPlaceholder}
            disabled={productUserInformation.isMe}
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
              autoComplete="off"
              type="text"
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
