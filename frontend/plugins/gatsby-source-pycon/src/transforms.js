const {
  GraphQLObjectType,
  GraphQLNonNull,
  GraphQLString,
  GraphQLSchema,
} = require(`gatsby/graphql`);
const {
  visitSchema,
  VisitSchemaKind,
} = require(`graphql-tools/dist/transforms/visitSchema`);
const {
  createResolveType,
  fieldMapToFieldConfigMap,
} = require(`graphql-tools/dist/stitching/schemaRecreation`);
const fromEntries = require("fromentries");

class NamespaceUnderFieldTransform {
  constructor({ typeName, fieldName, resolver }) {
    this.typeName = typeName;
    this.fieldName = fieldName;
    this.resolver = resolver;
  }

  transformSchema(schema) {
    const query = schema.getQueryType();
    let newQuery;
    const nestedType = new GraphQLObjectType({
      name: this.typeName,
      fields: () =>
        fieldMapToFieldConfigMap(
          query.getFields(),
          createResolveType(typeName => {
            if (typeName === query.name) {
              return newQuery;
            } else {
              return schema.getType(typeName);
            }
          }),
          true,
        ),
    });
    newQuery = new GraphQLObjectType({
      name: query.name,
      fields: {
        [this.fieldName]: {
          type: new GraphQLNonNull(nestedType),
          resolve: (parent, args, context, info) => {
            if (this.resolver) {
              return this.resolver(parent, args, context, info);
            } else {
              return {};
            }
          },
        },
      },
    });
    const typeMap = schema.getTypeMap();
    const allTypes = Object.keys(typeMap)
      .filter(name => name !== query.name)
      .map(key => typeMap[key]);

    return new GraphQLSchema({
      query: newQuery,
      types: allTypes,
    });
  }
}

class StripNonQueryTransform {
  transformSchema(schema) {
    return visitSchema(schema, {
      [VisitSchemaKind.MUTATION]() {
        return null;
      },
      [VisitSchemaKind.SUBSCRIPTION]() {
        return null;
      },
    });
  }
}

class RemoveConferenceArgument {
  constructor(conferenceCode) {
    this.conferenceCode = conferenceCode;
  }

  transformRequest(request) {
    const fields = this.schema.getQueryType().getFields();

    request.document.definitions.map(definition => {
      definition.selectionSet.selections.map(selection => {
        const queryField = fields[selection.name.value];

        if (
          queryField &&
          queryField.args.filter(argument => argument.name == "code").length >=
            1 &&
          selection.arguments.filter(argument => argument.name.value == "code")
            .length == 0
        ) {
          selection.arguments.push({
            kind: "Argument",
            name: {
              kind: "Name",
              value: "code",
            },
            value: {
              kind: "StringValue",
              value: this.conferenceCode,
            },
          });
        }

        return selection;
      });

      return definition;
    });

    return request;
  }
  transformSchema(schema) {
    const conferenceCode = this.conferenceCode;

    const transformedSchema = visitSchema(schema, {
      [VisitSchemaKind.ROOT_OBJECT](type, schema) {
        const fields = fromEntries(
          Object.entries(type.getFields()).map(([key, value]) => [
            key,
            {
              ...value,
              args: value.args.map(argument => {
                if (argument.name === "code") {
                  return {
                    ...argument,
                    defaultValue: conferenceCode,
                    type: GraphQLString,
                  };
                }

                return argument;
              }),
            },
          ]),
        );

        return new GraphQLObjectType({
          name: type.name,
          fields: () =>
            fieldMapToFieldConfigMap(
              fields,
              createResolveType(typeName => schema.getType(typeName)),
              true,
            ),
        });
      },
    });

    this.schema = transformedSchema;

    return transformedSchema;
  }
}

module.exports = {
  NamespaceUnderFieldTransform,
  StripNonQueryTransform,
  RemoveConferenceArgument,
};
