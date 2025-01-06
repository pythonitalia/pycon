import { Grid } from "@radix-ui/themes";
import { useLocalData } from "../local-state";
import { MarginInput } from "../margin-input";
import { AlignOptions } from "./align-options";

export const RunningElementsOptions = ({
  pageId,
}: {
  pageId: string;
}) => {
  const { setProperty, getProperties } = useLocalData();
  const position = pageId === "header" ? "top" : "bottom";
  const properties = getProperties(pageId);

  const onChangeAlign = (value: string) => {
    setProperty(pageId, "align", value);
  };

  const onChangeMargin = (value: string) => {
    setProperty(pageId, "margin", value);
  };

  return (
    <Grid columns="2">
      <AlignOptions
        value={properties.align}
        onChange={onChangeAlign}
        position={position}
      />
      <MarginInput value={properties.margin} onChange={onChangeMargin} />
    </Grid>
  );
};
