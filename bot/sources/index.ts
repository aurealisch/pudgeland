import { Client } from "discord.js";
import { ready } from "./events/ready.event.js";
import { configuration } from "../configuration.js";
import { pino } from "pino";

let client = new Client({
  intents: [
    "GuildBans",
    "GuildEmojisAndStickers",
    "GuildIntegrations",
    "GuildInvites",
    "GuildMembers",
    "GuildMessageReactions",
    "GuildMessageTyping",
    "GuildMessages",
    "GuildModeration",
    "GuildPresences",
    "GuildScheduledEvents",
    "GuildVoiceStates",
    "GuildWebhooks",
    "Guilds",
  ],
});
client.logger = pino();
client.customEmoji = {
  banana: "<:banana:1172161691686031430>",
  monkey: "<:monkey:1171112299621253208>",
  coin: "<:coin:1167478859474685982>",
  diamond: "<:diamond:1147867834114904156>",
  netherite: "<:netherite:1165365535119249559>",
  profile: "<:profile:1166736007027245086>",
};
client.applicationId = configuration.applicationId;
client.guildId = configuration.guildId;

client.once("ready", ready);

client.login(configuration.token);
