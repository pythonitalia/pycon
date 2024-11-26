import {
  CardPart,
  Heading,
  MultiplePartsCard,
  Spacer,
  Tag,
  Text,
} from "@python-italia/pycon-styleguide";
import clsx from "clsx";
import {
  eachDayOfInterval,
  eachMinuteOfInterval,
  format,
  parseISO,
  setHours,
  setMinutes,
} from "date-fns";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import type { CfpFormQuery } from "~/types";

const CHOICES = ["available", "preferred", "unavailable"];

type Props = {
  conferenceData: CfpFormQuery;
  selectedDuration: any;
  selectedAvailabilities: any;
  onChangeAvailability: any;
};
export const AvailabilitySection = ({
  conferenceData,
  selectedDuration,
  selectedAvailabilities,
  onChangeAvailability,
}: Props) => {
  const {
    conference: { start, end },
  } = conferenceData;
  const parsedStart = parseISO(start);
  const parsedEnd = parseISO(end);
  const daysBetween = eachDayOfInterval({ start: parsedStart, end: parsedEnd });
  const hoursBetween = eachMinuteOfInterval(
    {
      start: setHours(parsedStart, 9),
      end: setHours(parsedStart, 17),
    },
    {
      step: 30,
    },
  );

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={3}>
          <FormattedMessage id="cfp.availability.title" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left">
        <Text size={2}>
          <FormattedMessage id="cfp.availability.description" />
        </Text>
        <Spacer size="small" />
        <div
          className="grid gap-2 lg:gap-4 select-none"
          style={{
            gridTemplateColumns: `70px repeat(${daysBetween.length}, 1fr)`,
          }}
        >
          <div />

          {daysBetween.map((day) => (
            <Text
              key={day.toISOString()}
              weight="strong"
              size={"label3"}
              align="center"
            >
              {format(day, "EEEE d MMM")}
            </Text>
          ))}

          {hoursBetween.map((hour) => (
            <Fragment key={hour.toISOString()}>
              <div>
                <Text weight="strong" size={"label3"}>
                  {format(hour, "HH:mm")}
                </Text>
              </div>
              {daysBetween.map((day) => {
                const mergedDate = setHours(
                  setMinutes(day, hour.getMinutes()),
                  hour.getHours(),
                );

                const currentChoice =
                  selectedAvailabilities?.[mergedDate.getTime()] || "available";

                return (
                  <div
                    className={clsx("w-full cursor-pointer text-center p-1", {
                      "bg-grey-50 hover:bg-grey-100": true,
                    })}
                    onClick={(_) => {
                      const options = ["available", "preferred", "unavailable"];
                      const nextChoice =
                        options[
                          (options.indexOf(currentChoice) + 1) % options.length
                        ];
                      onChangeAvailability(mergedDate, nextChoice);
                    }}
                  >
                    {currentChoice === "available" && <>&nbsp;</>}
                    {currentChoice === "preferred" && "✔️"}
                    {currentChoice === "unavailable" && "❌"}
                  </div>
                );
              })}
            </Fragment>
          ))}

          <div />
          {daysBetween.map((day) => (
            <div className="flex items-center justify-center gap-1">
              <Text key={day.toISOString()} size={"label3"}>
                (Prefer all)
              </Text>
              /
              <Text key={day.toISOString()} size={"label3"}>
                (Unavailable all)
              </Text>
            </div>
          ))}
        </div>

        <Text size={3}>
          <FormattedMessage
            id="cfp.availability.explanation"
            values={{
              duration: selectedDuration ? (
                <Text size="inherit" weight="strong">
                  ({selectedDuration.name})
                </Text>
              ) : null,
            }}
          />
        </Text>
      </CardPart>
    </MultiplePartsCard>
  );
};
