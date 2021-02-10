import { ArrowLeftOutline } from "heroicons-react";

import { useRouter } from "next/router";

type Props = {
  to: string;
};

export const BackIcon: React.FC<Props> = ({ to }) => {
  const { push } = useRouter();
  return (
    <ArrowLeftOutline
      size={21}
      onClick={() => push(to)}
      className="mr-3 cursor-pointer"
    />
  );
};
