import React from "react";
import { Spacer } from "../spacer";
import { Button } from "../button";

type CTA = {
  label: string | React.ReactNode;
  link: string;
};

type Props = React.PropsWithChildren<{
  cta?: CTA;
}>;

export const MultiplePartsCard = ({ children, cta }: Props) => {
  return (
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
  );
};
