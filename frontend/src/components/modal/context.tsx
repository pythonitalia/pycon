import { createContext, useContext } from "react";
import { CustomizeTicketModalProps } from "../customize-ticket-modal";
import { ReassignTicketModalProps } from "../reassign-ticket-modal";
import { TicketQRCodeModalProps } from "../ticket-qrcode-modal";

export type ModalProps = {
  "sponsor-lead": null;
  "add-schedule-to-calendar": null;
  newsletter: null;
  "ticket-qr-code": TicketQRCodeModalProps;
  "customize-ticket": CustomizeTicketModalProps;
  "reassign-ticket": ReassignTicketModalProps;
};

export type ModalID = keyof ModalProps;

type ModalStateContextType = {
  modalId: ModalID | null;
  modalProps: ModalProps[keyof ModalProps] | null;
  setCurrentModal: <T extends ModalID>(
    newModal: T,
    props?: ModalProps[T],
  ) => void;
  closeCurrentModal: () => void;
};

export const ModalStateContext = createContext<ModalStateContextType>({
  modalId: null,
  modalProps: null,
  setCurrentModal: () => {},
  closeCurrentModal: () => {},
});

export const useSetCurrentModal = () => {
  const { setCurrentModal } = useContext(ModalStateContext);
  return setCurrentModal;
};

export const useModal = () => {
  const modalState = useContext(ModalStateContext);
  return modalState;
};
