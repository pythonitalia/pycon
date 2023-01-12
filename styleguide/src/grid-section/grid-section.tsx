import React from "react";
import { Heading } from "../heading";
import { Container } from "../container";
import { Spacer } from "../spacer";
import { SnakeHead } from "../illustrations/snake-head";
import { Grid } from "../grid";
import { GridCols } from "../grid/grid";

type Props = React.PropsWithChildren<{
  title?: string | React.ReactNode;
  cols: GridCols;
  showSnake?: boolean;
}>;

export const GridSection = ({
  title,
  cols,
  children,
  showSnake = false,
}: Props) => {
  return (
    <div>
      <Container>
        <Spacer size="xl" />

        {title && (
          <>
            <Heading size={1}>{title}</Heading>
            <Spacer
              showOnlyOn={showSnake ? "mobile" : undefined}
              size="large"
            />
          </>
        )}

        {showSnake && (
          <SnakeHead className="relative ml-auto w-32 lg:w-52 mr-6 md:mr-12 -mt-36 md:-mt-24 lg:-mt-44 hidden md:block" />
        )}

        <Grid cols={cols} gap="medium">
          {children}
        </Grid>
      </Container>
    </div>
  );
};
