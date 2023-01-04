import * as React from "react";

const ArrowIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={32} height={32} viewBox="0 0 32 32" fill="none" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M24.87 15l-7.034-6.253 1.328-1.495 9 8 .841.747-.84.748-9 8-1.33-1.495 7.035-6.253H4v-2h20.87z"
        fill="#0E1116"
      />
    </svg>
  );
};

export default ArrowIcon;
