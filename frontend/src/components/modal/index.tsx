import { Box } from "theme-ui";

import { Button } from "~/components/button/button";

type ModalProps = {
  show: boolean;
  onClose: () => void;
};

export const Modal: React.FC<ModalProps> = ({
  show = false,
  onClose,
  ...props
}) => {
  return (
    <Box
      sx={
        {
          position: "fixed",
          overflowY: "auto",
          zIndex: "20",
          inset: 0,
          display: show ? "block" : "none",
        } as any
      }
      role="dialog"
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
          paddingX: 4,
        }}
      >
        <Box
          sx={{
            position: "fixed",
            inset: 0,
            transition: "opacity 150ms cubic-bezier(0.4, 0, 0.2, 1)",
            bg: "gray",
            opacity: 0.75,
          }}
          onClick={onClose}
        />

        <Box
          sx={{
            position: "relative",
            width: "100%",
            maxWidth: "container",
            marginX: "auto",
            overflow: "hidden",
            backgroundColor: "white",
            border: "primary",
            zIndex: "50",
            boxShadow:
              "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
          }}
        >
          <Box
            sx={{
              display: "flex",
              position: "fixed",
              alignItems: "right",
              justifyContent: "right",
              width: "80%",
              maxWidth: "container",
              paddingX: 4,
              textAlign: "right",
              border: "1px solid green",
              paddingY: 3,
            }}
          >
            <Button
              variant="plus"
              sx={{
                cursor: "pointer",
              }}
              onClick={onClose}
            >
              x
            </Button>
          </Box>
          <Box sx={{ padding: 3 }}>{props.children}</Box>
        </Box>
      </Box>
    </Box>
  );
};
