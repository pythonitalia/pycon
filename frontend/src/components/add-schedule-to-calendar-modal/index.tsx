import {
  Button,
  Input,
  InputWrapper,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import posthog from "posthog-js";
import { FormattedMessage } from "react-intl";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { Modal } from "../modal";
import { useLoginState } from "../profile/hooks";

type Props = {
  onClose: () => void;
};

export const AddScheduleToCalendarModal = ({ onClose }: Props) => {
  const [isLoggedIn] = useLoginState();
  const { user } = useCurrentUser({
    skip: !isLoggedIn,
  });

  const link = user?.userScheduleFavouritesCalendarUrl;
  let prettyCalendarUrl = "";
  if (link) {
    const pattern = new URL(link);
    const pathname = pattern.pathname;
    const data = pathname.replace(
      "/schedule/user-schedule-favourites-calendar/",
      "",
    );
    const cacheBuster = Math.random().toString(36).slice(-5);
    prettyCalendarUrl = `${location.origin}/schedule/ical/${data}${pattern.search}&v=c${cacheBuster}`;
  }

  const autoSelectInput = (e: React.MouseEvent<HTMLInputElement>) => {
    (e.target as HTMLInputElement).select();
    document.execCommand("copy");
    posthog.capture("copy-calendar-url");
  };

  const pleaseWaitMessage = useTranslatedMessage("login.loading");

  return (
    <Modal
      title={<FormattedMessage id="addScheduleToCalendarModal.title" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <Button variant="secondary" onClick={onClose}>
            <FormattedMessage id="global.accordion.close" />
          </Button>
        </div>
      }
    >
      {!isLoggedIn && (
        <div>
          <Text size={2}>
            <FormattedMessage id="addScheduleToCalendarModal.loginRequired" />
          </Text>
        </div>
      )}
      {isLoggedIn && (
        <div>
          <Text size={2}>
            <FormattedMessage id="addScheduleToCalendarModal.steps" />
          </Text>
          <Spacer size="medium" />
          <InputWrapper>
            <Input
              onClick={autoSelectInput}
              readOnly={true}
              value={user ? prettyCalendarUrl : ""}
              placeholder={user ? "" : pleaseWaitMessage}
            />
          </InputWrapper>
          <Spacer size="thin" />
          <Text size={3}>
            <FormattedMessage id="addScheduleToCalendarModal.info" />
          </Text>
        </div>
      )}
    </Modal>
  );
};
