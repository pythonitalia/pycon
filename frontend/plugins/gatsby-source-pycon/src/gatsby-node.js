const uuidv4 = require(`uuid/v4`);
const { buildSchema, printSchema } = require(`gatsby/graphql`);
const {
  makeRemoteExecutableSchema,
  transformSchema,
  introspectSchema,
  RenameTypes,
} = require(`graphql-tools`);
const { createHttpLink } = require(`apollo-link-http`);
const fetch = require(`node-fetch`);
const invariant = require(`invariant`);

const {
  NamespaceUnderFieldTransform,
  StripNonQueryTransform,
  RemoveConferenceArgument,
} = require(`./transforms`);

exports.sourceNodes = async (
  { actions, createNodeId, cache, createContentDigest },
  options,
) => {
  const { addThirdPartySchema, createNode } = actions;
  const {
    url,
    typeName,
    fieldName,
    conferenceCode,
    headers = {},
    fetchOptions = {},
    createSchema,
    refetchInterval,
  } = options;

  const link = createHttpLink({
    uri: url,
    fetch,
    headers,
    fetchOptions,
  });

  let introspectionSchema;

  if (createSchema) {
    introspectionSchema = await createSchema(options);
  } else {
    const cacheKey = `gatsby-source-graphql-schema-${typeName}-${fieldName}`;
    let sdl = await cache.get(cacheKey);

    if (!sdl) {
      introspectionSchema = await introspectSchema(link);
      sdl = printSchema(introspectionSchema);
    } else {
      introspectionSchema = buildSchema(sdl);
    }

    await cache.set(cacheKey, sdl);
  }

  const remoteSchema = makeRemoteExecutableSchema({
    schema: introspectionSchema,
    link,
  });

  const nodeId = createNodeId(`gatsby-source-graphql-${typeName}`);
  const node = createSchemaNode({
    id: nodeId,
    typeName,
    fieldName,
    createContentDigest,
  });
  createNode(node);

  const resolver = (parent, args, context) => {
    context.nodeModel.createPageDependency({
      path: context.path,
      nodeId: nodeId,
    });
    return {};
  };

  const schema = transformSchema(remoteSchema, [
    new StripNonQueryTransform(),
    new RemoveConferenceArgument(conferenceCode),
    new RenameTypes(name => `${typeName}_${name}`),
    new NamespaceUnderFieldTransform({
      typeName,
      fieldName,
      resolver,
    }),
  ]);

  addThirdPartySchema({ schema });

  if (process.env.NODE_ENV !== `production`) {
    if (refetchInterval) {
      const msRefetchInterval = refetchInterval * 1000;
      const refetcher = () => {
        createNode(
          createSchemaNode({
            id: nodeId,
            typeName,
            fieldName,
            createContentDigest,
          }),
        );
        setTimeout(refetcher, msRefetchInterval);
      };
      setTimeout(refetcher, msRefetchInterval);
    }
  }
};

function createSchemaNode({ id, typeName, fieldName, createContentDigest }) {
  const nodeContent = uuidv4();
  const nodeContentDigest = createContentDigest(nodeContent);
  return {
    id,
    typeName: typeName,
    fieldName: fieldName,
    parent: null,
    children: [],
    internal: {
      type: `GraphQLSource`,
      contentDigest: nodeContentDigest,
      ignoreType: true,
    },
  };
}
