import { ApolloProvider } from "@apollo/client";
import withApollo from "next-with-apollo";

import { getApolloClient } from "./client";

export default withApollo((props) => getApolloClient(props), {
  render: ({ Page, props }) => {
    console.log("props =>", props, "page", Page);
    return (
      <ApolloProvider client={props.apollo}>
        <Page {...props} />
      </ApolloProvider>
    );
  },
});
