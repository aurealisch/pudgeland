import "@sapphire/plugin-api/register";
import SapphireClient from "@services/SapphireClient";

new SapphireClient().login(process.env.TOKEN);
