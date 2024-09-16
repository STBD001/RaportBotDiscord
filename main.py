import discord
from discord.ext import commands
from collections import defaultdict
import datetime

# Inicjalizacja bota
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Słownik do przechowywania danych o godzinach nauki
study_log = defaultdict(list)

# Wydarzenie po zalogowaniu bota
@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

# Komenda do logowania godzin nauki
@bot.command(name='log')
async def log_study(ctx, subject: str, hours: float):
    user = ctx.author
    current_time = datetime.datetime.now()

    # Zapisanie logu
    study_log[user.id].append({'subject': subject, 'hours': hours, 'time': current_time})

    await ctx.send(f"{user.name}, zapisano {hours} godzin nauki z przedmiotu: {subject}.")

# Komenda do generowania raportu dla użytkownika
@bot.command(name='raport')
async def report(ctx):
    user = ctx.author
    if user.id not in study_log or len(study_log[user.id]) == 0:
        await ctx.send(f"{user.name}, nie masz jeszcze żadnych logów nauki.")
        return

    report_message = f"**Raport nauki dla {user.name}:**\n"
    total_hours = 0

    for log in study_log[user.id]:
        subject = log['subject']
        hours = log['hours']
        time = log['time'].strftime("%Y-%m-%d %H:%M")
        report_message += f"{time}: {hours} godzin - {subject}\n"
        total_hours += hours

    report_message += f"\nŁączny czas nauki: {total_hours:.2f} godzin."

    await ctx.send(report_message)

# Komenda do generowania raportu globalnego (dla wszystkich)
@bot.command(name='global_raport')
async def global_report(ctx):
    if len(study_log) == 0:
        await ctx.send("Brak danych do wygenerowania globalnego raportu.")
        return

    global_message = "**Globalny raport nauki:**\n"
    global_totals = defaultdict(float)

    for user_id, logs in study_log.items():
        user = await bot.fetch_user(user_id)
        user_total = 0

        for log in logs:
            subject = log['subject']
            hours = log['hours']
            global_totals[subject] += hours
            user_total += hours

        global_message += f"{user.name}: {user_total:.2f} godzin\n"

    global_message += "\nŁączny czas nauki per przedmiot:\n"
    for subject, total_hours in global_totals.items():
        global_message += f"{subject}: {total_hours:.2f} godzin\n"

    await ctx.send(global_message)

# Uruchomienie bota
bot.run('xxx')
