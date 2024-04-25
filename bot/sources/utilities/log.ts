import { container } from "@sapphire/framework";

export default function log(text: string) {
  return function (
    target: any,
    propertyKey: string,
    propertyDescriptor: PropertyDescriptor
  ) {
    if (process.env.ENVIRONMENT === "development") {
      container.logger.info(text);
    }
  };
}
