import * as React from "react";

export const LiveIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={65} height={22} fill="none" {...props}>
      <rect
        x={0.844}
        y={0.074}
        width={63.928}
        height={21}
        rx={10.5}
        fill="#D75353"
      />
      <circle cx={16.308} cy={10.074} r={2.55} fill="#fff" />
      <circle opacity={0.5} cx={16.308} cy={10.074} r={4.964} stroke="#fff" />
      <path
        d="M34.442 15.074h-5.655V5.74h1.43v8.047h4.225v1.287zm2.834 0h-1.43V5.74h1.43v9.334zm9.641-9.334l-3.432 9.334h-1.573L38.48 5.74h1.534l2.717 7.67 2.756-7.67h1.43zm7.133 8.086v1.248h-5.915V5.74h5.824v1.248h-4.394V9.64h4.004v1.248h-4.004v2.938h4.485z"
        fill="#fff"
      />
    </svg>
  );
};
