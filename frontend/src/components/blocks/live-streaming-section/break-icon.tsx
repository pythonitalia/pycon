import clsx from "clsx";

export const BreakIcon = ({ className }: { className: string }) => (
  <div
    className={clsx(
      "w-[65px] h-[21px] bg-purple rounded-full text-[12px] font-medium text-white flex items-center justify-center uppercase",
      className,
    )}
  >
    Break
  </div>
);
