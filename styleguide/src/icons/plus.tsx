import * as React from "react";

export const PlusIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={32} height={32} fill="none" viewBox="0 0 32 32" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M15 17.5V30h3V17.5h12v-3H18V2h-3v12.5H2v3h13z"
        fill="#0E1116"
      />
    </svg>
  );
};
