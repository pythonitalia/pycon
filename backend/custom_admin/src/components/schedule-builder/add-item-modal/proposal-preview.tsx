import type { Language } from "../../../types";
import type { SubmissionFragmentFragment } from "../../fragments/submission.generated";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

type Props = {
  proposal: SubmissionFragmentFragment;
};
export const ProposalPreview = ({ proposal }: Props) => {
  return (
    <li className="p-2 bg-slate-300 odd:bg-slate-200">
      <strong>{proposal.title}</strong>
      {proposal.italianTitle !== proposal.title && (
        <div>{proposal.italianTitle}</div>
      )}

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
