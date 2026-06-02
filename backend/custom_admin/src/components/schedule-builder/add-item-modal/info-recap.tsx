import { DataList } from "@radix-ui/themes";

type Props = {
  info: {
    label: string;
    value: string;
  }[];
};

export const InfoRecap = ({ info }: Props) => {
  return (
    <DataList.Root my="3" size="2">
      {info.map(({ label, value }) => (
        <DataList.Item key={label}>
          <DataList.Label minWidth="100px">{label}</DataList.Label>
          <DataList.Value>{value}</DataList.Value>
        </DataList.Item>
      ))}
    </DataList.Root>
  );
};
