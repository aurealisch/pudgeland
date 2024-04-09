import "@sapphire/plugin-api/register";
import SapphireClient from "./modules/SapphireClient";

new SapphireClient().login(process.env.TOKEN);
