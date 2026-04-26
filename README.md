## tg-appointment-bot

A lightweight, functional Telegram bot for automating client appointments for services (manicure, massage, haircut). The bot lets clients choose a service, a specialist, and a time; the administrator manages the bookings database. 

# Features

- For clients:
    - Intuitive booking flow using buttons (Inline and Reply).
    - Option to choose a specific specialist or “any specialist”.
    - View current bookings.
    - Protection against double-booking the same time slot.
- For administrator:
    
    - Admin panel (command /admin).
    - View all active bookings.
    - Booking statistics.
    - Delete a specific booking or clear the entire database.

Tech stack

- Language: Python 3.x
- Library: aiogram
- Database: SQLite (aiosqlite)
- States: FSM (Finite State Machine) to manage dialog flow

Installation and running

- `git clone https://github.com/sudo-pacman-Syy/tg-appointment-bot.git`
- `create file .env and write to you're ADIM_ID and BOT_TOKEN`
- `make rebuild`
- `make run`

