/** @jsx jsx */
import { Box, Button, Flex, Select } from "@theme-ui/components";
import moment from "moment";
import { useCallback, useMemo } from "react";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

type Props = {
  conferenceStart?: string;
  conferenceEnd?: string;
  addRoom: (checkin: moment.Moment, checkout: moment.Moment) => void;
};
type Form = {
  checkin: string;
  checkout: string;
};

export const DATE_FORMAT = "MMM DD";

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

  const daysBetween =
    momentConferenceEnd.diff(momentConferenceStart, "days") + 1;

  let checkinDate: moment.Moment | null = null;
  let daysBetweenCheckinAndEnd = 0;

  if (formState.values.checkin) {
    checkinDate = momentConferenceStart
      .clone()
      .add(formState.values.checkin, "days");

    daysBetweenCheckinAndEnd = momentConferenceEnd.diff(checkinDate, "days");
  }

  const addRoomCallback = useCallback(() => {
    if (!checkinDate || !formState.values.checkout) {
      return;
    }

    addRoom(
      checkinDate,
      checkinDate.clone().add(formState.values.checkout, "days"),
    );
  }, [formState.values]);

  return (
    <Flex
      sx={{
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Flex sx={{}}>
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
          <option disabled={true} value="">
            Check-in
          </option>
          {new Array(daysBetween - 1).fill(null).map((_, i) => (
            <option key={i} value={i}>
              {momentConferenceStart
                .clone()
                .add(i, "day")
                .format(DATE_FORMAT)}
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
          <option disabled={true} value="">
            Check-out
          </option>
          {new Array(daysBetweenCheckinAndEnd).fill(null).map((_, i) => (
            <option key={i} value={i + 1}>
              {checkinDate!
                .clone()
                .add(i + 1, "day")
                .format(DATE_FORMAT)}
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
