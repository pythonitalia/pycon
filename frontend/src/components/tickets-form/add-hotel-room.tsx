/** @jsx jsx */
import { Box, Button, Flex, Select } from "@theme-ui/components";
import moment from "moment";
import { useCallback, useMemo } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";

type Props = {
  conferenceStart?: string;
  conferenceEnd?: string;
  addRoom: (checkin: moment.Moment, checkout: moment.Moment) => void;
};
type Form = {
  checkin: string;
  checkout: string;
};

export const AddHotelRoom: React.SFC<Props> = ({
  conferenceEnd,
  conferenceStart,
  addRoom,
}) => {
  const momentConferenceStart = useMemo(() => moment(conferenceStart), [
    conferenceStart,
  ]);
  const momentConferenceEnd = useMemo(() => moment(conferenceEnd), [
    conferenceEnd,
  ]);
  const [formState, { select }] = useFormState<Form>();

  const conferenceRunningDays = momentConferenceEnd.diff(
    momentConferenceStart,
    "days",
  );

  let checkinDate: moment.Moment | null = null;

  const conferenceDays = new Array(conferenceRunningDays)
    .fill(null)
    .map((_, i) => momentConferenceStart.clone().add(i, "days"));

  let daysAfterCheckin: moment.Moment[] = [];

  if (formState.values.checkin) {
    checkinDate = momentConferenceStart
      .clone()
      .add(formState.values.checkin, "days");

    const daysBetweenCheckinAndConferenceEnd = momentConferenceEnd.diff(
      checkinDate,
      "days",
    );

    /* +1 because we need to exclude the checkin day */
    daysAfterCheckin = new Array(daysBetweenCheckinAndConferenceEnd)
      .fill(null)
      .map((_, i) => checkinDate!.clone().add(i + 1, "days"));
  }

  const addRoomCallback = useCallback(() => {
    if (!checkinDate || !formState.values.checkout) {
      return;
    }

    addRoom(
      checkinDate,
      daysAfterCheckin[parseInt(formState.values.checkout, 10)],
    );
  }, [formState.values]);

  const lang = useCurrentLanguage();
  const dateFormatter = new Intl.DateTimeFormat(lang, {
    month: "long",
    day: "2-digit",
  });

  return (
    <Flex
      sx={{
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Flex>
        <Select
          sx={{
            flexShrink: 0,
          }}
          {...select({
            name: "checkin",
            onChange: () => {
              formState.resetField("checkout");
            },
          })}
        >
          <FormattedMessage id="addHotelRoom.checkin">
            {(text) => (
              <option disabled={true} value="">
                {text}
              </option>
            )}
          </FormattedMessage>

          {conferenceDays.map((day, i) => (
            <option key={i} value={i}>
              {dateFormatter.format(day.toDate())}
            </option>
          ))}
        </Select>
        <Select
          sx={{
            marginLeft: 1,
            flexShrink: 0,
          }}
          {...select("checkout")}
          disabled={checkinDate === null}
        >
          <FormattedMessage id="addHotelRoom.checkout">
            {(text) => (
              <option disabled={true} value="">
                {text}
              </option>
            )}
          </FormattedMessage>

          {daysAfterCheckin.map((day, i) => (
            <option key={i} value={i}>
              {dateFormatter.format(day.toDate())}
            </option>
          ))}
        </Select>
      </Flex>
      <Button
        sx={{
          marginLeft: 4,
          flexShrink: 0,
        }}
        variant="plus"
        onClick={addRoomCallback}
      >
        +
      </Button>
    </Flex>
  );
};
