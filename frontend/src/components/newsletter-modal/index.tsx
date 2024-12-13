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
import type React from "react";
import { useCallback, useRef } from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { useFormState } from "react-use-form-state";
import { useCurrentLanguage } from "~/locale/context";
import { createHref } from "../link";
import { Modal } from "../modal";

type NewsletterForm = {
  email: string;
  acceptedPrivacyPolicy: boolean;
};

export const NewsletterModal = ({ onClose }) => {
  const conferenceCode = process.env.conferenceCode;
  const formRef = useRef<HTMLFormElement>(undefined);
  const [formState, { text, checkbox }] = useFormState<NewsletterForm>({
    email: "",
    acceptedPrivacyPolicy: false,
  });
  const [subscribe, { loading, error, data, reset }] = useSubscribeMutation();
  const subscribeToNewsletter = data?.subscribeToNewsletter;

  const hasFormErrors =
    subscribeToNewsletter?.__typename === "SubscribeToNewsletterErrors";
  const hasCompletedSubscription =
    subscribeToNewsletter?.__typename === "NewsletterSubscribeResult";
  const isUnableToSubscribe =
    hasCompletedSubscription &&
    subscribeToNewsletter?.status ===
      NewsletterSubscriptionResult.UnableToSubscribe;
  const language = useCurrentLanguage();

  const canSubmit =
    formState.values.email.trim() !== "" &&
    formState.values.acceptedPrivacyPolicy &&
    !loading &&
    (!hasCompletedSubscription ||
      (hasCompletedSubscription && isUnableToSubscribe));

  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      if (
        loading ||
        (hasCompletedSubscription && !isUnableToSubscribe) ||
        !formRef.current.reportValidity()
      ) {
        return;
      }

      subscribe({
        variables: {
          input: {
            email: formState.values.email,
            conferenceCode,
          },
        },
      });
    },
    [formState.values, hasCompletedSubscription, loading],
  );

  const errorMessage = useTranslatedMessage("newsletter.error");

  const getErrors = (key: "validationEmail" | "nonFieldErrors") =>
    (hasFormErrors && subscribeToNewsletter.errors[key]) || [];

  return (
    <Modal
      title={<FormattedMessage id="footer.stayTuned" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={onClose}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button onClick={onSubmit} disabled={!canSubmit} variant="secondary">
            <FormattedMessage id="newsletter.button" />
          </Button>
        </div>
      }
    >
      <form onSubmit={onSubmit} ref={formRef} autoComplete="off">
        <Text size={2}>
          <FormattedMessage id="newsletter.text" />
        </Text>
        <Spacer size="small" />

        <InputWrapper title={<FormattedMessage id="signup.email" />}>
          <Input
            placeholder="guido@python.org"
            {...text("email")}
            required={true}
            type="email"
            errors={[
              ...getErrors("validationEmail"),
              error || isUnableToSubscribe ? errorMessage : "",
            ]}
          />
        </InputWrapper>

        <Spacer size="small" />

        <label htmlFor="acceptedPrivacyPolicy">
          <HorizontalStack gap="small" alignItems="center">
            <Checkbox
              {...checkbox("acceptedPrivacyPolicy")}
              checked={formState.values.acceptedPrivacyPolicy}
              required
              id="acceptedPrivacyPolicy"
            />
            <Text size={2} weight="strong" hoverColor="none">
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
                      <Text
                        size="inherit"
                        weight="strong"
                        decoration="underline"
                        hoverColor="green"
                      >
                        <FormattedMessage id="signup.privacyPolicy" />
                      </Text>
                    </Link>
                  ),
                }}
              />
            </Text>
          </HorizontalStack>
        </label>

        {hasCompletedSubscription && !isUnableToSubscribe && (
          <>
            <Spacer size="small" />
            <Text size={2}>
              {subscribeToNewsletter.status ===
                NewsletterSubscriptionResult.Subscribed && (
                <FormattedMessage id="newsletter.success" />
              )}
              {subscribeToNewsletter.status ===
                NewsletterSubscriptionResult.WaitingConfirmation && (
                <FormattedMessage id="newsletter.confirmViaEmail" />
              )}
              {subscribeToNewsletter.status ===
                NewsletterSubscriptionResult.OptInFormRequired && (
                <FormattedMessage
                  id="newsletter.optinFormRequired"
                  values={{
                    link: (
                      <Link
                        href="https://pythonitalia.myflodesk.com/manual-optin"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <Text
                          decoration="underline"
                          color="none"
                          size="inherit"
                        >
                          <FormattedMessage
                            id={"newsletter.optinFormRequired.link"}
                          />
                        </Text>
                      </Link>
                    ),
                  }}
                />
              )}
            </Text>
          </>
        )}
      </form>
    </Modal>
  );
};
