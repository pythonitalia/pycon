import { RecoilRoot } from "recoil";

import { Drawer } from "~/components/drawer";

import "tailwindcss/tailwind.css";

const App = ({ Component, pageProps }) => (
  <RecoilRoot>
    <div className="h-screen w-screen flex overflow-hidden bg-white">
      <Drawer />
      <Component {...pageProps} />
    </div>
  </RecoilRoot>
);

export default App;
