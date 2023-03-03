import * as React from "react";

export const GearIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" {...props}>
      <path
        d="M11.552 16.793L9.586 20.07 5 21.379v5.242l4.586.655 1.966 3.93-2.621 4.587 3.931 3.276 3.931-1.966 3.276 1.966 1.31 4.586h5.242l1.31-4.586 3.931-1.966 3.931 1.966 3.276-3.931-1.966-3.931 1.31-3.276L43 26.621v-5.242l-4.586-1.31-1.31-3.931 1.965-3.931-3.276-3.276-3.93 2.62-3.932-1.965L27.276 5h-5.897l-1.31 4.586-3.276 1.31-3.93-1.965-3.932 3.931 2.62 3.931z"
        stroke="#0E1116"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <circle cx={24.002} cy={24} r={7.017} stroke="#0E1116" strokeWidth={3} />
    </svg>
  );
};
