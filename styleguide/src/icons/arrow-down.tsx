import * as React from "react";

export const ArrowDownIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={20} height={12} fill="none" viewBox="0 0 20 12" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M19.878 2.16l-9 9-.707.707-.707-.707-9-9L1.878.746l8.293 8.293L18.464.746l1.414 1.414z"
        fill="#0E1116"
      />
    </svg>
  );
};
