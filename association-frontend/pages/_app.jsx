import Footer from "~/components/footer/footer";
import Header from "~/components/header/header";

import "styles/globals.css";
import "tailwindcss/tailwind.css";

const MyApp = ({ Component, pageProps }) => {
  return (
    <div>
      <Header />
      <main>
        <Component {...pageProps} />
      </main>
      <Footer />
    </div>
  );
};

export default MyApp;
