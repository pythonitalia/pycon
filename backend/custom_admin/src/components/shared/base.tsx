import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

type Props = {
  children: React.ReactNode;
};

const client = new ApolloClient({
  uri: (window as any).apolloGraphQLUrl,
  cache: new InMemoryCache(),
});

export const Base = ({ children }: Props) => {
  return (
    <ApolloProvider client={client}>
      <DndProvider backend={HTML5Backend}>{children}</DndProvider>
    </ApolloProvider>
  );
};
