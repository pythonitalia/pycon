import { Heading } from "@python-italia/pycon-styleguide";
import { CloseIcon } from "@python-italia/pycon-styleguide/icons";
import clsx from "clsx";
import React, { useEffect } from "react";

type ModalProps = {
  title: string | React.ReactNode;
  show: boolean;
  onClose: () => void;
  children: React.ReactNode;
  actions?: React.ReactNode;
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
        "fixed overflow-y-auto inset-0 z-[2050] flex items-center justify-center !border-t-0 !border-b-0",
        {
          block: show,
          hidden: !show,
        },
      )}
      role="dialog"
    >
      <div className="fixed inset-0 bg-caramel/90" onClick={onClose}></div>
      <div className="md:px-4 z-10 w-full h-screen md:h-auto md:max-w-3xl">
        <div className="md:border md:border-black divide-y flex flex-col h-screen md:h-auto bg-milk">
          <div className="bg-coral px-4 py-6 md:px-6 md:py-8 flex justify-between items-center">
            <Heading size={3}>{title}</Heading>
            <div
              onClick={onClose}
              className="cursor-pointer w-7 h-7 md:w-10 md:h-10"
            >
              <CloseIcon full />
            </div>
          </div>
          <div className="bg-milk px-4 md:px-6 py-8 max-h-[400px] overflow-x-scroll grow">
            {children}
          </div>
          {actions && (
            <div className="bg-milk px-4 md:px-6 py-4 mt-auto">{actions}</div>
          )}
        </div>
      </div>
    </div>
  );
};
