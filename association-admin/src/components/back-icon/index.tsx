import classnames from "classnames";
import { ArrowLeftOutline } from "heroicons-react";

import { useRouter } from "next/router";

type Props = {
  to: string;
  className?: string;
};

export const BackIcon: React.FC<Props> = ({ to, className }) => {
  const { push, back } = useRouter();

  return (
    <ArrowLeftOutline
      size={21}
      onClick={() => {
        if (to === "back") {
          back();
        } else {
          push(to);
        }
      }}
      className={classnames(
        "mr-3 text-gray-700 fill-current cursor-pointer mt-1",
        className,
      )}
    />
  );
};
