import { isEmpty } from "./is-empty.js";

type StringEncodable =
  | {
      toString(): string;
    }
  | string;

export function multilineTrim(
  strings: TemplateStringsArray,
  ...values: StringEncodable[]
): string {
  let text = "";

  for (let i = 0; i < strings.length; i++) {
    text += strings[i].replace(/\\`/g, "`");
    if (i < values.length) {
      text += values[i];
    }
  }

  const lines = text.split("\n");

  const minIndentation = lines
    .filter((line) => line.trim().length > 0)
    .map((line) => (isEmpty(line) && line.match(/^\s*/)?.[0].length) || 0)
    .reduce((min, indentation) => Math.min(min, indentation), Infinity);

  const outputLines = lines.map((line) => line.slice(minIndentation));

  return outputLines.join("\n");
}
