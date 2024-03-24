import { AddScheduleToCalendarModal } from "../add-schedule-to-calendar-modal";
import {
  CustomizeTicketModal,
  CustomizeTicketModalProps,
} from "../customize-ticket-modal";
import { useModal } from "../modal/context";
import { NewsletterModal } from "../newsletter-modal";
import {
  ReassignTicketModal,
  ReassignTicketModalProps,
} from "../reassign-ticket-modal";
import { SponsorLeadModal } from "../sponsor-lead-modal";
import {
  TicketQRCodeModal,
  TicketQRCodeModalProps,
} from "../ticket-qrcode-modal";

export const ModalRenderer = () => {
  const { modalId, modalProps, closeCurrentModal } = useModal();

  if (modalId === null) {
    return null;
  }

  switch (modalId) {
    case "sponsor-lead":
      return <SponsorLeadModal onClose={closeCurrentModal} />;
    case "add-schedule-to-calendar":
      return <AddScheduleToCalendarModal onClose={closeCurrentModal} />;
    case "newsletter":
      return <NewsletterModal onClose={closeCurrentModal} />;
    case "ticket-qr-code":
      return (
        <TicketQRCodeModal
          onClose={closeCurrentModal}
          {...(modalProps as TicketQRCodeModalProps)}
        />
      );
    case "customize-ticket":
      return (
        <CustomizeTicketModal
          onClose={closeCurrentModal}
          {...(modalProps as CustomizeTicketModalProps)}
        />
      );
    case "reassign-ticket":
      return (
        <ReassignTicketModal
          onClose={closeCurrentModal}
          {...(modalProps as ReassignTicketModalProps)}
        />
      );
    default:
      console.error("Unknown modalId", modalId);
      return null;
  }
};
