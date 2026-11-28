import * as React from "react";

export const HotelIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" {...props}>
      <path stroke="#0E1116" strokeWidth={3} d="M16.5 8.5h16v31h-16z" />

      <path
        stroke="#0E1116"
        strokeWidth={3}
        d="M2 39.5h44M7.5 18.5h33v21h-33z"
      />
    </svg>
  );
};
