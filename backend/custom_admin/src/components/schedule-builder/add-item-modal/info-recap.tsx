import { Fragment } from "react";

type Props = {
  info: {
    label: string;
    value: string;
  }[];
};

export const InfoRecap = ({ info }: Props) => {
  return (
    <div className="my-3 grid grid-cols-[100px_1fr]">
      {info.map(({ label, value }) => (
        <Fragment key={label}>
          <strong>{label}</strong>
          <span>{value}</span>
        </Fragment>
      ))}
    </div>
  );
};
