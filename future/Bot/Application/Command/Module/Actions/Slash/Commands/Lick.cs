using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class ActionsApplicationCommandModule
    {
        [SlashCommand("лизнуть", "Лизнуть пользователя")]
        public async Task LickSlashCommand(InteractionContext interactionContext)
        {
            await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
        }
    }
}
