import {
  Button,
  Spacer,
  Text,
  Input,
  InputWrapper,
  BasicButton,
  Link,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { Modal } from "../modal";

export const NewsletterModal = ({ openModal, show }) => {
  const formRef = useRef<HTMLFormElement>();
  const [email, setEmail] = useState("");
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

  const canSubmit =
    email.trim() !== "" &&
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
          email,
        },
      });
    },
    [email, hasCompletedSubscription, loading],
  );

  const errorMessage = useTranslatedMessage("newsletter.error");

  const getErrors = (key: "validationEmail" | "nonFieldErrors") =>
    (hasFormErrors && data.subscribeToNewsletter[key]) || [];
  const closeModal = () => {
    openModal(false);
    reset();
  };

  return (
    <Modal
      title={<FormattedMessage id="footer.stayTuned" />}
      onClose={() => closeModal()}
      show={show}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={() => closeModal()}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button role="secondary" onClick={onSubmit} disabled={!canSubmit}>
            <FormattedMessage id="newsletter.button" />
          </Button>
        </div>
      }
    >
      <form onSubmit={onSubmit} ref={formRef}>
        <Text size={2}>
          <FormattedMessage id="newsletter.text" />
        </Text>
        <Spacer size="small" />

        <InputWrapper title={<FormattedMessage id="signup.email" />}>
          <Input
            placeholder="guido@python.org"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setEmail(e.target.value)
            }
            value={email}
            required={true}
            type="email"
            errors={[
              ...getErrors("validationEmail"),
              error || isUnableToSubscribe ? errorMessage : "",
            ]}
          />
        </InputWrapper>

        {hasCompletedSubscription && !isUnableToSubscribe && (
          <Text size={2}>
            {subscribeToNewsletter.status ==
              NewsletterSubscriptionResult.Subscribed && (
              <FormattedMessage id="newsletter.success" />
            )}
            {subscribeToNewsletter.status ==
              NewsletterSubscriptionResult.WaitingConfirmation && (
              <FormattedMessage id="newsletter.confirmViaEmail" />
            )}
            {subscribeToNewsletter.status ==
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
                      <Text decoration="underline" color="none" size="inherit">
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
        )}
      </form>
    </Modal>
  );
};
