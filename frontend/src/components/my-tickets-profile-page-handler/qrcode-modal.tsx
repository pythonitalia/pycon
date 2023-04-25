import QRCode from "react-qr-code";

import { Modal } from "../modal";

type Props = {
  open: boolean;
  openModal: (open: boolean) => void;
  qrCodeValue: string;
};
export const QRCodeModal = ({ open, openModal, qrCodeValue }: Props) => {
  return (
    <Modal title="QR Code" show={open} onClose={() => openModal(false)}>
      <QRCode value={qrCodeValue} bgColor="none" />
    </Modal>
  );
};
