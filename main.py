import discord
from discord import app_commands
from discord.ui import View, Select
import datetime, random, traceback, os
import pyppeteer
import asyncio
import pytz
channels = [1560908743863042129]
token = ""

locale_to_timezone = {
    discord.Locale.american_english: 'America/New_York',        # en-US
    discord.Locale.british_english: 'Europe/London',            # en-GB
    discord.Locale.bulgarian: 'Europe/Sofia',                   # bg
    discord.Locale.chinese: 'Asia/Shanghai',                    # zh-CN
    discord.Locale.taiwan_chinese: 'Asia/Taipei',               # zh-TW
    discord.Locale.croatian: 'Europe/Zagreb',                   # hr
    discord.Locale.czech: 'Europe/Prague',                      # cs
    discord.Locale.indonesian: 'Asia/Jakarta',                  # id
    discord.Locale.danish: 'Europe/Copenhagen',                 # da
    discord.Locale.dutch: 'Europe/Amsterdam',                   # nl
    discord.Locale.finnish: 'Europe/Helsinki',                  # fi
    discord.Locale.french: 'Europe/Paris',                      # fr
    discord.Locale.german: 'Europe/Berlin',                     # de
    discord.Locale.greek: 'Europe/Athens',                      # el
    discord.Locale.hindi: 'Asia/Kolkata',                      # hi
    discord.Locale.hungarian: 'Europe/Budapest',                # hu
    discord.Locale.italian: 'Europe/Rome',                      # it
    discord.Locale.japanese: 'Asia/Tokyo',                      # ja
    discord.Locale.korean: 'Asia/Seoul',                        # ko
    discord.Locale.latin_american_spanish: 'America/Mexico_City', # es-419
    discord.Locale.lithuanian: 'Europe/Vilnius',                # lt
    discord.Locale.norwegian: 'Europe/Oslo',                    # no
    discord.Locale.polish: 'Europe/Warsaw',                     # pl
    discord.Locale.brazil_portuguese: 'America/Sao_Paulo',      # pt-BR
    discord.Locale.romanian: 'Europe/Bucharest',                # ro
    discord.Locale.russian: 'Europe/Moscow',                    # ru
    discord.Locale.spain_spanish: 'Europe/Madrid',              # es-ES
    discord.Locale.swedish: 'Europe/Stockholm',                 # sv-SE
    discord.Locale.thai: 'Asia/Bangkok',                        # th
    discord.Locale.turkish: 'Europe/Istanbul',                  # tr
    discord.Locale.ukrainian: 'Europe/Kyiv',                    # uk
    discord.Locale.vietnamese: 'Asia/Ho_Chi_Minh',              # vi
}

def get_current_time_in_locale(interaction: discord.Interaction):
    user_locale = interaction.locale  # Get the user's locale
    timezone_str = locale_to_timezone.get(user_locale, 'UTC')  # Default to UTC if locale not found
    timezone = pytz.timezone(timezone_str)
    
    # Get the current time in the specified timezone
    current_time = datetime.datetime.now(timezone)
    return current_time

def generate_time_range(interaction):
    current_time = get_current_time_in_locale(interaction)
    
    random_minutes = random.randint(2, 7)
    new_time = current_time + datetime.timedelta(minutes=random_minutes)
    
    # Adjust if the new time minute exceeds 59
    if new_time.minute > 59:
        new_time = new_time.replace(hour=new_time.hour + 1, minute=new_time.minute % 60)
    
    current_time_format = current_time.strftime('%I:%M %p').lstrip('0')
    new_time_format = new_time.strftime('%I:%M %p').lstrip('0')
    original_time_format = current_time.strftime("%d %B %Y")
    
    return current_time_format, new_time_format, original_time_format

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD_ID = 1293281234037772420  # Replace with your guild ID
        guild = discord.Object(id=GUILD_ID)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Use /proof to see the commands"))
        print(f"{self.user} ({self.user.id}) is ready!")

client = Client()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(client.user.mention):
        await message.channel.send(f"{message.author.mention} /proof")













