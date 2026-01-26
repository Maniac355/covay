"""Localization helpers for the Go game UI."""

from __future__ import annotations


_PLAYER_LABELS = {
    "Black": "Đen",
    "White": "Trắng",
    "Tie": "Hòa",
}

_RULESET_LABELS = {
    "Japanese": "Nhật Bản",
    "Chinese": "Trung Quốc",
}


def vi_player(name: str) -> str:
    return _PLAYER_LABELS.get(name, name)


def vi_ruleset(name: str) -> str:
    return _RULESET_LABELS.get(name, name)
