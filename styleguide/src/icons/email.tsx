import * as React from "react";

export const EmailIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" {...props}>
      <path
        d="M44 9L24 23 4 9"
        stroke="#0E1116"
        strokeWidth={3}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <mask id="prefix__a" fill="#fff">
        <rect x={2} y={6} width={44} height={35.2} rx={1} />
      </mask>
      <rect
        x={2}
        y={6}
        width={44}
        height={35.2}
        rx={1}
        stroke="#0E1116"
        strokeWidth={6}
        strokeLinejoin="round"
        mask="url(#prefix__a)"
      />
    </svg>
  );
};
