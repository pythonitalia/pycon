import "styles/globals.css";
import "tailwindcss/tailwind.css";
import Footer from "~/components/footer/footer";
import Header from "~/components/header/header";

const MyApp = ({ Component, pageProps }) => {
  return (
    <div>
      <div className="bg-white">
        <Header />
        <main>
          <Component {...pageProps} />
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default MyApp;
