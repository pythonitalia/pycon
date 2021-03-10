import { ReactElement } from "react";

import { BackIcon } from "../back-icon";
import { Heading } from "../heading";

type Props = {
  headingContent: ReactElement | string;
  backTo?: string;
};

export const PageHeader: React.FC<Props> = ({
  headingContent,
  children,
  backTo,
}) => (
  <div className="border-b border-gray-200 px-6 py-4">
    <div className="flex items-center flex-row min-w-0">
      {backTo && <BackIcon to={backTo} />}
      <Heading>{headingContent}</Heading>
    </div>
    {children}
  </div>
);
