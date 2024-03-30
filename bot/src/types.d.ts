import DatabaseService from "./services/Database.js";
import QuestManager from "./services/QuestManager.js";

declare module "discord.js" {
  export interface Client {
    database: DatabaseService;
    questManager: QuestManager;
    mediaChannelId: string;
    memesChannelId: string;
  }
}

declare module "bun" {
  interface Env {
    TOKEN: string;
  }
}
