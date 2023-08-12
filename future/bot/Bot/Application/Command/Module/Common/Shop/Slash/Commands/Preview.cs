using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class CommonApplicationCommandModule
    {
        partial class ShopApplicationCommandModule
        {
            [SlashCommand("просмотр", "Просмотр магазина предметов")]
            public async Task PreviewSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
