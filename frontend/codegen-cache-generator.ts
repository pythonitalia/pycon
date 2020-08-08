// @ts-ignore
module.exports = {
  plugin: (schema, documents, config) => {
    const definitionsAllowed = config.definitions;
    let definitionsCode = [];

    for (const doc of documents) {
      definitionsCode = definitionsCode.concat(
        doc.document.definitions.map((definition) => {
          if (definitionsAllowed.indexOf(definition.name.value) === -1) {
            return;
          }

          return writeCode(definition);
        }),
      );
    }

    return definitionsCode.join("");
  },
};

const writeCode = (definition) => {
  const definitionName = definition.name.value;
  const documentName = `${definitionName}Document`;
  const variablesTypes = `${definitionName}QueryVariables`;
  const queryType = `${definitionName}Query`;
  const funcPostfix = `${definitionName}QueryCache`;

  const writeOptionsTypeName = `${funcPostfix}WriteOptions`;
  const readOptionsTypeName = `${funcPostfix}ReadOptions`;

  return `
  type ${readOptionsTypeName}<TMutation> = {
    cache: Apollo.ApolloCache<TMutation>;
    variables: ${variablesTypes};
  }

  type ${writeOptionsTypeName}<TMutation> = {
    cache: Apollo.ApolloCache<TMutation>;
    variables: ${variablesTypes};
    data: ${queryType};
  }

  export function read${funcPostfix}<TMutation>(options: ${readOptionsTypeName}<TMutation>) {
    return options.cache.readQuery<${queryType}, ${variablesTypes}>({
      query: ${documentName},
      variables: options.variables,
    })
  }

  export function write${funcPostfix}<TMutation>(options: ${writeOptionsTypeName}<TMutation>) {
    return options.cache.writeQuery<${queryType}, ${variablesTypes}>({
      query: ${documentName},
      variables: options.variables,
      data: options.data,
    })
  }
`;
};
