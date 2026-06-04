"""
Debug utilities for watching values in the HUD

Usage:
    from src import debug

    debug.watch("event", next_event[2])
    debug.watch("player_health", self.health)
    debug.watch("enemy_count", len(game.enemies))
"""

stored_debug_values = {}

# Record a value to display this frame
def watch(key, value):
    stored_debug_values[key] = value

# Current watched values, read by the renderer when used
def stored_values():
    return stored_debug_values

# Evict all watched values
def clear_values():
    stored_debug_values.clear()