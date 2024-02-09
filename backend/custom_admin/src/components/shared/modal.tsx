import clsx from "clsx";
import { useEffect } from "react";

type Props = {
  onClose: () => void;
  children: React.ReactNode;
  className?: string;
  isOpen: boolean;
};

export const Modal = ({ isOpen, onClose, children, className }: Props) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [isOpen]);

  return (
    <div>
      <div
        className="fixed top-0 left-0 w-full h-full bg-black/50 z-[500]"
        onClick={onClose}
      />
      <div
        className={clsx(
          "fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[1000] bg-white",
          className,
        )}
      >
        {children}
      </div>
    </div>
  );
};
