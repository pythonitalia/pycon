import { useModal } from "../modal/context";
import { SponsorLeadModal } from "../sponsor-lead-modal";

export const ModalRenderer = () => {
  const { modalId, closeCurrentModal } = useModal();

  if (modalId === null) {
    return null;
  }

  switch (modalId) {
    case "sponsor-lead":
      return <SponsorLeadModal onClose={closeCurrentModal} />;
    default:
      console.error("Unknown modalId", modalId);
      return null;
  }
};
