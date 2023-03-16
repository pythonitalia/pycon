import { SectionItem } from "~/components/section-item";

export const SectionCertification = () => {
  return (
    <SectionItem
      title={"Attestato Validazione Corso di Studi 🐍"}
      withBackground={true}
      overlay={false}
      textTheme={"black"}
      backgroundImageClass={"bg-white-background"}
    >
      <p className="mx-auto mb-4 text-xl text-black">
        I corsi elencati in questa pagina sono offerti da Enti Scolastici,
        pubblici o privati, che ci hanno volontariamente sottoposto il relativo
        programma di studi.
      </p>
      <p className="mx-auto mb-4 text-xl text-black">
        L'Associazione, a titolo assolutamente gratuito, li ha visionati e
        ritenuti meritevoli di apparire in questa pagina, in quanto adeguati dal
        punto di vista qualitativo dei contenuti e quantitativo delle ore di
        insegnamento.
      </p>
      <ul className="mb-4">
        <li>
          <a
            className="underline text-xl"
            rel="noopener"
            target="_blank"
            href="https://example.com"
          >
            Nome instituto qui
          </a>
        </li>
      </ul>
      <p className="mx-auto mb-4 text-xl text-black">
        L'attestato consente all'Ente di definire il proprio programma di studi
        come “Approvato da Python Italia” e di mostrare il logo
        dell'Associazione sui propri canali di comunicazione. L'attestato ha
        validità di un anno e viene prorogato automaticamente nel caso il
        programma didattico resti idoneo ai requisiti dell'Associazione.
      </p>
    </SectionItem>
  );
};
