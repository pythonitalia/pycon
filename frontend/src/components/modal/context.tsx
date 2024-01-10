import { createContext, useContext } from "react";

type ModalStateContextType = {
  modalId: string | null;
  setCurrentModal: (newModal: string) => void;
  closeCurrentModal: () => void;
};

export const ModalStateContext = createContext<ModalStateContextType>({
  modalId: null,
  setCurrentModal: null,
  closeCurrentModal: null,
});

export const useSetCurrentModal = () => {
  const { setCurrentModal } = useContext(ModalStateContext);
  return (newModal: string) => setCurrentModal(newModal);
};

export const useModal = () => {
  const modalState = useContext(ModalStateContext);
  return modalState;
};
