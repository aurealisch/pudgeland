package me.aurealisch.pudgeland

import org.bukkit.Material
import org.bukkit.inventory.ItemStack

data class DrugItem(val displayName: String) {
    val itemStack = ItemStack(Material.STICK).itemMeta?.setDisplayName(displayName)
}
