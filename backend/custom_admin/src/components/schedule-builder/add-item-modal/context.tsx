import { createContext, useContext, useMemo, useState } from "react";

import { AddItemModal } from ".";
import type { Room, Slot } from "../../../types";

type Props = {
  children: React.ReactNode;
};

type AddItemModalContextProps = {
  isOpen: boolean;
  open: ({ slot, room }: { slot: Slot; room: Room }) => void;
  close: () => void;
  data: { slot: Slot; room: Room } | null;
};

const AddItemModalContext = createContext<AddItemModalContextProps>({
  isOpen: false,
  open: ({ slot, room }) => {},
  close: () => {},
  data: null,
});

export const AddItemModalProvider = ({ children }: Props) => {
  const [openData, setOpenData] = useState(null);

  const open = ({ slot, room }) => {
    setOpenData({ slot, room });
  };

  const close = () => {
    setOpenData(null);
  };

  const state = useMemo(
    () => ({ isOpen: !!openData, open, close, data: openData }),
    [openData],
  );

  return (
    <AddItemModalContext.Provider value={state}>
      <AddItemModal />
      {children}
    </AddItemModalContext.Provider>
  );
};

export const useAddItemModal = () => {
  return useContext(AddItemModalContext);
};
