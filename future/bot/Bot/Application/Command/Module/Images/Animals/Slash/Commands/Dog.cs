using DSharpPlus.SlashCommands;
using DSharpPlus.Entities;

namespace Bot
{
    partial class ImagesApplicationCommandModule
    {
        partial class AnimalsApplicationCommandModule
        {
            [SlashCommand("собака", "Случайное изображение собаки")]
            public async Task DogSlashCommand(InteractionContext interactionContext)
            {
                await interactionContext.CreateResponseAsync(DSharpPlus.InteractionResponseType.ChannelMessageWithSource, new DiscordInteractionResponseBuilder().WithContent("Hello, World!"));
            }
        }
    }
}
