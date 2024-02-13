import { createContext, useContext, useMemo, useState } from "react";

import { AddItemModal } from ".";
import type { Day, Room, Slot } from "../../../types";

type Props = {
  children: React.ReactNode;
};

type AddItemModalContextProps = {
  isOpen: boolean;
  open: ({ slot, room }: { slot: Slot; room: Room; day: Day }) => void;
  close: () => void;
  data: { slot: Slot; room: Room; day: Day } | null;
};

const AddItemModalContext = createContext<AddItemModalContextProps>({
  isOpen: false,
  open: ({ slot, room, day }) => {},
  close: () => {},
  data: null,
});

export const AddItemModalProvider = ({ children }: Props) => {
  const [openData, setOpenData] = useState(null);

  const open = ({ slot, room, day }) => {
    setOpenData({ slot, room, day });
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
