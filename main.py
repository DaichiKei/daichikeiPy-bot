import discord
from discord.ext import commands
from gtts import gTTS
import os

# Token bot Anda
TOKEN = ""

# Intent untuk membaca pesan
intents = discord.Intents.default()
intents.message_content = True

# Membuat objek bot
bot = commands.Bot(command_prefix=".", intents=intents)

# Struktur data untuk menyimpan pertanyaan dan jawaban
responses = {
    "halo": "Halo! Ada yang bisa saya bantu?",
    "apa kabar": "Saya baik, terima kasih! Bagaimana dengan Anda?",
    "siapa kamu": "Saya adalah chatbot AI sederhana.",
    "bantu saya": "Tentu! Apa yang bisa saya bantu?",
}

# Event ketika bot berhasil login
@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}!")

# Command untuk bergabung ke voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
    # Periksa apakah pesan dikirim di channel "daichikei-only"
        if ctx.channel.name != 'daichikei-only':
            return

    # Periksa apakah pengirim pesan adalah Daichi Kei (gunakan ID pengguna Daichi Kei)
        if ctx.author.id != 860752020867907596:  # Ganti dengan ID pengguna Daichi Kei
            await ctx.channel.send("Hanya bisa digunakan oleh Daichi Kei.")
            return
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Bot telah bergabung ke voice channel!")
    else:
        await ctx.send("Anda harus berada di voice channel agar bot bisa bergabung.")

# Command untuk meninggalkan voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
    # Periksa apakah pesan dikirim di channel "daichikei-only"
        if ctx.channel.name != 'daichikei-only':
            return

    # Periksa apakah pengirim pesan adalah Daichi Kei (gunakan ID pengguna Daichi Kei)
        if ctx.author.id != 860752020867907596:  # Ganti dengan ID pengguna Daichi Kei
            await ctx.channel.send("Hanya bisa digunakan oleh Daichi Kei.")
            return
        await ctx.voice_client.disconnect()
        await ctx.send("Bot telah meninggalkan voice channel.")
    else:
        await ctx.send("Bot tidak berada di voice channel.")

# Event untuk membaca pesan dan berbicara di voice channel
@bot.event
async def on_message(message):
    # Abaikan pesan dari bot itu sendiri
    if message.author == bot.user:
        return
    
    # Periksa apakah pesan dikirim di channel "daichikei-only"
    if message.channel.name != 'daichikei-only':
        return

    # Periksa apakah pengirim pesan adalah Daichi Kei (gunakan ID pengguna Daichi Kei)
    if message.author.id != 860752020867907596:  # Ganti dengan ID pengguna Daichi Kei
        await message.channel.send("Hanya bisa digunakan oleh Daichi Kei.")
        return

    # Ambil pesan pengguna
    user_message = message.content.lower()

    # Cek apakah pesan cocok dengan keyword (opsional)
    # response = responses.get(user_message, None)

    # Jika ada pesan dan bot berada di voice channel
    if user_message and message.guild.voice_client:
        # Menggunakan gTTS untuk membuat file audio
        tts = gTTS(user_message, lang="id")
        tts.save("message.mp3")

        # Memutar audio di voice channel
        voice_client = message.guild.voice_client
        audio_source = discord.FFmpegPCMAudio("message.mp3")
        if not voice_client.is_playing():
            voice_client.play(audio_source)

    # Proses perintah lainnya
    await bot.process_commands(message)


# Menjalankan bot
bot.run(TOKEN)
