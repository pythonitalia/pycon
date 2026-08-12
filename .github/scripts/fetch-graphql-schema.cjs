const { writeFile } = require("node:fs/promises");
const {
  buildClientSchema,
  getIntrospectionQuery,
  printSchema,
} = require("graphql");

const [endpoint, output] = process.argv.slice(2);

if (!endpoint || !output) {
  throw new Error("Usage: fetch-graphql-schema.cjs <endpoint> <output>");
}

async function main() {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: getIntrospectionQuery({
        directiveIsRepeatable: true,
        inputValueDeprecation: true,
        oneOf: true,
        schemaDescription: true,
        specifiedByUrl: true,
      }),
    }),
  });
  const body = await response.text();

  if (!response.ok) {
    throw new Error(`${response.status} ${body}`);
  }

  const result = JSON.parse(body);

  if (result.errors?.length) {
    throw new Error(JSON.stringify(result.errors));
  }

  await writeFile(output, printSchema(buildClientSchema(result.data)));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
