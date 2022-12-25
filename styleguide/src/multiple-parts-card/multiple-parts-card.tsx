import React, { useState } from "react";
import { Spacer } from "../spacer";
import { Button } from "../button";
import { MultiPartsCardContext } from "./context";

type CTA = {
  label: string | React.ReactNode;
  link: string;
};

type Props = {
  cta?: CTA;
  expand?: string;
  children: React.ReactNode;
  clickablePart?: string;
  expandTarget?: string;
  openByDefault?: boolean;
};

export const MultiplePartsCard = ({
  children,
  clickablePart,
  expandTarget,
  cta,
  openByDefault = true,
}: Props) => {
  const isMatchingId = (id?: string, target?: string) => {
    if (!target || !id) {
      return false;
    }

    return target === id;
  };
  const [open, toggleOpen] = useState(openByDefault);

  return (
    <MultiPartsCardContext.Provider
      value={{
        clickablePart,
        expandTarget,
        open,
        toggleOpen,
        isClickablePart: (id) => isMatchingId(id, clickablePart),
        isTargetPart: (id) => isMatchingId(id, expandTarget),
      }}
    >
      <div className="flex flex-col h-full">
        <div className="text-center border bg-cream border-black divide-y-3 h-full flex flex-col justify-between">
          {children}
        </div>

        {cta && (
          <>
            <Spacer size="xs" />

            <Button size="small" fullWidth linkTo={cta.link}>
              {cta.label}
            </Button>
          </>
        )}
      </div>
    </MultiPartsCardContext.Provider>
  );
};