class NitroPage:
    def __init__(self, gifter_username, receiver_username, gifter_message, receiver_message, gifter_avatar_url, receiver_avatar_url, timestamp_1, timestamp_2, full_date, claimed):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""


        self.gifter_username = gifter_username.replace('<', '').replace('>', '').replace('script', '')
        self.receiver_username = receiver_username.replace('<', '').replace('>', '').replace('script', '')

        self.gifter_message = gifter_message.replace('<', '').replace('>', '').replace('script', '')
        self.receiver_message = receiver_message.replace('<', '').replace('>', '').replace('script', '')

        self.gifter_avatar_url = gifter_avatar_url
        self.receiver_avatar_url = receiver_avatar_url

        self.timestamp_1 = timestamp_1
        self.timestamp_2 = timestamp_2
        self.full_date = full_date
        if self.full_date.startswith('0'):
            self.full_date = self.full_date.replace('0', '', 1)

        self.claimed = claimed

    def get_proof(self):
        if self.claimed==True:
            filename = "assets/nitroproof.html"
        else:
            filename = "assets/nitroproofclaimed.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('GIFTER_USERNAME', self.gifter_username)
            self.html_content = self.html_content.replace('RECEIVER_USERNAME', self.receiver_username)
            self.html_content = self.html_content.replace('GIFTER_MESSAGE', self.gifter_message+' ' if self.gifter_message!="" else self.gifter_message)
            self.html_content = self.html_content.replace('RECEIVER_MESSAGE', self.receiver_message)
            self.html_content = self.html_content.replace('GIFTER_AVATAR_URL', self.gifter_avatar_url)
            self.html_content = self.html_content.replace('RECEIVER_AVATAR_URL', self.receiver_avatar_url)
            self.html_content = self.html_content.replace('TIMESTAMP_1', self.timestamp_1)
            self.html_content = self.html_content.replace('TIMESTAMP_2', self.timestamp_2)
            self.html_content = self.html_content.replace('FULL_DATE', self.full_date)
            self.html_content = self.html_content.replace('KJASNZXCJD', f'{random.randint(36,47)}')
        return self.html_content

