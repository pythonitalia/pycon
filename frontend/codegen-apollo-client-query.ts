// @ts-ignore
module.exports = {
  plugin: (schema, documents, config) => {
    let definitionsCode = [];

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
export async function query${codeFriendlyName}(variables?: ${definitionName}QueryVariables): Promise<${definitionName}QueryResult> {
  const client = getApolloClient();
  // @ts-ignore
  return client.query({
    query: ${definitionName}Document,
    variables,
  });
}

`;
};
