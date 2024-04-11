package me.aurealisch.pudgeland.commandExecutors;

import me.aurealisch.pudgeland.Pudgeland;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

public class ConnectCommandExecutor implements CommandExecutor {
    private final Pudgeland pudgeland;

    public ConnectCommandExecutor(Pudgeland pudgeland) {
        this.pudgeland = pudgeland;
    }

    @Override
    public boolean onCommand(@NotNull CommandSender commandSender, @NotNull Command command, @NotNull String label, String[] arguments) {
        if (!(commandSender instanceof Player)) return false;

        Player player = (Player) commandSender;

        if (arguments.length != 1) return false;

        String id = arguments[0];

        player.sendMessage(id);

        return true;
    }
}
