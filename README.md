# 🐦 Angry Birds (Pygame Powered)

A 2-player Angry Birds-style physics game built with **Pygame**, featuring classic sling mechanics, destructible towers, and bird projectiles.

## 🎮 Features

- 🎯 Sling-based launching mechanics for both players
- 🧱 Destructible towers made of wood, ice, and stone
- 🐤 Multiple bird types (red, blue, yellow, bomb)
- 🎵 Background music and sound effects
- 🕹️ Turn-based 2-player gameplay
- 🖼️ Custom assets, loading screen, and clean UI

## 🧠 How It Works

- Physics (velocity, gravity, collision detection) is manually handled using Python logic.
- Towers are loaded from text files (`tower.txt`) using block characters (e.g., `W`, `I`, `S`).
- Each bird type can interact with blocks differently.
- A custom game loop handles turn-switching, bird launching, and win conditions.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- `pygame`

```bash
pip install pygame