class NitroModal(discord.ui.Modal, title='Nitro proof generator'):
    type = discord.ui.TextInput(
        label="Nitro type (leave empty for unclaimed)",
        placeholder="unclaimed/claimed",
        style=discord.TextStyle.short,
        required=False,
    )

    gifteridd = discord.ui.TextInput(
        label="Gifter's ID (leave empty for yours)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )

    giftertext = discord.ui.TextInput(
        label="Gifter's message",
        placeholder="Congratulations! You won the giveaway, here's your nitro: ",
        style=discord.TextStyle.short,
        required=False,
    )

    receiveridd = discord.ui.TextInput(
        label="Receiver's ID (leave empty for random)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )

    receivertext = discord.ui.TextInput(
        label="Receiver's message",
        style=discord.TextStyle.short,
        placeholder='OMG! Thanks!',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.note = ""
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 

            if self.type.value == "claimed":
                self.nitroclaimed = True
            else:
                self.nitroclaimed = False

            self.gifter = interaction.user
            if self.gifteridd.value != "":
                try:
                    self.gifter = await client.fetch_user(int(self.gifteridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"
            if self.gifter.global_name == None:
                self.gifter_globalname = self.gifter.name
            else:
                self.gifter_globalname = self.gifter.global_name


            members = await interaction.guild.chunk()
            self.receiver = random.choice(members)
            if self.receiveridd.value != "":
                try:
                    self.receiver = await client.fetch_user(int(self.receiveridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"


            if self.receiver.global_name == None:
                self.receiver_globalname = self.receiver.name
            else:
                self.receiver_globalname = self.receiver.global_name

            self.gifter_message = self.giftertext.value
            self.receiver_message = self.receivertext.value

            if not self.gifter.avatar:
                self.gifter_avatar = self.gifter.default_avatar.url
            else:
                self.gifter_avatar = self.gifter.avatar.url

            if not self.receiver.avatar:
                self.receiver_avatar = self.receiver.default_avatar.url
            else:
                self.receiver_avatar = self.receiver.avatar.url

            times = generate_time_range(interaction)

            self.timestamp_1 = times[0]
            self.timestamp_2 = times[1]
            self.full_date = times[2]
            proof = NitroPage(self.gifter_globalname, self.receiver_globalname, self.gifter_message, self.receiver_message, self.gifter_avatar, self.receiver_avatar, self.timestamp_1, self.timestamp_2, self.full_date, self.nitroclaimed).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()
            
            await page.setViewport({'width': 1300, 'height': 500})

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.goto(absolute_path)
            screenshot_options = {
                'path': 'proof.png',
                'clip': {
                    'x': random.randint(1, 8),
                    'y': random.randint(75,83),
                    'width': random.randint(850,1100),
                    'height': random.randint(400,420)
                }
            }
            await page.screenshot(screenshot_options)
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description=f"> **Please check your DMs!** {self.note if self.note else ''}")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure you provided valid information and try again. Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof for a nitro giveaway.')
async def nitroproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(NitroModal())


class RobuxPage:
    def __init__(self, gifter_username, receiver_username, receiver_message, gifter_avatar_url, receiver_avatar_url, timestamp_1, timestamp_2, full_date):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""

    

        self.gifter_username = gifter_username.replace('<', '').replace('>', '').replace('script', '')
        self.receiver_username = receiver_username.replace('<', '').replace('>', '').replace('script', '')

        self.receiver_message = receiver_message.replace('<', '').replace('>', '').replace('script', '')

        self.gifter_avatar_url = gifter_avatar_url
        self.receiver_avatar_url = receiver_avatar_url

        self.timestamp_1 = timestamp_1
        self.timestamp_2 = timestamp_2
        self.full_date = full_date
        if self.full_date.startswith('0'):
            self.full_date = self.full_date.replace('0', '', 1)


    def get_proof(self):
        filename = "assets/robuxproof.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('GIFTER_USERNAME', self.gifter_username)
            self.html_content = self.html_content.replace('RECEIVER_USERNAME', self.receiver_username)
            self.html_content = self.html_content.replace('RECEIVER_MESSAGE', self.receiver_message)
            self.html_content = self.html_content.replace('GIFTER_AVATAR_URL', self.gifter_avatar_url)
            self.html_content = self.html_content.replace('RECEIVER_AVATAR_URL', self.receiver_avatar_url)
            self.html_content = self.html_content.replace('TIMESTAMP_1', self.timestamp_1)
            self.html_content = self.html_content.replace('TIMESTAMP_2', self.timestamp_2)
            self.html_content = self.html_content.replace('FULL_DATE', self.full_date)
        return self.html_content

class RobuxModal(discord.ui.Modal, title='Robux proof generator'):
 
    gifteridd = discord.ui.TextInput(
        label="Gifter's ID (leave empty for yours)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )



    receiveridd = discord.ui.TextInput(
        label="Receiver's ID (leave empty for random)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )
    receivertext = discord.ui.TextInput(
        label="Receiver's message",
        style=discord.TextStyle.short,
        placeholder='OMG! Thanks!',
        required=True,
    )



    async def on_submit(self, interaction: discord.Interaction):
        self.note = ""
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 


            self.gifter = interaction.user
            if self.gifteridd.value != "":
                try:
                    self.gifter = await client.fetch_user(int(self.gifteridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"
            if self.gifter.global_name == None:
                self.gifter_globalname = self.gifter.name
            else:
                self.gifter_globalname = self.gifter.global_name


            members = await interaction.guild.chunk()
            self.receiver = random.choice(members)
            if self.receiveridd.value != "":
                try:
                    self.receiver = await client.fetch_user(int(self.receiveridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"


            if self.receiver.global_name == None:
                self.receiver_globalname = self.receiver.name
            else:
                self.receiver_globalname = self.receiver.global_name


            self.receiver_message = self.receivertext.value

            if not self.gifter.avatar:
                self.gifter_avatar = self.gifter.default_avatar.url
            else:
                self.gifter_avatar = self.gifter.avatar.url

            if not self.receiver.avatar:
                self.receiver_avatar = self.receiver.default_avatar.url
            else:
                self.receiver_avatar = self.receiver.avatar.url

            times = generate_time_range(interaction)

            self.timestamp_1 = times[0]
            self.timestamp_2 = times[1]
            self.full_date = times[2]
            proof = RobuxPage(self.gifter_globalname, self.receiver_globalname, self.receiver_message, self.gifter_avatar, self.receiver_avatar, self.timestamp_1, self.timestamp_2, self.full_date).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()
            
            await page.setViewport({'width': 1300, 'height': 500})

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.goto(absolute_path)
            screenshot_options = {
                'path': 'proof.png',
                'clip': {
                    'x': random.randint(1, 8),
                    'y': random.randint(130, 135),
                    'width': random.randint(850, 1100),
                    'height': random.randint(350, 355)
                }
            }
            await page.screenshot(screenshot_options)
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description=f"> **Please check your DMs!** {self.note if self.note else ''}")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure your DM's are enabled.**\n**> Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof for a robux giveaway.')
async def robuxproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(RobuxModal())


class MinecraftPage:
    def __init__(self, gifter_username, receiver_username, receiver_message, gifter_avatar_url, receiver_avatar_url, timestamp_1, timestamp_2, full_date):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""


        self.gifter_username = gifter_username.replace('<', '').replace('>', '').replace('script', '')
        self.receiver_username = receiver_username.replace('<', '').replace('>', '').replace('script', '')

        self.receiver_message = receiver_message.replace('<', '').replace('>', '').replace('script', '')

        self.gifter_avatar_url = gifter_avatar_url
        self.receiver_avatar_url = receiver_avatar_url

        self.timestamp_1 = timestamp_1
        self.timestamp_2 = timestamp_2
        self.full_date = full_date
        if self.full_date.startswith('0'):
            self.full_date = self.full_date.replace('0', '', 1)


    def get_proof(self):
        filename = "assets/minecraftproof.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('GIFTER_USERNAME', self.gifter_username)
            self.html_content = self.html_content.replace('RECEIVER_USERNAME', self.receiver_username)
            self.html_content = self.html_content.replace('RECEIVER_MESSAGE', self.receiver_message)
            self.html_content = self.html_content.replace('GIFTER_AVATAR_URL', self.gifter_avatar_url)
            self.html_content = self.html_content.replace('MC_EMAIL', 'mahdi1337@gmail.com'+str(random.randint(1,10000000)))
            self.html_content = self.html_content.replace('MC_PASS', 'mahdi1337'+str(random.randint(1,10000000)))
            self.html_content = self.html_content.replace('RECEIVER_AVATAR_URL', self.receiver_avatar_url)
            self.html_content = self.html_content.replace('TIMESTAMP_1', self.timestamp_1)
            self.html_content = self.html_content.replace('TIMESTAMP_2', self.timestamp_2)
            self.html_content = self.html_content.replace('FULL_DATE', self.full_date)
        return self.html_content

class MinecraftModal(discord.ui.Modal, title='Minecraft proof generator'):
    gifteridd = discord.ui.TextInput(
        label="Gifter's ID (leave empty for yours)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )

    receiveridd = discord.ui.TextInput(
        label="Receiver's ID (leave empty for random)",
        style=discord.TextStyle.short,
        placeholder='12345678901234567890',
        required=False,
    )

    receivertext = discord.ui.TextInput(
        label="Receiver's message",
        style=discord.TextStyle.short,
        placeholder='OMG! Thanks!',
        required=True,
    )


    async def on_submit(self, interaction: discord.Interaction):
        self.note = ""
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 


            self.gifter = interaction.user
            if self.gifteridd.value != "":
                try:
                    self.gifter = await client.fetch_user(int(self.gifteridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"
            if self.gifter.global_name == None:
                self.gifter_globalname = self.gifter.name
            else:
                self.gifter_globalname = self.gifter.global_name


            members = await interaction.guild.chunk()
            self.receiver = random.choice(members)
            if self.receiveridd.value != "":
                try:
                    self.receiver = await client.fetch_user(int(self.receiveridd.value))
                except:
                    self.note = "Note: Invalid Receiver ID"


            if self.receiver.global_name == None:
                self.receiver_globalname = self.receiver.name
            else:
                self.receiver_globalname = self.receiver.global_name

            self.receiver_message = self.receivertext.value

            if not self.gifter.avatar:
                self.gifter_avatar = self.gifter.default_avatar.url
            else:
                self.gifter_avatar = self.gifter.avatar.url

            if not self.receiver.avatar:
                self.receiver_avatar = self.receiver.default_avatar.url
            else:
                self.receiver_avatar = self.receiver.avatar.url

            times = generate_time_range(interaction)

            self.timestamp_1 = times[0]
            self.timestamp_2 = times[1]
            self.full_date = times[2]
            proof = MinecraftPage(self.gifter_globalname, self.receiver_globalname, self.receiver_message, self.gifter_avatar, self.receiver_avatar, self.timestamp_1, self.timestamp_2, self.full_date).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()
            
            await page.setViewport({'width': 1300, 'height': 500})

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.goto(absolute_path)
            screenshot_options = {
                'path': 'proof.png',
                'clip': {
                    'x': random.randint(1, 8),
                    'y': random.randint(170, 180),
                    'width': random.randint(850, 1100),
                    'height': random.randint(300,320)
                }
            }
            await page.screenshot(screenshot_options)
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description="> **Please check your DMs!**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure you provided valid information and try again.**\n**> Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof for a minecraft giveaway.')
async def minecraftproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(MinecraftModal())

class BoostsPage:
    def __init__(self, channel_name, gifter_username, timestamp_1, full_date):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""

        self.channel_name = channel_name.replace('<', '').replace('>', '').replace('script', '')

        self.gifter_username = gifter_username.replace('<', '').replace('>', '').replace('script', '')

        self.timestamp_1 = timestamp_1
        self.full_date = full_date
        if self.full_date.startswith('0'):
            self.full_date = self.full_date.replace('0', '', 1)
            

    def get_proof(self):
        filename = "assets/boostproof.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('CHANNEL_NAME', self.channel_name)
            self.html_content = self.html_content.replace('BOOSTER_USERNAME', self.gifter_username)
            self.html_content = self.html_content.replace('TIMESTAMP_1', f'Today at {self.timestamp_1}')
            self.html_content = self.html_content.replace('FULL_DATE', self.full_date)
        return self.html_content

class BoostsModal(discord.ui.Modal, title='14x Boosts proof generator'):
    gifter = discord.ui.TextInput(
        label="Booster Username (leave empty for yours)",
        placeholder=".gg/proofgen",
        style=discord.TextStyle.short,
        required=False,
    )

    channel_name = discord.ui.TextInput(
        label='Channel name (leave empty for general)',
        style=discord.TextStyle.short,
        placeholder='general',
        required=False,
        max_length=32,
    )


    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 

            if self.gifter.value == "" :
                self.gifter = interaction.user
                if self.gifter.global_name == None:
                    self.gifter_globalname = self.gifter.name
                else:
                    self.gifter_globalname = self.gifter.global_name
            else:
                self.gifter_globalname = self.gifter.value
            
            if self.channel_name.value == "":
                self.channelname = "general"
            else:
                self.channelname = self.channel_name.value

            times = generate_time_range(interaction)

            self.timestamp_1 = times[0]
            self.full_date = times[2]
            proof = BoostsPage(self.channelname, self.gifter_globalname, self.timestamp_1, self.full_date).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()
            
            await page.setViewport({'width': 1350, 'height': 700})

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.goto(absolute_path)
            screenshot_options = {
                'path': 'proof.png',
                'clip': {
                    'x': 0,
                    'y': 140,
                    'width': 950,
                    'height': 550
                }
            }
            await page.screenshot(screenshot_options)
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description="> **Please check your DMs!**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure you provided valid information and try again.**\n**> Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof for a 14x boost sale.')
async def boostsproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(BoostsModal())


class InventoryPage:
    def __init__(self, gifter_username, nitro_amount, basic_amount):
        self.actual_datetime = datetime.datetime.now()
        self.proof = ""

        self.gifter_username = gifter_username.replace('<', '').replace('>', '').replace('script', '')

        self.nitro_amount = nitro_amount.replace('<', '').replace('>', '').replace('script', '')
        self.basic_amount = basic_amount.replace('<', '').replace('>', '').replace('script', '')

    def get_proof(self):
        filename = "assets/inventorypage.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('USERNAME', self.gifter_username)
            self.html_content = self.html_content.replace('BOOSTAMOUNT', self.nitro_amount)
            self.html_content = self.html_content.replace('BASICAMOUNT', self.basic_amount)
        return self.html_content

class InventoryModal(discord.ui.Modal, title='14x Boosts proof generator'):
    gifter = discord.ui.TextInput(
        label="Username (leave empty for yours)",
        placeholder="mahdi1337",
        style=discord.TextStyle.short,
        required=False,
    )

    nitro_amount = discord.ui.TextInput(
        label='Boost amount',
        style=discord.TextStyle.short,
        placeholder='10',
        required=False,
        max_length=32
    )

    basic_amount = discord.ui.TextInput(
        label='Basic amount',
        style=discord.TextStyle.short,
        placeholder='10',
        required=False,
        max_length=32
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 

            if self.gifter.value == "" :
                self.gifter = interaction.user
                if self.gifter.global_name == None:
                    self.gifter_globalname = self.gifter.name
                else:
                    self.gifter_globalname = self.gifter.global_name
            else:
                self.gifter_globalname = self.gifter.value

            proof = InventoryPage(self.gifter_globalname, self.nitro_amount.value, self.basic_amount.value).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()
            
            await page.setViewport({'width': 1350, 'height': 1100})

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.goto(absolute_path)
            screenshot_options = {
                'path': 'proof.png',
                'clip': {
                    'x': 0,
                    'y': 0,
                    'width': 1070,
                    'height': 1150
                }
            }
            await page.screenshot(screenshot_options)
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description="> **Please check your DMs!**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure you provided valid information and try again.**\n**> Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof of a gift inventory.')
async def inventoryproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(InventoryModal())



class PaypalPage:
    def __init__(self, amount, receiver):
        if ',' not in amount:
            amount += ',00'
        if '.' in amount:
            amount.replace('.', ',')
        if '$' in amount:
            amount.replace('$', '')
        self.amount = amount
        self.receiver = receiver

    def get_proof(self):
        filename = "assets/paypal_page.html"
        
        with open(filename, 'r', encoding="utf-8") as file:
            self.html_content = file.read()
            self.html_content = self.html_content.replace('AMOUNT', self.amount)
            self.html_content = self.html_content.replace('RECEIVER', self.receiver)
        return self.html_content

class PaypalModal(discord.ui.Modal, title='Paypal transaction proof generator'):
    gifter = discord.ui.TextInput(
        label="Receiver Name",
        placeholder="mahdi",
        style=discord.TextStyle.short,
        required=True,
    )

    nitro_amount = discord.ui.TextInput(
        label='Amount',
        style=discord.TextStyle.short,
        placeholder='10',
        required=True,
        max_length=32
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False, thinking=True) 

            proof = PaypalPage(self.nitro_amount.value, self.gifter.value).get_proof()
            with open("assets/temp.html", "w", encoding="utf-8") as f:
                f.write(proof)
                
            browser = await pyppeteer.launch(executablePath="chrome-win64/chrome.exe")
            page = await browser.newPage()

            absolute_path = f'file://{os.path.abspath("assets/temp.html")}'
            await page.setViewport({'width': 1280, 'height': 1024})
            await page.goto(absolute_path)
            await page.screenshot({'path': 'proof.png', 'fullPage': True})
            await browser.close()
            
            embed = discord.Embed(color=0x717CDA, title="Success", description="> **Please check your DMs!**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            await interaction.user.send(file=discord.File('proof.png'))
            
        except Exception:
            embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! Something went wrong, please make sure you provided valid information and try again.**\n**> Check out <#1256873254153355326> for comon errors and solutions.**")
            embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
            embed.set_footer(text="PekkleDev")
            await interaction.followup.send(embed=embed)
            traceback.print_exc()

@client.tree.command(description='Generate proof of a paypal transaction.')
async def paypalproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    await interaction.response.send_modal(PaypalModal())






@client.tree.command(description='See all the proof generator commands.')
async def proof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    embed = discord.Embed(color=0x717CDA, title="Proof Generator", description="""
> **/nitroproof**
> **/inventoryproof**
> **/robuxproof**
> **/minecraftproof**
> **/paypalproof**
                                           
> ~~**/bloxfruitsproof**~~ - COMING SOON
> ~~**/cashappproof**~~ - COMING SOON
""")
    embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
    embed.set_footer(text="PekkleDev")
    await interaction.response.send_message(embed=embed, delete_after=10)

@client.tree.command(description='See all the proof generator commands.')
async def help(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(color=0x717CDA, title="Error", description="> **Oops! You can't use this command here. Please go to <#1256872146525749329>.**")
        embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
        embed.set_footer(text="PekkleDev")
        await interaction.response.send_message(embed=embed)
        return
    embed = discord.Embed(color=0x717CDA, title="Proof Generator", description="""
> **/nitroproof**
> **/inventoryproof**
> **/robuxproof**
> **/minecraftproof**
> **/paypalproof**
                                           
> ~~**/bloxfruitsproof**~~ - COMING SOON
> ~~**/cashappproof**~~ - COMING SOON
""")
    embed.set_image(url="https://eu-central.storage.cloudconvert.com/tasks/fdd4b55f-0f2c-4ebd-8fcc-76aca2ba5049/Sanrio_Characters_Pekkle_Image002%20%281%29.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=cloudconvert-production%2F20241024%2Ffra%2Fs3%2Faws4_request&X-Amz-Date=20241024T155233Z&X-Amz-Expires=86400&X-Amz-Signature=150afffe92ba7e3b7315f782c9db3cc34ceb20bbf77e1429237792cc07a899b1&X-Amz-SignedHeaders=host&response-content-disposition=inline%3B%20filename%3D%22Sanrio_Characters_Pekkle_Image002%20%281%29.png%22&response-content-type=image%2Fpng&x-id=GetObject")
    embed.set_footer(text="PekkleDev")
    await interaction.response.send_message(embed=embed, delete_after=10)

client.run(token)
