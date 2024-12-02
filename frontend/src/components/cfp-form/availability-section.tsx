import {
  CardPart,
  Heading,
  MultiplePartsCard,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { addDays, eachDayOfInterval, format, parseISO } from "date-fns";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { useCurrentLanguage } from "~/locale/context";
import type { CfpFormQuery } from "~/types";

const CHOICES = ["available", "preferred", "unavailable"];
const RANGES = ["am", "pm"];

type Props = {
  conferenceData: CfpFormQuery;
  speakerAvailabilities: any;
  onChangeAvailability: any;
};
export const AvailabilitySection = ({
  conferenceData,
  speakerAvailabilities,
  onChangeAvailability,
}: Props) => {
  const language = useCurrentLanguage();
  const {
    conference: { start, end },
  } = conferenceData;
  const parsedStart = addDays(parseISO(start), 1);
  const parsedEnd = parseISO(end);
  const daysBetween = eachDayOfInterval({ start: parsedStart, end: parsedEnd });
  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "2-digit",
    month: "long",
  });

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
            gridTemplateColumns: `150px repeat(${daysBetween.length}, 1fr)`,
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
              {dateFormatter.format(day)}
            </Text>
          ))}

          {RANGES.map((hour) => (
            <Fragment key={hour}>
              <div>
                <Text weight="strong" size={"label3"} as="p">
                  {hour === "am" ? (
                    <FormattedMessage id="cfp.availability.table.morning" />
                  ) : (
                    <FormattedMessage id="cfp.availability.table.afternoon" />
                  )}
                </Text>
                <Spacer size="thin" />
                <Text weight="strong" size={"label3"} as="p">
                  {hour === "am" ? (
                    <FormattedMessage id="cfp.availability.table.morning.range" />
                  ) : (
                    <FormattedMessage id="cfp.availability.table.afternoon.range" />
                  )}
                </Text>
              </div>
              {daysBetween.map((day) => {
                const availabilityDate = `${format(day, "yyyy-MM-dd")}@${hour}`;
                const currentChoice =
                  speakerAvailabilities?.[availabilityDate] || "available";

                return (
                  <div
                    className="w-full cursor-pointer text-center p-1 bg-grey-50 hover:bg-grey-100"
                    onClick={(_) => {
                      const nextChoice =
                        CHOICES[
                          (CHOICES.indexOf(currentChoice) + 1) % CHOICES.length
                        ];
                      onChangeAvailability(availabilityDate, nextChoice);
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
        </div>

        <Spacer size="small" />

        <Text size={3}>
          <FormattedMessage id="cfp.availability.explanation" />
        </Text>
      </CardPart>
    </MultiplePartsCard>
  );
};
