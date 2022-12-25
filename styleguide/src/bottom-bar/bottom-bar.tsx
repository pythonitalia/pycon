import React from "react";
import { Spacer } from "../spacer";
import { Separator } from "../separator";
import { Container } from "../container";

type Props = {
  children: React.ReactNode;
  action: React.ReactNode;
};

export const BottomBar = ({ children, action }: Props) => {
  return (
    <div className="sticky bottom-0 bg-milk">
      <Container>
        <Spacer size="2md" />
        <div className="grid items-center lg:grid-cols-bottombar lg:gap-16">
          <div>{children}</div>
          <Spacer size="xs" showOnlyOn="mobile" />
          <Spacer size="xs" showOnlyOn="tablet" />
          <div>{action}</div>
        </div>
        <Spacer size="2md" />
      </Container>
      <Separator />
    </div>
  );
};
