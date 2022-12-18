import React from "react";
import { Heading } from "../heading";
import { Container } from "../container";
import { Spacer } from "../spacer";
import clsx from "clsx";

type Props = React.PropsWithChildren<{
  title?: string | React.ReactNode;
  cols: number;
}>;

export const GridSection = ({ title, cols, children }: Props) => {
  return (
    <div>
      <Container>
        <Spacer size="xl" />

        {title && (
          <>
            <Heading size={1}>{title}</Heading>
            <Spacer size="large" />
          </>
        )}

        <div
          className={clsx("grid gap-2 lg:gap-6", {
            "lg:grid-cols-1": cols === 1,
            "lg:grid-cols-2": cols === 2,
            "lg:grid-cols-3": cols === 3,
            "lg:grid-cols-4": cols === 4,
            "lg:grid-cols-5": cols === 5,
            "lg:grid-cols-6": cols === 6,
            "lg:grid-cols-7": cols === 7,
          })}
        >
          {children}
        </div>
      </Container>
    </div>
  );
};
