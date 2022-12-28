import React from "react";
import { Container } from "../container";
import { ContainerSize } from "../container/container";
import { Spacer } from "../spacer";

type Props = {
  children: React.ReactNode;
  containerSize?: ContainerSize;
};

export const Section = ({ children, containerSize = "base" }: Props) => {
  return (
    <div>
      <Container size={containerSize}>
        <Spacer size="xl" />
        {children}
        <Spacer size="xl" />
      </Container>
    </div>
  );
};
