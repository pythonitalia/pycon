import {
  BasicButton,
  Button,
  Grid,
  GridColumn,
  Link,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useCurrentLanguage } from "~/locale/context";
import {
  MyProfileWithTicketsDocument,
  MyProfileWithTicketsQuery,
  useUpdateTicketMutation,
} from "~/types";

import { useState } from "react";
import { Badge } from "../badge";
import { createHref } from "../link";
import { Modal } from "../modal";
import { ProductQuestionnaire } from "../product-questionnaire";

type Props = {
  onClose: () => void;
};

export const snakeToCamel = (str: string) => {
  return str.replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
};

export type CustomizeTicketModalProps = {
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
};

type Form = {
  id: string;
  attendeeName: string;
  attendeeEmail: string;
  answers: { [key: string]: string };
  isMe: boolean;
};

export const CustomizeTicketModal = ({
  onClose,
  ticket,
}: Props & CustomizeTicketModalProps) => {
  const language = useCurrentLanguage();

  const callUpdateUserTicket = (updatedProductUserInformation) => {
    const answers = ticket.item.questions
      .map((question) => {
        let answer: string;
        let option = null;

        if (question.options.length > 0) {
          option = question.options.filter(
            (option) =>
              option.id === updatedProductUserInformation.answers[question.id],
          )[0];
          answer = option.name;
        } else {
          answer = updatedProductUserInformation.answers[question.id] || "";
        }

        const data: {
          answer: string;
          question: string;
          options?: string[];
        } = {
          answer,
          question: question.id,
        };

        if (option) {
          data.options = [option.id];
        }
        return data;
      })
      .filter((item) => item.answer !== "");

    updateTicket({
      variables: {
        conference: process.env.conferenceCode,
        language: language,
        input: {
          id: updatedProductUserInformation.id,
          name: updatedProductUserInformation.attendeeName,
          email: updatedProductUserInformation.attendeeEmail,
          answers,
        },
      },
    });
  };

  const [updateTicket, { loading: updatingTicket, error: updateTicketError }] =
    useUpdateTicketMutation({
      onCompleted(result) {
        if (
          result.updateAttendeeTicket.__typename ===
          "UpdateAttendeeTicketErrors"
        ) {
          setErrors(
            Object.fromEntries(
              result.updateAttendeeTicket.errors.map((error) => [
                snakeToCamel(error.field),
                error.message,
              ]),
            ),
          );
          return;
        }
      },
    });

  const saveTicketChanges = (updatedProductUserInformation: any) => {
    setErrors({});
    setProductUserInformation(updatedProductUserInformation);
    callUpdateUserTicket(updatedProductUserInformation);
  };

  const [productUserInformation, setProductUserInformation] = useState({
    id: ticket.id,
    attendeeName: ticket.name ?? "",
    attendeeEmail: ticket.email ?? "",
    errors: {},
    answers: ticket.item.questions.reduce((acc, question) => {
      acc[question.id] =
        question.options.length > 0
          ? question.answer?.options[0] ?? question.options[0].id
          : question.answer?.answer;
      return acc;
    }, {}),
    isMe: false,
  });
  const [errors, setErrors] = useState({});

  const [formState] = useFormState<Form>({
    id: productUserInformation.id,
    attendeeName: productUserInformation.attendeeName,
    attendeeEmail: productUserInformation.attendeeEmail,
    answers: productUserInformation.answers,
    isMe: productUserInformation.isMe,
  });

  const taglineQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "tagline",
  );
  const taglineAnswer = formState.values.answers[taglineQuestion.id];

  const pronounsQuestion = ticket.item.questions.find(
    (question) =>
      question.name.toLowerCase() === "pronouns" ||
      question.name.toLowerCase() === "pronomi",
  );
  const pronounsAnswer = pronounsQuestion.options.find(
    (option) => option.id === formState.values.answers[pronounsQuestion.id],
  )?.name;

  return (
    <Modal
      size="large"
      title={<FormattedMessage id="profile.ticketsEdit.modalTitle" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={onClose}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button
            disabled={updatingTicket}
            size="small"
            onClick={() => saveTicketChanges(formState.values)}
            variant="secondary"
          >
            <FormattedMessage id="profile.tickets.save" />
          </Button>
        </div>
      }
    >
      <Grid cols={3}>
        <GridColumn colSpan={2}>
          <ProductQuestionnaire
            product={ticket.item}
            index={0}
            cols={1}
            hideAttendeeEmail={true}
            productUserInformation={{
              ...formState.values,
              errors,
            }}
            updateTicketInfo={({ key, value }) => {
              formState.setField(key, value);
            }}
            updateQuestionAnswer={({ question, answer }) => {
              formState.setField("answers", {
                ...formState.values.answers,
                [question]: answer,
              });
            }}
          />
          {updateTicketError && (
            <Text size="label4" color="red">
              <FormattedMessage id="global.somethingWentWrong" />
            </Text>
          )}
        </GridColumn>
        <GridColumn>
          <div className="max-w-[302px] max-h-[453px]">
            <Badge
              name={formState.values.attendeeName}
              pronouns={pronounsAnswer}
              tagline={taglineAnswer}
              cutLines={false}
              role={ticket.role}
              hashedTicketId={ticket.hashid}
            />
          </div>
          <div>
            <Spacer size="small" />
            <Text size="label3" as="p">
              <FormattedMessage id="profile.ticketsEdit.qrCodeDescription" />
            </Text>
            <Spacer size="small" />
            <Link
              href={createHref({
                path: "/profile/edit",
                locale: language,
              })}
              target="_blank"
            >
              <Text size="label3" as="p" color="none">
                <FormattedMessage id="profile.ticketsEdit.editProfile" />
              </Text>
            </Link>
          </div>
        </GridColumn>
      </Grid>
    </Modal>
  );
};
