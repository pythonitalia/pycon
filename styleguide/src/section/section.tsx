import React from "react";
import { Container } from "../container";
import { Spacer } from "../spacer";

type Props = React.PropsWithChildren<{}>;

export const Section = ({ children }: Props) => {
  return (
    <div>
      <Container>
        <Spacer size="xl" />
        {children}
        <Spacer size="xl" />
      </Container>
    </div>
  );
};
