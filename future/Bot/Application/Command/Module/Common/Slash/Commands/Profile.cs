using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class CommonApplicationCommandModule
    {
        [SlashCommand("профиль", "Профиль")]
        public async Task ProfileSlashCommand(InteractionContext interactionContext)
        {
            await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
        }
    }
}
