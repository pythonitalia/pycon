import { atom, useRecoilState } from "recoil";

const drawerOpen = atom({
  key: "drawerOpen",
  default: true,
});

export const useDrawer = () => {
  const [isOpen, setOpen] = useRecoilState(drawerOpen);
  return {
    open: isOpen,
    openDrawer: () => setOpen(true),
    closeDrawer: () => setOpen(false),
  };
};
