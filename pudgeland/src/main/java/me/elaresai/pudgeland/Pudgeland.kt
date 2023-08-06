package me.elaresai.pudgeland

import me.elaresai.pudgeland.command.executor.ConnectCommandExecutor
import me.elaresai.pudgeland.command.executor.ConvertCommandExecutor
import org.bukkit.plugin.java.JavaPlugin

class Pudgeland : JavaPlugin() {
    override fun onEnable() {
        // Plugin startup logic
        logger.info("Hello, World!")

        getCommand("connect")?.setExecutor(ConnectCommandExecutor())
        getCommand("convert")?.setExecutor(ConvertCommandExecutor())
    }

    override fun onDisable() {
        // Plugin shutdown logic
    }
}
