using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class CommonApplicationCommandModule
    {
        partial class ReputationApplicationCommandModule
        {
            [SlashCommand("убрать", "Убрать репутацию пользователю")]
            public async Task RemoveSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
