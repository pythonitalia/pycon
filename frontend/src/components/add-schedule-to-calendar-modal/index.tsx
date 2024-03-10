import {
  Button,
  Input,
  InputWrapper,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useCurrentUser } from "~/helpers/use-current-user";
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
    prettyCalendarUrl = `${location.origin}/schedule/ical/${data}${pattern.search}`;
  }

  return (
    <Modal
      title={<FormattedMessage id="addScheduleToCalendarModal.title" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <Button variant="secondary">
            <FormattedMessage id="global.accordion.close" />
          </Button>
        </div>
      }
    >
      {!user && (
        <div>
          <Text size={2}>
            <FormattedMessage id="addScheduleToCalendarModal.loginRequired" />
          </Text>
        </div>
      )}
      {user && (
        <div>
          <Text size={2}>
            <FormattedMessage id="addScheduleToCalendarModal.steps" />
          </Text>
          <Spacer size="medium" />
          <InputWrapper>
            <Input readOnly={true} value={prettyCalendarUrl} />
          </InputWrapper>
          <Spacer size="thin" />
          <Text size={2}>
            <FormattedMessage id="addScheduleToCalendarModal.info" />
          </Text>
        </div>
      )}
    </Modal>
  );
};
