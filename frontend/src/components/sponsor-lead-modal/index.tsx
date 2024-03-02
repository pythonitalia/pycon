import {
  BasicButton,
  Button,
  Checkbox,
  HorizontalStack,
  Input,
  InputWrapper,
  Link,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useCurrentLanguage } from "~/locale/context";
import { useSendSponsorLeadMutation } from "~/types";

import { createHref } from "../link";
import { Modal } from "../modal";

type SponsorLeadForm = {
  email: string;
  fullname: string;
  company: string;
  consentToContactViaEmail: boolean;
  acceptPrivacyPolicy: boolean;
};
export const SponsorLeadModal = ({ onClose }) => {
  const formRef = useRef<HTMLFormElement>();
  const language = useCurrentLanguage();
  const [sendSponsorLeadMutation, { loading, data, error }] =
    useSendSponsorLeadMutation();
  const [formState, { email, text, checkbox }] = useFormState<SponsorLeadForm>({
    email: "",
    fullname: "",
    company: "",
    consentToContactViaEmail: false,
    acceptPrivacyPolicy: false,
  });

  const onSubmit = (e) => {
    e.preventDefault();
    if (!formRef.current.reportValidity()) {
      return;
    }

    if (!formState.values.acceptPrivacyPolicy) {
      return;
    }

    sendSponsorLeadMutation({
      variables: {
        input: {
          fullname: formState.values.fullname,
          company: formState.values.company,
          email: formState.values.email,
          consentToContactViaEmail: formState.values.consentToContactViaEmail,
          conferenceCode: process.env.conferenceCode,
        },
      },
    });
  };

  const submitComplete =
    data?.sendSponsorLead?.__typename === "OperationResult" &&
    data?.sendSponsorLead?.ok;

  return (
    <Modal
      title={<FormattedMessage id="sponsorLeadModal.title" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={onClose}>
            <FormattedMessage id="modal.cancel" />
          </BasicButton>
          <Button
            disabled={
              loading || submitComplete || !formState.values.acceptPrivacyPolicy
            }
            onClick={onSubmit}
            variant="secondary"
          >
            <FormattedMessage id="sponsorLeadModal.submit" />
          </Button>
        </div>
      }
    >
      <Text size={2}>
        <FormattedMessage id="sponsorLeadModal.body" />
      </Text>
      <Spacer size="medium" />
      {!submitComplete && (
        <form onSubmit={onSubmit} ref={formRef} autoComplete="off">
          <InputWrapper
            title={<FormattedMessage id="signup.fullname" />}
            required={true}
          >
            <Input
              placeholder="Jane Doe"
              required={true}
              {...text("fullname")}
            />
          </InputWrapper>
          <Spacer size="small" />
          <InputWrapper
            title={<FormattedMessage id="sponsorLeadModal.company" />}
            required={true}
          >
            <Input
              placeholder="Save the world with Python TLD"
              required={true}
              {...text("company")}
            />
          </InputWrapper>
          <Spacer size="small" />
          <InputWrapper
            title={<FormattedMessage id="signup.email" />}
            required={true}
          >
            <Input
              placeholder="my-name@my-amazing-company.com"
              required={true}
              {...email("email")}
            />
          </InputWrapper>

          <Spacer size="small" />

          <InputWrapper
            title={
              <FormattedMessage id="sponsorLeadModal.consentToContactViaEmail.heading" />
            }
          >
            <HorizontalStack gap="small" alignItems="center">
              <Checkbox
                {...checkbox("consentToContactViaEmail")}
                size="small"
              />
              <Text size={2} weight="strong">
                <FormattedMessage id="sponsorLeadModal.consentToContactViaEmail.body" />
              </Text>
            </HorizontalStack>
          </InputWrapper>

          <Spacer size="small" />

          <InputWrapper
            title={
              <FormattedMessage id="sponsorLeadModal.acceptPrivacyPolicy.heading" />
            }
            required={true}
          >
            <HorizontalStack gap="small" alignItems="center">
              <Checkbox
                {...checkbox("acceptPrivacyPolicy")}
                required
                size="small"
              />
              <Text size={2} weight="strong">
                <FormattedMessage
                  id="sponsorLeadModal.acceptPrivacyPolicy"
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
          </InputWrapper>
          {error && (
            <Text size={1} color="red">
              {error.message}
            </Text>
          )}
        </form>
      )}
      {submitComplete && (
        <Text size={1}>
          <FormattedMessage id="sponsorLeadModal.completed" />
        </Text>
      )}
    </Modal>
  );
};
