using DSharpPlus;
using DSharpPlus.SlashCommands;

namespace Bot
{
    internal class Program
    {
        private static async Task Main()
        {
            var discordConfiguration = new DiscordConfiguration()
            {
                Token = ""
            };

            var discordClient = new DiscordClient(discordConfiguration);

            var slashCommandsExtension = discordClient.UseSlashCommands();

            slashCommandsExtension.RegisterCommands<ActionsApplicationCommandModule>();
            slashCommandsExtension.RegisterCommands<CommonApplicationCommandModule>();
            slashCommandsExtension.RegisterCommands<EconomicsApplicationCommandModule>();
            slashCommandsExtension.RegisterCommands<ImagesApplicationCommandModule>();

            await discordClient.ConnectAsync();
            await Task.Delay(-1);
        }
    }
}
