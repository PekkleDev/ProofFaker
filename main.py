import string
import os
import random
import discord
from discord.ext import commands
from discord import app_commands

# ==========================================
# AYARLAR
# ==========================================

TOKEN = os.getenv("TOKEN")

PROOF_CHANNEL_ID = 1563982186011435232
STATUS_ROLE_ID = 1563982169100132484
STATUS_LOG_CHANNEL_ID = 1563982173491564594
OWNER_ID = 1547736123189502062

# Boş bırakırsan otomatik algılama denenir
GUILD_TAG = "free"

REQUIRED_STATUS_TEXTS = [
    "/trnitro",
    ".gg/trnitro",
    "@trnitro"
]




# ==========================================
# BOT KURULUMU
# Ayarlar bölümünün altına yapıştır.
# ==========================================

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


def generate_code(prefix):
    chars = string.ascii_uppercase + string.digits
    parts = [
        "".join(random.choices(chars, k=4))
        for _ in range(3)
    ]
    return f"{prefix}-" + "-".join(parts)


# ==========================================
# GUILD TAG KONTROLÜ
# ==========================================

def has_server_guild_tag(member):
    primary_guild = getattr(member, "primary_guild", None)

    if primary_guild is None:
        return False

    identity_guild_id = getattr(
        primary_guild, "identity_guild_id", None
    )
    identity_enabled = getattr(
        primary_guild, "identity_enabled", False
    )
    tag = getattr(primary_guild, "tag", None)

    if str(identity_guild_id) != str(member.guild.id):
        return False

    if identity_enabled is not True or not tag:
        return False

    if GUILD_TAG:
        return tag.casefold() == GUILD_TAG.casefold()

    return True


# ==========================================
# DURUM METNİ KONTROLÜ
# ==========================================

def has_required_status(member):
    for activity in getattr(member, "activities", []):
        if isinstance(activity, discord.CustomActivity):
            status_text = str(activity.state or "").casefold()

            if any(
                text.casefold() in status_text
                for text in REQUIRED_STATUS_TEXTS
            ):
                return True

    return False


# ==========================================
# ORTAK ROL GÜNCELLEME + LOG
# ==========================================

async def update_special_role(member):
    if member.bot:
        return

    role = member.guild.get_role(STATUS_ROLE_ID)
    if role is None:
        print(f"Rol bulunamadı: {STATUS_ROLE_ID}")
        return

    status_match = has_required_status(member)
    tag_match = has_server_guild_tag(member)

    print(
        f"[ROL KONTROL] {member} | "
        f"Durum: {status_match} | "
        f"Guild Tag: {tag_match} | "
        f"Rol ID: {STATUS_ROLE_ID}"
    )

    should_have_role = status_match or tag_match
    already_has_role = role in member.roles

    if should_have_role == already_has_role:
        return

    log_channel = member.guild.get_channel(STATUS_LOG_CHANNEL_ID)

    try:
        if should_have_role:
            reasons = []

            if status_match:
                reasons.append("Belirlenen durum metni")

            if tag_match:
                reasons.append("Sunucunun Guild Tag'i")

            await member.add_roles(
                role,
                reason=" / ".join(reasons)
            )

            title = "✅ Otomatik Rol Verildi"
            color = discord.Color.green()
            detail = "Rol sebebi: " + " ve ".join(reasons)

        else:
            await member.remove_roles(
                role,
                reason="Durum metni ve Guild Tag koşulları sağlanmıyor"
            )

            title = "➖ Otomatik Rol Kaldırıldı"
            color = discord.Color.red()
            detail = (
                "Üyenin belirlenen durum metni ve sunucu Guild Tag'i "
                "artık eşleşmiyor."
            )

        embed = discord.Embed(
            title=title,
            description=detail,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(
            name="Üye",
            value=f"{member.mention} (`{member.id}`)",
            inline=False
        )
        embed.add_field(
            name="Rol",
            value=role.mention,
            inline=True
        )

        if log_channel is not None:
            await log_channel.send(embed=embed)

    except discord.Forbidden:
        print(
            "Rol işlemi başarısız. Botun Manage Roles iznini "
            "ve rol sırasını kontrol et."
        )
    except discord.HTTPException as error:
        print(f"Otomatik rol hatası: {error}")


# ==========================================
# /NITRO
# ==========================================

@bot.tree.command(name="nitro", description="Nitro kodu oluştur.")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.choices(
    tur=[
        app_commands.Choice(name="Basic", value="Basic"),
        app_commands.Choice(name="Boost", value="Boost"),
    ],
    sure=[
        app_commands.Choice(name="Aylık", value="Aylık"),
        app_commands.Choice(name="Yıllık", value="Yıllık"),
    ]
)
async def nitro(
    interaction: discord.Interaction,
    tur: app_commands.Choice[str],
    sure: app_commands.Choice[str]
):
    embed = discord.Embed(
        title="🎁 Nitro Ödülü",
        color=discord.Color.gold()
    )
    embed.add_field(name="Tür", value=tur.value, inline=True)
    embed.add_field(name="Süre", value=sure.value, inline=True)
    embed.add_field(
        name="Kod",
        value=f"```{generate_code('NITRO')}```",
        inline=False
    )
    embed.add_field(
        name="📌 Nasıl kullanılır?",
        value=(
            "Discord Kullanıcı Ayarları → Hediye Envanteri "
            "bölümüne girip geçerli bir hediye kodunu kullan."
        ),
        inline=False
    )
    await interaction.response.send_message(embed=embed)


# ==========================================
# /ROBUX
# ==========================================

@bot.tree.command(name="robux", description="Robux ödül kodu oluştur.")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.choices(
    miktar=[
        app_commands.Choice(name="450 Robux", value="450"),
        app_commands.Choice(name="1500 Robux", value="1500"),
        app_commands.Choice(name="4500 Robux", value="4500"),
        app_commands.Choice(name="10000 Robux", value="10000"),
        app_commands.Choice(name="5000 Robux", value="5000"),
    ],
    sure=[
        app_commands.Choice(name="Aylık", value="Aylık"),
        app_commands.Choice(name="Yıllık", value="Yıllık"),
    ]
)
async def robux(
    interaction: discord.Interaction,
    miktar: app_commands.Choice[str],
    sure: app_commands.Choice[str]
):
    embed = discord.Embed(
        title="💰 Robux Ödülü",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Miktar",
        value=f"{miktar.value} Robux",
        inline=True
    )
    embed.add_field(name="Süre", value=sure.value, inline=True)
    embed.add_field(
        name="Kod",
        value=f"```{generate_code('ROBUX')}```",
        inline=False
    )
    embed.add_field(
        name="📌 Nasıl kullanılır?",
        value=(
            "Gerçek Roblox hediye kartları için resmi kod "
            "kullanma sayfasını ziyaret et:\n"
            "https://www.roblox.com/redeem"
        ),
        inline=False
    )
    await interaction.response.send_message(embed=embed)


# ==========================================
# /PROOF — YALNIZCA OWNER
# ==========================================

@bot.tree.command(name="proof", description="Ödül görselini kanala gönder.")
@app_commands.describe(gorsel_url="Görselin HTTPS bağlantısı")
async def proof(
    interaction: discord.Interaction,
    gorsel_url: str
):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ Bu komutu yalnızca bot sahibi kullanabilir.",
            ephemeral=True
        )
        return

    if not gorsel_url.startswith("https://"):
        await interaction.response.send_message(
            "HTTPS bağlantısı kullan.",
            ephemeral=True
        )
        return

    channel = bot.get_channel(PROOF_CHANNEL_ID)

    if channel is None:
        try:
            channel = await bot.fetch_channel(PROOF_CHANNEL_ID)
        except discord.HTTPException:
            await interaction.response.send_message(
                "Kanal bulunamadı.",
                ephemeral=True
            )
            return

    embed = discord.Embed(
        title="🏆 ÖDÜL KAZANILDI!",
        description=(
            "✨ Tebrikler!\n\n"
            "Bir kullanıcı davet yaparak ödül kazandı!\n"
            "🎉 Katılımın ve desteğin için teşekkür ederiz."
        ),
        color=discord.Color.gold()
    )
    embed.set_image(url=gorsel_url)
    embed.set_footer(text="Ödül Sistemi")

    try:
        await channel.send(embed=embed)
    except (discord.HTTPException, discord.Forbidden):
        await interaction.response.send_message(
            "Mesaj gönderilemedi; kanal izinlerini kontrol et.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"Ödül mesajı <#{PROOF_CHANNEL_ID}> kanalına gönderildi.",
        ephemeral=True
    )


