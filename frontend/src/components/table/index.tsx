import { Grid, Text } from "@python-italia/pycon-styleguide";
import clsx from "clsx";
import { Fragment } from "react";

type Props<T> = {
  cols: number;
  data: T[];
  rowGetter: (item: T) => any[];
  keyGetter: (item: T) => string;
};

export const Table = <T,>({ data, rowGetter, keyGetter, cols }: Props<T>) => (
  <Grid cols={cols} gap="none">
    {data.map((item, dataIndex) => {
      const row = rowGetter(item);

      return (
        <Fragment key={dataIndex}>
          {row.map((content, itemIndex) => {
            return (
              <div
                key={keyGetter(content)}
                className={clsx(
                  "border-t border-r flex items-center p-4 lg:py-5 lg:px-6",
                  {
                    "border-l mt-2 lg:mt-0": itemIndex === 0,
                    "border-l lg:border-l-0": itemIndex !== 0,
                    "border-b lg:border-b-0": itemIndex === row.length - 1,
                    "lg:border-b last:border-b": dataIndex === data.length - 1,
                  },
                )}
              >
                {content}
              </div>
            );
          })}
        </Fragment>
      );
    })}
  </Grid>
);
