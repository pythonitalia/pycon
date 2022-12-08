// @ts-ignore
module.exports = {
  plugin: (schema, documents, config) => {
    let definitionsCode = [];
    console.warn("Hello Vercel. API_URL_SERVER: ", process.env.API_URL_SERVER);

    for (const doc of documents) {
      definitionsCode = definitionsCode.concat(
        doc.document.definitions
          .filter((definition) => definition.operation === "query")
          .map((definition) => writeApolloClientQuery(definition)),
      );
    }

    return definitionsCode.join("");
  },
};

const writeApolloClientQuery = (definition) => {
  const definitionName = definition.name.value;
  const codeFriendlyName = `${definitionName[0].toUpperCase()}${definitionName.slice(
    1,
  )}`;

  return `
export async function query${codeFriendlyName}(client: ApolloClient<any>, variables?: ${definitionName}QueryVariables): Promise<${definitionName}QueryResult> {
  // @ts-ignore
  return client.query({
    query: ${definitionName}Document,
    variables,
  });
}

`;
};
