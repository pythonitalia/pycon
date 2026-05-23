import React, { useContext } from "react";

type MultiPartsCardContextType = {
  clickablePart?: string;
  expandTarget?: string;
  open: boolean;
  toggleOpen?: React.Dispatch<React.SetStateAction<boolean>>;
  isClickablePart: (id?: string) => boolean;
  isTargetPart: (id?: string) => boolean;
};

export const MultiPartsCardContext =
  React.createContext<MultiPartsCardContextType>({
    open: false,
    isClickablePart: () => false,
    isTargetPart: () => false,
  });

export const useMultiPartsCardContext = () => useContext(MultiPartsCardContext);
