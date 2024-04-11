declare module "bun" {
  interface Env {
    PORT: number;
    API_URL: string;
    REDIS_URL: string;
  }
}
