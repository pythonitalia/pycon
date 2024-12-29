import {
  Button,
  CardPart,
  Checkbox,
  Grid,
  GridColumn,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  Link,
  MultiplePartsCard,
  Spacer,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  InvitationLetterOnBehalfOf,
  InvitationLetterRequestStatus,
  useInvitationLetterFormQuery,
  useRequestInvitationLetterMutation,
} from "~/types";
import { Alert } from "../alert";
import { createHref } from "../link";

const ON_BEHALF_OF_OPTIONS = [
  {
    label: <FormattedMessage id="invitationLetterForm.onBehalfOf.value.self" />,
    value: InvitationLetterOnBehalfOf.Self,
  },
  {
    label: (
      <FormattedMessage id="invitationLetterForm.onBehalfOf.value.other" />
    ),
    value: InvitationLetterOnBehalfOf.Other,
  },
];

type InvitationLetterFormFields = {
  onBehalfOf: InvitationLetterOnBehalfOf;
  email: string;
  fullName: string;
  nationality: string;
  address: string;
  passportNumber: string;
  embassyName: string;
  acceptedPrivacyPolicy: boolean;
  dateOfBirth: string;
};

export const InvitationLetterForm = () => {
  const {
    data: {
      me: { hasAdmissionTicket, invitationLetterRequest },
    },
  } = useInvitationLetterFormQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  const language = useCurrentLanguage();
  const [formState, { checkbox, radio, text, textarea, email, date }] =
    useFormState<InvitationLetterFormFields>({
      onBehalfOf: InvitationLetterOnBehalfOf.Self,
      acceptedPrivacyPolicy: false,
    });

  const alreadySentRequest = invitationLetterRequest !== null;
  const onBehalfOfSelf =
    formState.values.onBehalfOf === InvitationLetterOnBehalfOf.Self;
  const onBehalfOfOther =
    formState.values.onBehalfOf === InvitationLetterOnBehalfOf.Other;
  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  const [
    requestInvitationLetter,
    {
      loading: isRequestingInvitationLetter,
      data: requestInvitationLetterData,
      error: requestInvitationLetterError,
    },
  ] = useRequestInvitationLetterMutation({
    updateQueries: {
      InvitationLetterForm: (prev, { mutationResult }) => {
        if (
          onBehalfOfOther ||
          mutationResult.data.requestInvitationLetter.__typename !==
            "InvitationLetterRequest"
        ) {
          return prev;
        }

        return {
          ...prev,
          me: {
            ...prev.me,
            invitationLetterRequest:
              mutationResult.data.requestInvitationLetter,
          },
        };
      },
    },
  });
  const canSeeForm =
    onBehalfOfOther ||
    (onBehalfOfSelf && hasAdmissionTicket && !alreadySentRequest);
  const canSubmit =
    formState.values.acceptedPrivacyPolicy &&
    canSeeForm &&
    !isRequestingInvitationLetter;

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (canSubmit) {
      await requestInvitationLetter({
        variables: {
          input: {
            conference: process.env.conferenceCode,
            email: formState.values.email || "",
            fullName: formState.values.fullName,
            address: formState.values.address,
            dateOfBirth: formState.values.dateOfBirth,
            embassyName: formState.values.embassyName,
            nationality: formState.values.nationality,
            onBehalfOf: formState.values.onBehalfOf,
            passportNumber: formState.values.passportNumber,
          },
        },
      });
    }
  };

  const getErrors = (field: string) =>
    (requestInvitationLetterData?.requestInvitationLetter.__typename ===
      "RequestInvitationLetterErrors" &&
      requestInvitationLetterData.requestInvitationLetter.errors[field]) ||
    [];

  const formHasErrors =
    requestInvitationLetterData?.requestInvitationLetter.__typename ===
    "RequestInvitationLetterErrors";
  const requestSubmitted =
    requestInvitationLetterData?.requestInvitationLetter.__typename ===
    "InvitationLetterRequest";

  return (
    <form onSubmit={onSubmit}>
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>
            <FormattedMessage id="invitationLetterForm.title" />
          </Heading>
        </CardPart>
        <CardPart background="milk" contentAlign="left">
          <Grid cols={1} gap="medium">
            <InputWrapper
              required={true}
              title={
                <FormattedMessage id="invitationLetterForm.onBehalfOf.title" />
              }
              description={
                <FormattedMessage id="invitationLetterForm.onBehalfOf.description" />
              }
            >
              <HorizontalStack gap="small">
                {ON_BEHALF_OF_OPTIONS.map((type) => (
                  <label key={type.value}>
                    <HorizontalStack gap="small" alignItems="center">
                      <Checkbox
                        {...radio("onBehalfOf", type.value)}
                        required={true}
                        size="small"
                      />
                      <Text weight="strong" size={2}>
                        {type.label}
                      </Text>
                    </HorizontalStack>
                  </label>
                ))}
              </HorizontalStack>
            </InputWrapper>

            {onBehalfOfSelf && alreadySentRequest && (
              <div>
                <Text size={2}>
                  <FormattedMessage id="invitationLetterForm.requestAlreadySent" />
                </Text>
                <Spacer size="thin" />
                {invitationLetterRequest.status ===
                  InvitationLetterRequestStatus.Pending && (
                  <Text size={2}>
                    <FormattedMessage id="invitationLetterForm.requestStatus.pending" />
                  </Text>
                )}
                {invitationLetterRequest.status ===
                  InvitationLetterRequestStatus.Sent && (
                  <Text size={2}>
                    <FormattedMessage id="invitationLetterForm.requestStatus.sent" />
                  </Text>
                )}
                {invitationLetterRequest.status ===
                  InvitationLetterRequestStatus.Rejected && (
                  <Text size={2}>
                    <FormattedMessage id="invitationLetterForm.requestStatus.rejected" />
                  </Text>
                )}
              </div>
            )}

            {onBehalfOfSelf && !hasAdmissionTicket && (
              <Text size={2} color="error">
                <FormattedMessage id="invitationLetterForm.noAdmissionTicket" />
              </Text>
            )}

            {onBehalfOfOther && (
              <InputWrapper
                required={true}
                title={
                  <FormattedMessage id="invitationLetterForm.email.title" />
                }
                description={
                  <FormattedMessage id="invitationLetterForm.email.description" />
                }
              >
                <Input
                  {...email("email")}
                  required={true}
                  maxLength={320}
                  placeholder={inputPlaceholder}
                  errors={getErrors("email")}
                />
              </InputWrapper>
            )}

            {canSeeForm && (
              <>
                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.fullName.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.fullName.description" />
                  }
                >
                  <Input
                    {...text("fullName")}
                    required={true}
                    placeholder={inputPlaceholder}
                    errors={getErrors("fullName")}
                  />
                </InputWrapper>

                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.dateOfBirth.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.dateOfBirth.description" />
                  }
                >
                  <Input
                    {...date("dateOfBirth")}
                    required={true}
                    placeholder={inputPlaceholder}
                    errors={getErrors("dateOfBirth")}
                  />
                </InputWrapper>

                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.nationality.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.nationality.description" />
                  }
                >
                  <Input
                    {...text("nationality")}
                    required={true}
                    placeholder={inputPlaceholder}
                    errors={getErrors("nationality")}
                    maxLength={100}
                  />
                </InputWrapper>

                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.address.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.address.description" />
                  }
                >
                  <Textarea
                    {...textarea("address")}
                    required={true}
                    maxLength={300}
                    rows={2}
                    placeholder={inputPlaceholder}
                    errors={getErrors("address")}
                  />
                </InputWrapper>

                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.passportNumber.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.passportNumber.description" />
                  }
                >
                  <Input
                    {...text("passportNumber")}
                    required={true}
                    placeholder={inputPlaceholder}
                    errors={getErrors("passportNumber")}
                    maxLength={20}
                  />
                </InputWrapper>

                <InputWrapper
                  required={true}
                  title={
                    <FormattedMessage id="invitationLetterForm.embassyName.title" />
                  }
                  description={
                    <FormattedMessage id="invitationLetterForm.embassyName.description" />
                  }
                >
                  <Input
                    {...text("embassyName")}
                    type="text"
                    required={true}
                    placeholder={inputPlaceholder}
                    errors={getErrors("embassyName")}
                    maxLength={300}
                  />
                </InputWrapper>
              </>
            )}
          </Grid>
        </CardPart>
      </MultiplePartsCard>

      <Spacer size="medium" />

      <Grid cols={3}>
        <GridColumn colSpan={2}>
          <label>
            <HorizontalStack gap="small" alignItems="center">
              <Checkbox
                {...checkbox("acceptedPrivacyPolicy")}
                checked={formState.values.acceptedPrivacyPolicy}
              />
              <Text size={2} weight="strong">
                <FormattedMessage
                  id="global.acceptPrivacyPolicy"
                  values={{
                    link: (
                      <Link
                        className="underline"
                        target="_blank"
                        href={createHref({
                          path: "/privacy-policy",
                          locale: language,
                        })}
                      >
                        Privacy Policy
                      </Link>
                    ),
                  }}
                />
              </Text>
            </HorizontalStack>
          </label>
        </GridColumn>
        <VerticalStack alignItems="end">
          <Button fullWidth="mobile" variant="secondary" disabled={!canSubmit}>
            {!isRequestingInvitationLetter && (
              <FormattedMessage id="global.submit" />
            )}
            {isRequestingInvitationLetter && (
              <FormattedMessage id="global.pleaseWait" />
            )}
          </Button>
          {requestSubmitted && (
            <Alert variant="success">
              <FormattedMessage id="invitationLetterForm.requestSubmitted" />
            </Alert>
          )}
          {formHasErrors && (
            <Alert variant="alert">
              <FormattedMessage id="invitationLetterForm.errors.generic" />
            </Alert>
          )}
          {requestInvitationLetterError && (
            <Alert variant="alert">
              {requestInvitationLetterError.message}
            </Alert>
          )}
        </VerticalStack>
      </Grid>
    </form>
  );
};
