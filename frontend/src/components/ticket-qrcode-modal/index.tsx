import QRCode from "react-qr-code";

import { Modal } from "../modal";

type Props = {
  onClose: () => void;
};

export type TicketQRCodeModalProps = {
  qrCodeValue: string;
};

export const TicketQRCodeModal = ({
  onClose,
  qrCodeValue,
}: Props & TicketQRCodeModalProps) => {
  return (
    <Modal title="QR Code" show={true} onClose={onClose}>
      <QRCode value={qrCodeValue} bgColor="none" />
    </Modal>
  );
};
