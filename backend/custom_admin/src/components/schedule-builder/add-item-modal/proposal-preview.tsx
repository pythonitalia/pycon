import type { Language } from "../../../types";
import type { SubmissionFragmentFragment } from "../../fragments/submission.generated";
import type { AvailabilityValue } from "../../utils/availability";
import { getSlotAvailabilityKey } from "../../utils/availability";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

const AVAILABILITY_STYLES: Record<
  AvailabilityValue,
  { label: string; className: string }
> = {
  preferred: {
    label: "Preferred",
    className: "bg-green-200 text-green-900 font-semibold",
  },
  available: { label: "Available", className: "bg-blue-100 text-blue-900" },
  unavailable: {
    label: "Unavailable",
    className: "bg-red-200 text-red-900 font-semibold",
  },
};

type Props = {
  proposal: SubmissionFragmentFragment;
};

export const ProposalPreview = ({ proposal }: Props) => {
  const { data } = useAddItemModal();

  const availabilityKey =
    data?.day?.day && data?.slot?.hour
      ? getSlotAvailabilityKey(data.day.day, data.slot.hour)
      : null;

  const availabilities: Record<string, AvailabilityValue> =
    proposal.speaker?.participant?.speakerAvailabilities ?? {};

  const slotAvailability = availabilityKey
    ? availabilities[availabilityKey]
    : undefined;

  return (
    <li className="p-2 bg-slate-300 odd:bg-slate-200">
      <div className="flex items-start justify-between gap-2">
        <div>
          <strong>{proposal.title}</strong>
          {proposal.italianTitle !== proposal.title && (
            <div>{proposal.italianTitle}</div>
          )}
        </div>
        {slotAvailability && (
          <span
            className={`shrink-0 text-xs px-2 py-0.5 rounded ${AVAILABILITY_STYLES[slotAvailability].className}`}
          >
            {AVAILABILITY_STYLES[slotAvailability].label}
          </span>
        )}
      </div>

      <InfoRecap
        info={[
          { label: "Type", value: proposal.type.name },
          { label: "Duration", value: `${proposal.duration.duration} mins` },
          { label: "Speaker", value: proposal.speaker.fullName },
        ]}
      />
      <AddActions proposal={proposal} />
    </li>
  );
};

const AddActions = ({ proposal }: { proposal: SubmissionFragmentFragment }) => {
  const { conferenceId } = useCurrentConference();
  const { data, close } = useAddItemModal();
  const [createScheduleItem] = useCreateScheduleItemMutation();
  const languages = proposal.languages;
  const onCreate = async (language: Language) => {
    await createScheduleItem({
      variables: {
        input: {
          conferenceId,
          type:
            proposal.type.name.toLowerCase() === "talk" ? "talk" : "training",
          proposalId: proposal.id,
          languageId: language.id,
          slotId: data.slot.id,
          rooms: [data.room.id],
        },
      },
    });
    close();
  };

  return (
    <div>
      {languages.map((language) => (
        <button
          type="button"
          onClick={(e) => onCreate(language)}
          className="btn mr-3"
          key={language.id}
        >
          Add to schedule in {language.name}
        </button>
      ))}
    </div>
  );
};
