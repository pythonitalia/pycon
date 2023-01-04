import { Heading } from "@python-italia/pycon-styleguide";
import { CloseIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import React, { useEffect } from "react";

type ModalProps = {
  title: string | React.ReactNode;
  show: boolean;
  onClose: () => void;
  children: React.ReactNode;
  actions: React.ReactNode;
};

export const Modal = ({
  title,
  show = false,
  onClose,
  children,
  actions,
}: ModalProps) => {
  useEffect(() => {
    if (show) {
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [show]);

  return (
    <div
      className={clsx(
        "fixed overflow-y-auto inset-0 z-[2050] flex items-center justify-center",
        {
          block: show,
          hidden: !show,
        },
      )}
      role="dialog"
    >
      <div className="fixed inset-0 bg-caramel/90" onClick={onClose}></div>
      <div className="px-4 z-10 w-full max-w-3xl">
        <div className="border border-black divide-y">
          <div className="bg-coral px-6 py-8 flex justify-between">
            <Heading size={3}>{title}</Heading>
            <div onClick={onClose} className="cursor-pointer">
              <CloseIcon />
            </div>
          </div>
          <div className="bg-milk px-6 py-8 max-h-[400px] overflow-x-scroll">
            {children}
          </div>
          {actions && <div className="bg-milk px-6 py-4">{actions}</div>}
        </div>
      </div>
    </div>
  );
};
