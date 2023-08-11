using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class CommonApplicationCommandModule
    {
        partial class LeadersApplicationCommandModule
        {
            [SlashCommand("обезьяны", "Лидеры по обезьянам")]
            public async Task MonkeysSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
