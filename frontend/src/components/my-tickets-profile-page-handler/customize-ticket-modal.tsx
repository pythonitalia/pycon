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
import { MyProfileWithTicketsQuery } from "~/types";

import { Badge } from "../badge";
import { createHref } from "../link";
import { Modal } from "../modal";
import { ProductQuestionnaire } from "../product-questionnaire";

type Props = {
  open: boolean;
  openModal: (open: boolean) => void;
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
  productUserInformation: any;
  updatingTicket: boolean;
  updateTicketError: any;
  saveChanges: (updatedProductUserInformation: any) => void;
  errors: { [key: string]: string };
};

type Form = {
  id: string;
  attendeeName: string;
  attendeeEmail: string;
  answers: { [key: string]: string };
};

export const CustomizeTicketModal = ({
  open,
  openModal,
  ticket,
  updatingTicket,
  updateTicketError,
  saveChanges,
  productUserInformation,
  errors,
}: Props) => {
  const language = useCurrentLanguage();
  const [formState] = useFormState<Form>({
    id: productUserInformation.id,
    attendeeName: productUserInformation.attendeeName,
    attendeeEmail: productUserInformation.attendeeEmail,
    answers: productUserInformation.answers,
  });

  const taglineQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "tagline",
  );
  const taglineAnswer = formState.values.answers[taglineQuestion.id];

  const pronounsQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "pronouns",
  );
  const pronounsAnswer = pronounsQuestion.options.find(
    (option) => option.id === formState.values.answers[pronounsQuestion.id],
  )?.name;

  return (
    <Modal
      size="large"
      title={<FormattedMessage id="profile.ticketsEdit.modalTitle" />}
      onClose={() => openModal(false)}
      show={open}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={() => openModal(false)}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button
            disabled={updatingTicket}
            size="small"
            role="secondary"
            onClick={() => saveChanges(formState.values)}
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
