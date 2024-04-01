import "@sapphire/plugin-api/register";
import SapphireClient from "@svcs/SapphireClient";

new SapphireClient().login(process.env.TOKEN);
