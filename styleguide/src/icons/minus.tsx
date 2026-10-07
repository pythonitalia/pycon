import * as React from "react";

export const MinusIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={32} height={32} viewBox="0 0 32 32" fill="none" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M30 17.5H2v-3h28v3z"
        fill="#0E1116"
      />
    </svg>
  );
};
