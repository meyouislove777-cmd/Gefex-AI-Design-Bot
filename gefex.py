"""
═══════════════════════════════════════════════════════════════
 Gefex — AI Design Bot (Python Single File)
 خيالك، نصممه. 🎨🤖
═══════════════════════════════════════════════════════════════

ملف واحد فقط.
- كل الأوامر موجودة هنا
- لا يوجد انتهاء صلاحية للأزرار
- حد يومي عادل فقط
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ====================== الإعدادات ======================
TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
GUILD_ID = os.getenv("GUILD_ID")  # اختياري
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "12"))

if not TOKEN or not OPENAI_API_KEY:
    print("❌ حط DISCORD_TOKEN و OPENAI_API_KEY في ملف .env")
    exit(1)

COLOR = 0x00D4AA
FOOTER = "Gefex — AI Design Bot | مجاني بالكامل"

# ====================== قاعدة بيانات JSON ======================
DB_PATH = Path(__file__).parent / "gefex-data.json"

def load_db():
    try:
        if DB_PATH.exists():
            return json.loads(DB_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"usage": {}, "identity": {}}

def save_db(data):
    try:
        DB_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print("DB save error:", e)

db = load_db()

def today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def get_usage(user_id: int) -> int:
    key = f"{user_id}_{today()}"
    return db["usage"].get(key, 0)

def add_usage(user_id: int, amount: int = 1):
    key = f"{user_id}_{today()}"
    db["usage"][key] = db["usage"].get(key, 0) + amount
    save_db(db)

def can_use(user_id: int, cost: int = 1) -> bool:
    return get_usage(user_id) + cost <= DAILY_LIMIT

def save_identity(guild_id, user_id, data: dict):
    key = f"{guild_id or 'dm'}_{user_id}"
    db["identity"][key] = {
        "name": data.get("name"),
        "colors": data.get("colors"),
        "style": data.get("style"),
        "base_prompt": data.get("base_prompt"),
        "updated_at": int(datetime.utcnow().timestamp())
    }
    save_db(db)

def get_identity(guild_id, user_id):
    key = f"{guild_id or 'dm'}_{user_id}"
    return db["identity"].get(key)

# ====================== OpenAI ======================
openai_client = OpenAI(api_key=OPENAI_API_KEY)

STYLES = {
    "gaming": "epic gaming style, vibrant neon colors, dynamic composition, high energy, esports aesthetic, sharp details, dramatic lighting",
    "luxury": "luxury premium style, elegant gold and black, sophisticated, high-end, cinematic lighting, rich textures, exclusive feel",
    "anime": "anime style, detailed anime illustration, vibrant colors, clean lines, studio quality, expressive, beautiful lighting",
    "cyberpunk": "cyberpunk style, neon lights, futuristic city, dark atmosphere, high tech, glowing elements, rainy night",
    "minimal": "minimalist style, clean design, simple shapes, limited color palette, modern, elegant negative space",
    "futuristic": "futuristic sci-fi style, advanced technology, sleek surfaces, holographic elements, clean futuristic design",
    "dark": "dark moody style, deep shadows, high contrast, dramatic lighting, black and dark tones, mysterious atmosphere",
    "cartoon": "cartoon style, bold outlines, vibrant flat colors, playful, fun, exaggerated features, clean illustration",
    "realistic": "photorealistic, highly detailed, realistic textures, natural lighting, 8k, professional photography",
    "cinematic": "cinematic style, film still, dramatic lighting, depth of field, color graded, epic composition, movie quality"
}

STYLE_CHOICES = [
    app_commands.Choice(name="Gaming - قيمنق", value="gaming"),
    app_commands.Choice(name="Luxury - فخم", value="luxury"),
    app_commands.Choice(name="Anime - أنمي", value="anime"),
    app_commands.Choice(name="Cyberpunk - سايبربانك", value="cyberpunk"),
    app_commands.Choice(name="Minimal - مينيمال", value="minimal"),
    app_commands.Choice(name="Futuristic - مستقبلي", value="futuristic"),
    app_commands.Choice(name="Dark - داكن", value="dark"),
    app_commands.Choice(name="Cartoon - كرتون", value="cartoon"),
    app_commands.Choice(name="Realistic - واقعي", value="realistic"),
    app_commands.Choice(name="Cinematic - سينمائي", value="cinematic"),
]

async def enhance_prompt(user_prompt: str, type_: str = "general", style: str = None, colors: str = None, name: str = None) -> str:
    type_map = {
        "logo": "Professional logo design. Clean, memorable, suitable for branding, vector-like, high contrast.",
        "banner": "Wide Discord server banner. Eye-catching, professional, atmospheric.",
        "profile": "Square profile picture / avatar. Centered strong subject, works at small size.",
        "poster": "Promotional poster or advertisement. Bold, clear hierarchy, attention-grabbing.",
        "thumbnail": "YouTube-style thumbnail. High contrast, bold, clickable look.",
        "background": "High quality background / wallpaper. Aesthetic, not too busy.",
        "pack": "Cohesive brand identity element. Consistent style and colors.",
        "general": "High-quality digital design or illustration."
    }

    system = (
        "You are an expert prompt engineer for DALL·E. "
        "Turn the user idea into one detailed English prompt only. No explanations. "
        "Understand Arabic perfectly. Keep under 350 words. Add quality boosters."
    )

    msg = f"User idea: {user_prompt}\nType: {type_map.get(type_, type_map['general'])}"
    if style:
        msg += f"\nStyle: {style}"
    if colors:
        msg += f"\nColors: {colors}"
    if name:
        msg += f"\nName/Brand: {name}"

    try:
        res = await asyncio.to_thread(
            openai_client.chat.completions.create,
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": msg}
            ],
            temperature=0.7,
            max_tokens=400
        )
        enhanced = res.choices[0].message.content.strip() if res.choices else user_prompt
        if style and style in STYLES:
            enhanced += f", {STYLES[style]}"
        return enhanced
    except Exception as e:
        print("Enhance error:", e)
        fallback = user_prompt
        if style and style in STYLES:
            fallback += f", {STYLES[style]}"
        if colors:
            fallback += f", colors: {colors}"
        return fallback

async def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> dict:
    valid = ["1024x1024", "1792x1024", "1024x1792"]
    final_size = size if size in valid else "1024x1024"

    res = await asyncio.to_thread(
        openai_client.images.generate,
        model="dall-e-3",
        prompt=prompt[:4000],
        n=1,
        size=final_size,
        quality="hd" if quality == "hd" else "standard",
        response_format="url"
    )

    url = res.data[0].url if res.data else None
    if not url:
        raise Exception("No image returned")
    revised = getattr(res.data[0], "revised_prompt", None) or prompt
    return {"url": url, "revised": revised}

# ====================== الإمبدات ======================
def base_embed() -> discord.Embed:
    e = discord.Embed(color=COLOR)
    e.set_footer(text=FOOTER)
    e.timestamp = datetime.utcnow()
    return e

def loading_embed(text: str = "جاري إنشاء التصميم...") -> discord.Embed:
    e = base_embed()
    e.title = "🎨 Gefex يعمل..."
    e.description = f"⏳ {text}"
    return e

def error_embed(title: str, desc: str) -> discord.Embed:
    e = base_embed()
    e.color = 0xFF4D4D
    e.title = f"❌ {title}"
    e.description = desc
    return e

def rate_embed(used: int) -> discord.Embed:
    return error_embed(
        "تم الوصول للحد اليومي",
        f"استخدمت **{used}/{DAILY_LIMIT}** صورة اليوم.\nالحد يتجدد كل 24 ساعة.\nGefex مجاني بالكامل."
    )

def image_embed(title: str, url: str, original: str = None, revised: str = None) -> discord.Embed:
    e = base_embed()
    e.title = title
    e.set_image(url=url)
    if original:
        p = original[:177] + "..." if len(original) > 180 else original
        e.add_field(name="📝 الوصف", value=p, inline=False)
    if revised:
        r = revised[:177] + "..." if len(revised) > 180 else revised
        e.add_field(name="✨ الوصف المحسّن", value=r, inline=False)
    return e

# ====================== أزرار ======================
class RegenView(discord.ui.View):
    def __init__(self, prompt: str, size: str, quality: str, user_id: int):
        super().__init__(timeout=None)  # بدون انتهاء صلاحية
        self.prompt = prompt
        self.size = size
        self.quality = quality
        self.user_id = user_id

    @discord.ui.button(label="إعادة التوليد", emoji="🔄", style=discord.ButtonStyle.primary, custom_id="regen_btn")
    async def regen(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message(
                embed=error_embed("غير مسموح", "هذا الزر لصاحب الطلب فقط."), ephemeral=True
            )
        if not can_use(interaction.user.id):
            return await interaction.response.send_message(
                embed=rate_embed(get_usage(interaction.user.id)), ephemeral=True
            )

        await interaction.response.defer()
        try:
            result = await generate_image(self.prompt, self.size, self.quality)
            add_usage(interaction.user.id)
            embed = image_embed("🔄 تم إعادة التوليد", result["url"], revised=result["revised"])
            await interaction.edit_original_response(embed=embed, view=self)
        except Exception as e:
            print("Regen error:", e)
            await interaction.followup.send(embed=error_embed("فشل", "حاول مرة أخرى."), ephemeral=True)

    @discord.ui.button(label="رابط الصورة", emoji="🔗", style=discord.ButtonStyle.secondary, custom_id="link_btn")
    async def link(self, interaction: discord.Interaction, button: discord.ui.Button):
        url = None
        if interaction.message and interaction.message.embeds:
            url = interaction.message.embeds[0].image.url if interaction.message.embeds[0].image else None
        if not url:
            return await interaction.response.send_message("ما لقيت رابط.", ephemeral=True)
        await interaction.response.send_message(f"🔗 رابط الصورة:\n{url}", ephemeral=True)

# ====================== دالة التوليد المشتركة ======================
async def do_generate(interaction: discord.Interaction, *, prompt: str, type_: str = "general",
                      style: str = None, colors: str = None, name: str = None,
                      size: str = "1024x1024", quality: str = "standard", title: str = "🎨 تصميمك جاهز"):

    user_id = interaction.user.id
    guild_id = interaction.guild_id

    if not can_use(user_id):
        return await interaction.edit_original_response(embed=rate_embed(get_usage(user_id)))

    try:
        final_style, final_colors, final_name = style, colors, name
        if guild_id:
            idn = get_identity(guild_id, user_id)
            if idn:
                if not final_style and idn.get("style"):
                    final_style = idn["style"]
                if not final_colors and idn.get("colors"):
                    final_colors = idn["colors"]
                if not final_name and idn.get("name"):
                    final_name = idn["name"]

        enhanced = await enhance_prompt(prompt, type_, final_style, final_colors, final_name)
        result = await generate_image(enhanced, size, quality)

        add_usage(user_id)

        embed = image_embed(title, result["url"], prompt, result["revised"])
        view = RegenView(enhanced, size, quality, user_id)
        await interaction.edit_original_response(embed=embed, view=view)

    except Exception as err:
        print("Generate error:", err)
        msg = "حدث خطأ أثناء إنشاء الصورة. حاول لاحقًا."
        err_str = str(err).lower()
        if "400" in err_str or "invalid" in err_str:
            msg = "الوصف غير مناسب. جرب تعديله."
        if "429" in err_str or "rate" in err_str:
            msg = "تم تجاوز حد OpenAI مؤقتًا. انتظر قليلاً."
        if "quota" in err_str or "billing" in err_str:
            msg = "رصيد OpenAI غير كافٍ."
        await interaction.edit_original_response(embed=error_embed("فشل التوليد", msg))

# ====================== البوت ======================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Gefex شغّال → {bot.user}")
    print(f"📊 السيرفرات: {len(bot.guilds)}")
    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ تم مزامنة {len(synced)} أمر في السيرفر")
        else:
            synced = await bot.tree.sync()
            print(f"✅ تم مزامنة {len(synced)} أمر عام")
    except Exception as e:
        print("Sync error:", e)

    await bot.change_presence(activity=discord.Game(name="خيالك، نصممه 🎨 | /مساعدة"))

# ---------- الأوامر ----------

@bot.tree.command(name="تخيل", description="حوّل أي وصف إلى صورة بالذكاء الاصطناعي")
@app_commands.describe(الوصف="اكتب فكرتك", الستايل="الستايل", الالوان="الألوان", الجودة="الجودة")
@app_commands.choices(الستايل=STYLE_CHOICES)
@app_commands.choices(الجودة=[
    app_commands.Choice(name="عادية", value="standard"),
    app_commands.Choice(name="عالية HD", value="hd")
])
async def imagine(interaction: discord.Interaction, الوصف: str, الستايل: str = None, الالوان: str = None, الجودة: str = "standard"):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed())
    await do_generate(interaction, prompt=الوصف, style=الستايل, colors=الالوان, quality=الجودة, title="🎨 تخيلتك صارت صورة")

@bot.tree.command(name="لوقو", description="إنشاء شعار احترافي")
@app_commands.describe(الاسم="اسم البراند", الوصف="وصف إضافي", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def logo(interaction: discord.Interaction, الاسم: str, الوصف: str = None, الستايل: str = "minimal", الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري تصميم الشعار..."))
    prompt = f'Professional logo for "{الاسم}". {الوصف or ""}'.strip()
    await do_generate(interaction, prompt=prompt, type_="logo", style=الستايل, colors=الالوان, name=الاسم, title=f"✨ لوقو: {الاسم}")

@bot.tree.command(name="بنر", description="إنشاء بنر للسيرفر")
@app_commands.describe(الوصف="وصف البنر", الاسم="اسم السيرفر", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def banner(interaction: discord.Interaction, الوصف: str, الاسم: str = None, الستايل: str = None, الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري تصميم البنر..."))
    await do_generate(interaction, prompt=الوصف, type_="banner", style=الستايل, colors=الالوان, name=الاسم, size="1792x1024", title="🖼️ بنر السيرفر جاهز")

@bot.tree.command(name="بروفايل", description="إنشاء صورة بروفايل")
@app_commands.describe(الوصف="وصف الصورة", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def profile(interaction: discord.Interaction, الوصف: str, الستايل: str = None, الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري تصميم البروفايل..."))
    await do_generate(interaction, prompt=الوصف, type_="profile", style=الستايل, colors=الالوان, title="👤 صورة البروفايل جاهزة")

@bot.tree.command(name="بوستر", description="إنشاء بوستر أو إعلان")
@app_commands.describe(الوصف="موضوع البوستر", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def poster(interaction: discord.Interaction, الوصف: str, الستايل: str = None, الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري تصميم البوستر..."))
    await do_generate(interaction, prompt=الوصف, type_="poster", style=الستايل, colors=الالوان, size="1024x1792", title="📢 البوستر جاهز")

@bot.tree.command(name="ثَمبنيل", description="إنشاء صورة مصغرة")
@app_commands.describe(الوصف="وصف الثَمبنيل", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def thumbnail(interaction: discord.Interaction, الوصف: str, الستايل: str = None, الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري تصميم الثَمبنيل..."))
    await do_generate(interaction, prompt=الوصف, type_="thumbnail", style=الستايل, colors=الالوان, size="1792x1024", title="🎬 الثَمبنيل جاهز")

@bot.tree.command(name="خلفية", description="إنشاء خلفية")
@app_commands.describe(الوصف="وصف الخلفية", الستايل="الستايل", الالوان="الألوان")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def background(interaction: discord.Interaction, الوصف: str, الستايل: str = None, الالوان: str = None):
    await interaction.response.defer()
    await interaction.edit_original_response(embed=loading_embed("جاري إنشاء الخلفية..."))
    await do_generate(interaction, prompt=الوصف, type_="background", style=الستايل, colors=الالوان, size="1792x1024", title="🌄 الخلفية جاهزة")

@bot.tree.command(name="باك", description="إنشاء هوية بصرية كاملة للسيرفر")
@app_commands.describe(الاسم="اسم السيرفر", الالوان="الألوان الرئيسية", الستايل="الستايل", وصف_اضافي="تفاصيل إضافية")
@app_commands.choices(الستايل=STYLE_CHOICES)
async def pack(interaction: discord.Interaction, الاسم: str, الالوان: str, الستايل: str, وصف_اضافي: str = None):
    await interaction.response.defer()
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    cost = 4

    if not can_use(user_id, cost):
        return await interaction.edit_original_response(embed=rate_embed(get_usage(user_id)))

    await interaction.edit_original_response(embed=loading_embed(f"جاري بناء الهوية البصرية لـ **{الاسم}**...\nقد يستغرق حوالي دقيقة."))

    try:
        base_idea = f'Brand identity for "{الاسم}". Colors: {الالوان}. Style: {الستايل}. {وصف_اضافي or ""}'
        base_enhanced = await enhance_prompt(base_idea, "pack", الستايل, الالوان, الاسم)
        save_identity(guild_id, user_id, {"name": الاسم, "colors": الالوان, "style": الستايل, "base_prompt": base_enhanced})

        assets = [
            {"label": "الشعار (Logo)", "size": "1024x1024", "extra": "clean logo, centered, icon + wordmark"},
            {"label": "البنر", "size": "1792x1024", "extra": "wide server banner, atmospheric"},
            {"label": "صورة البروفايل", "size": "1024x1024", "extra": "square profile picture, strong center"},
            {"label": "صورة الترحيب", "size": "1792x1024", "extra": "welcome banner for new members"},
        ]

        results = []
        for a in assets:
            try:
                prompt = f"{base_enhanced}, {a['extra']}, consistent brand identity, same color palette"
                img = await generate_image(prompt, a["size"])
                results.append({**a, "url": img["url"]})
                add_usage(user_id)
                await asyncio.sleep(1.4)
            except Exception as e:
                print("Pack asset fail:", e)

        if not results:
            return await interaction.edit_original_response(embed=error_embed("فشل الباك", "لم يتم توليد صور. حاول لاحقًا."))

        first = results[0]
        emb = image_embed(f"🔥 باك الهوية: {الاسم}", first["url"], base_idea)
        for r in results[1:]:
            emb.add_field(name=r["label"], value=f"[الصورة]({r['url']})", inline=False)
        
        await interaction.edit_original_response(embed=emb)

    except Exception as err:
        print("Pack error:", err)
        await interaction.edit_original_response(embed=error_embed("فشل الباك", "حاول لاحقًا."))

@bot.tree.command(name="مساعدة", description="معلومات عن البوت والأوامر")
async def help_cmd(interaction: discord.Interaction):
    emb = base_embed()
    emb.title = "📖 مساعدة Gefex"
    emb.description = "بوت ديسكورد ذكي لتوليد الصور والتصاميم بالذكاء الاصطناعي"
    
    emb.add_field(
        name="🎨 الأوامر الأساسية",
        value="""
