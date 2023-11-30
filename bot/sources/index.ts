import { Client } from "discord.js";
import { ready } from "./events/ready.event.js";
import { pino } from "pino";
import "dotenv/config";

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
client.configuration = {
  applicationId: "1151189706038579290",
  guildId: "1010816890513395803",
  collectingMin: 5,
  collectingMax: 50,
};

client.once("ready", ready);

client.login(process.env.TOKEN);
