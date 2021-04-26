import React, { ReactNode } from "react";

import { Modal } from "~/components/modal";

type Props = {
  title: string;
  showModal: boolean;
  children: ReactNode;
  closeModal: () => void;
};

export const SimpleModal = ({
  title,
  children,
  showModal,
  closeModal,
}: Props) => (
  <Modal
    className="items-center"
    showModal={showModal}
    closeModalHandler={closeModal}
    title={title}
  >
    {children}
  </Modal>
);
