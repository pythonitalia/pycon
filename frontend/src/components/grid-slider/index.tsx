/** @jsx jsx */
import { Box, Flex, Grid, Heading } from "@theme-ui/components";
import { useState } from "react";
import { jsx } from "theme-ui";

import { useSSRResponsiveValue } from "../../helpers/use-ssr-responsive-value";
import { ArrowIcon } from "../icons/arrow";

const useSlider = <T extends any>(
  objects: T[],
  perPage: number,
): [T[], () => void, () => void] => {
  const [index, setIndex] = useState(0);

  // TODO: fix the increase to find the last page
  const increase = () =>
    setIndex(Math.min(index + perPage, objects.length - 1));
  const decrease = () => setIndex(Math.max(index - perPage, 0));

  return [objects.slice(index, index + perPage), increase, decrease];
};

const Slider = <T extends { id: string }>({
  page,
  showArrows,
  increase,
  decrease,
  Component,
}: {
  page: T[];
  showArrows: boolean;
  increase: () => void;
  decrease: () => void;
  Component: React.ElementType;
}) => (
  <Grid
    sx={{
      justifyContent: "center",
      gridTemplateColumns: ["1fr", "100px minmax(200px, 1200px) 100px"],
    }}
    gap={0}
  >
    <Flex
      onClick={decrease}
      sx={{
        display: ["none", "flex"],
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {showArrows && <ArrowIcon sx={{ width: 40 }} />}
    </Flex>

    <Grid columns={[1, 2, 3]} gap={0}>
      {page.map(item => (
        <Component key={item.id} {...item} />
      ))}
    </Grid>

    <Flex
      onClick={increase}
      sx={{
        display: ["none", "flex"],
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {showArrows && <ArrowIcon sx={{ width: 40 }} direction="right" />}
    </Flex>
  </Grid>
);

export const GridSlider = <T extends { id: string }>({
  title,
  items,
  Component,
}: {
  title: string | React.ReactElement;
  items: T[];
  Component: React.ElementType;
}) => {
  const columns = useSSRResponsiveValue([1, 2, 3]);
  const showArrows = items.length > columns;
  const [page, increase, decrease] = useSlider(items, columns);

  if (items.length === 0) {
    return null;
  }

  return (
    <Box sx={{ borderBottom: "primary", borderTop: "primary" }}>
      <Box sx={{ borderBottom: "primary", py: 4 }}>
        <Heading
          as="h1"
          sx={{
            px: 3,
            display: "flex",
            maxWidth: "container",
            mx: "auto",
          }}
        >
          {title}
          {showArrows && (
            <Box
              sx={{
                marginLeft: "auto",
                flex: "0 0 60px",
                display: ["block", "none"],
              }}
            >
              <ArrowIcon
                onClick={decrease}
                sx={{ width: 20, height: 20, mr: 2 }}
              />
              <ArrowIcon
                onClick={increase}
                sx={{ width: 20, height: 20 }}
                direction="right"
              />
            </Box>
          )}
        </Heading>
      </Box>

      <Slider
        page={page}
        showArrows={showArrows}
        increase={increase}
        decrease={decrease}
        Component={Component}
      />
    </Box>
  );
};
