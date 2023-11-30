import { Command } from "./command.js";
import { Database } from "../modules/database.ts";
import { CustomEmoji } from "./customEmoji.js";
import { Logger } from "pino";
import { Configuration } from "./configuration.js";

declare module "discord.js" {
  export interface Client {
    commands: Command[];
    logger: Logger;
    database: Database;
    customEmoji: CustomEmoji;
    configuration: Configuration;
  }
}