`/تخيل` - حوّل أي فكرة إلى صورة
`/لوقو` - تصميم شعار احترافي
`/بنر` - بنر للسيرفر
`/بروفايل` - صورة بروفايل
`/بوستر` - بوستر أو إعلان
`/ثَمبنيل` - صورة مصغرة (YouTube)
`/خلفية` - خلفية جميلة
`/باك` - هوية بصرية كاملة (4 صور)
        """,
        inline=False
    )
    
    emb.add_field(
        name="⚙️ الخيارات",
        value="""
• **الستايل**: gaming, luxury, anime, cyberpunk, minimal...
• **الألوان**: أي وصف لوني (مثل: gold and black)
• **الجودة**: عادية أو HD عالية
        """,
        inline=False
    )
    
    emb.add_field(
        name="📊 الحد اليومي",
        value=f"**{DAILY_LIMIT}** صورة في اليوم (حد عادل)\nالحد يتجدد كل 24 ساعة",
        inline=False
    )
    
    emb.add_field(
        name="🎯 نصائح",
        value="""
• اكتب أوصاف تفصيلية وواضحة
• جرب أستايلات مختلفة
• استخدم الأزرار للإعادة أو النسخ
• السيرفر ينتظر إعادتك! 💎
        """,
        inline=False
    )
    
    await interaction.response.send_message(embed=emb)

if __name__ == "__main__":
    bot.run(TOKEN)