# ==========================================
# /DMALL — YALNIZCA OWNER
# ==========================================

@bot.tree.command(
    name="dmall",
    description="Sunucu üyelerine özel mesaj gönder."
)
@app_commands.describe(mesaj="Üyelere gönderilecek mesaj")
async def dmall(
    interaction: discord.Interaction,
    mesaj: str
):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "❌ Bu komutu yalnızca bot sahibi kullanabilir.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    if guild is None:
        await interaction.followup.send(
            "Bu komut yalnızca sunucuda kullanılabilir.",
            ephemeral=True
        )
        return

    sent = 0
    failed = 0

    for member in guild.members:
        if member.bot:
            continue

        try:
            embed = discord.Embed(
                title="📩 Sunucu Mesajı",
                description=mesaj[:4000],
                color=discord.Color.blurple()
            )
            embed.set_footer(
                text=f"{guild.name} • Sunucu Duyurusu"
            )

            await member.send(embed=embed)
            sent += 1

        except (discord.Forbidden, discord.HTTPException):
            failed += 1

    await interaction.followup.send(
        f"📬 DM gönderimi tamamlandı.\n"
        f"✅ Gönderilen: {sent}\n"
        f"⚠️ Gönderilemeyen: {failed}",
        ephemeral=True
    )


# ==========================================
# ÖZEL DURUM DEĞİŞİNCE ROLÜ KONTROL ET
# ==========================================

@bot.event
async def on_presence_update(before, after):
    await update_special_role(after)


# ==========================================
# ÜYE BİLGİSİ DEĞİŞİNCE ROLÜ KONTROL ET
# ==========================================

@bot.event
async def on_member_update(before, after):
    await update_special_role(after)


# ==========================================
# YENİ ÜYE KATILINCA KONTROL ET
# ==========================================

@bot.event
async def on_member_join(member):
    await update_special_role(member)


# ==========================================
# KOMUT HATALARI
# ==========================================

@nitro.error
@robux.error
@proof.error
@dmall.error
async def command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        message = "❌ Bu komutu yalnızca yöneticiler kullanabilir."
    else:
        print(f"Komut hatası: {error}")
        message = "Bir hata oluştu. Ayarları kontrol et."

    if interaction.response.is_done():
        await interaction.followup.send(
            message,
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            message,
            ephemeral=True
        )


# ==========================================
# BAŞLAT
# ==========================================

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(
            f"{bot.user} aktif! "
            f"{len(synced)} komut senkronize edildi."
        )
    except discord.HTTPException as error:
        print(f"Komut senkronizasyon hatası: {error}")


if not TOKEN:
    raise RuntimeError(
        "TOKEN ortam değişkeni ayarlanmamış!"
    )

bot.run(TOKEN)
