import type { Language, Proposal } from "../../../types";
import { useCurrentConference } from "../../utils/conference";
import { useAddItemModal } from "./context";
import { useCreateScheduleItemMutation } from "./create-schedule-item.generated";
import { InfoRecap } from "./info-recap";

type Props = {
  proposal: Proposal;
};
export const ProposalPreview = ({ proposal }: Props) => {
  return (
    <li className="p-2 bg-slate-300 odd:bg-slate-200">
      <strong>{proposal.title}</strong>
      <InfoRecap
        info={[
          { label: "Type", value: proposal.type.name },
          { label: "Duration", value: `${proposal.duration} mins` },
          { label: "Speaker", value: proposal.speaker.fullname },
        ]}
      />
      <AddActions proposal={proposal} />
    </li>
  );
};

const AddActions = ({ proposal }: { proposal: Proposal }) => {
  const conferenceId = useCurrentConference();
  const { data } = useAddItemModal();
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
  };

  return (
    <div>
      {languages.map((language) => (
        <button
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
