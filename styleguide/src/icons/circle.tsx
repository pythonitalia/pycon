import * as React from "react";

export const CircleIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" {...props}>
      <circle cx={24} cy={24} r={14.5} stroke="#0E1116" strokeWidth={3} />
    </svg>
  );
};
