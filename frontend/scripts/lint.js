// Simple script to run eslint via precommit and fix the
// path of the js files to not have frontend/ in the path

const CLIEngine = require("eslint").CLIEngine;

const cli = new CLIEngine();

const filesToLint = process.argv
    .slice(2)
    .map(path => path.replace(/^frontend\//, ""));

const report = cli.executeOnFiles(filesToLint);

const formatter = cli.getFormatter();

console.log(formatter(report.results));

if (report.errorCount) {
    process.exit(1);
}
