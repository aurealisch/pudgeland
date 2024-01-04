from dataclasses import dataclass as dataclasses_dataclass


@dataclasses_dataclass
class Configuration:
    collecting_range_start: int
    collecting_range_stop: int
    domestication_ratio: int
    purchase_coin_ratio: int
    purchase_diamond_ratio: int
    purchase_netherite_ratio: int
