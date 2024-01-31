import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";

type Props = {
  children: React.ReactNode;
};

const client = new ApolloClient({
  uri: (window as any).apolloGraphQLUrl,
  cache: new InMemoryCache(),
});

export const Base = ({ children }: Props) => {
  console.log("client", client);
  return <ApolloProvider client={client}>{children}</ApolloProvider>;
};
