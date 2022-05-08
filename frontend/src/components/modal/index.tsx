import { useEffect } from "react";
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
  useEffect(() => {
    if (show) {
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [show]);

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
            maxHeight: "container",
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
              alignItems: "right",
              justifyContent: "right",
              maxWidth: "container",
              textAlign: "right",
              m: -1,
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
