using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class ActionsApplicationCommandModule
    {
        [SlashCommand("обнять", "Обнять пользователя")]
        public async Task HugSlashCommand(InteractionContext interactionContext)
        {
            await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
        }
    }
}
