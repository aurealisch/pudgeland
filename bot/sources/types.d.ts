declare module "bun" {
  interface Env {
    TOKEN: string;
    ADDRESS: string;
    PORT: number;
    POSTGRES_HOSTNAME: string;
    POSTGRES_PORT: number;
    POSTGRES_DATABASE: string;
    POSTGRES_USERNAME: string;
    POSTGRES_PASSWORD: string;
    ENVIRONMENT: "production" | "development";
  }
}
