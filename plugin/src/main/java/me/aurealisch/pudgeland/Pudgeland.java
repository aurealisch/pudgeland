package me.aurealisch.pudgeland;

import me.aurealisch.pudgeland.commandExecutors.ConnectCommandExecutor;
import me.aurealisch.pudgeland.commandExecutors.DisconnectCommandExecutor;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.Objects;

@SuppressWarnings("unused")
public final class Pudgeland extends JavaPlugin {
    @Override
    public void onEnable() {
        // Plugin startup logic
        getLogger().info("Hello, World!");

        Objects.requireNonNull(getCommand("connect")).setExecutor(new ConnectCommandExecutor());
        Objects.requireNonNull(getCommand("disconnect")).setExecutor(new DisconnectCommandExecutor());
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
        getLogger().info("Goodbye, World!");
    }
}
