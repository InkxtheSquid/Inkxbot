import asyncio
import aiohttp
import time

from time import gmtime, strftime
import logging
import json

from discord.ext import commands
import discord

log = logging.getLogger()


def mode_key(argument):
    lower = argument.lower().strip('"')
    if lower.startswith('rank'):
        return 'Ranked Battle'
    elif lower.startswith('turf') or lower.startswith('regular'):
        return 'Regular Battle'
    elif lower == 'league':
        return 'League Battle'
    elif lower == 'season':
        return 'X rank'
    elif lower == 'zones':
        return 'Zones'
    elif lower == 'tower':
        return 'Tower'
    elif lower == 'rainmaker':
        return 'Rainmaker'
    elif lower == 'clam':
        return 'Clam'
    else:
        raise commands.BadArgument('Unknown schedule type, try: "ranked", "season", "regular", or "league"')

def region_key(argument):
    lower = argument.lower().strip('"') 
    if lower.startswith('us') or lower.startswith('usa'):
        return 'The United States'
    elif lower.startswith('eu') or lower.startswith('europe'):
        return 'Europe'
    elif lower.startswith('jpn') or lower.startswith('japan'):
        return 'Japan'
    else:
        raise commands.BadArgument('Unknown region type, try: "usa", "europe", or "japan"')


def clouts():
    with open('mapcallouts.json') as m:
        return json.load(m)

def sr_mapredirect():
    with open('srmaps.json') as sr:
        return json.load(sr)

def map_key(argument):
    return

class Splatoon(commands.Cog):
    """Splatoon 2 related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.taskupdater = bot.loop.create_task(self.splatnet_clock())

    def __unload(self):
        self.taskupdater.cancel()

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(error)

    async def load_schedule(self):
        async with self.bot.aio_session.get("https://splatoon.ink/schedule2.json") as url:
            return await url.json()

    async def load_sr(self):
        async with self.bot.aio_session.get("https://splatoon2.ink/data/coop-schedules.json") as srurl:
            srurl.seek(0)
            return await srurl.json(content_type='text/html')

    async def load_festival(self):
        async with self.bot.aio_session.get("https://splatoon2.ink/data/festivals.json") as festurl:
            return await festurl.json(content_type='text/html')

    async def load_gear(self):
        async with self.bot.aio_session.get("https://splatoon2.ink/data/merchandises.json") as gearurl:
            gearurl.seek(0)
            return await gearurl.json(content_type='text/html')

    async def splatnet(self):
        ss = '<:ss:464545843077316608>'
        swim = '<:ssu:456283088507633664>'
        run = '<:rsu:456283043640901633>'
        qr = '<:qr:456283022233305110>'
        rp = '<:rp:464544035667705877>'
        h = '<:haunt:456282919141376000>'
        iru = '<:iru:464545966154973205>'
        ism = '<:ism:456282944676429865>'
        iss = '<:iss:456282966877011968>'
        scu = '<:scu:456283060573437953>'
        subpow = '<:spu:464545070347976714>'
        qsj = '<:qsj:456283032765333504>'
        specpow = '<:spu:456283073881964544>'
        inkres = '<:inkres:456282934979330059>'
        bdef = '<:bdu:456282725033181190>'
        cb = '<:cb:456282763520245775>'
        og = '<:og:464543533748191232>'
        lde = '<:lde:456282978931310612>'
        tena = '<:tenacity:456283111710261248>'
        cbk = '<:comeback:456282893136691200>'
        ns = '<:ns:464544322071691274>'
        therm = '<:ti:464544226131312641>'
        sj = '<:sj:464544423485636610>'
        os = '<:os:456282995289227275>'
        dr = '<:dr:456282900627849226>'
        gearjson = await self.load_gear()
        dict = gearjson
        newgear = dict["merchandises"][5]
        gearname = newgear['gear']['name']
        gearthumb = newgear['gear']['image']
        gearprice = str(newgear['price'])
        gearabillity = newgear['skill']['name']
        assets = 'https://splatoon2.ink/assets/splatnet'
        link = assets + gearthumb
        #ids are kinda the key to show the abillity, thermal ink is 106
        if gearabillity == 'Ink Saver (Main)':
            emoji = ism
        elif gearabillity == 'Ink Saver (Sub)':
            emoji = iss
        elif gearabillity == 'Ink Recovery Up':
            emoji = iru
        elif gearabillity == 'Run Speed Up':
            emoji = run
        elif gearabillity == 'Swim Speed Up':
            emoji = swim
        elif gearabillity == 'Special Charge Up':
            emoji = scu
        elif gearabillity == 'Special Saver':
            emoji = ss
        elif gearabillity == 'Special Power Up':
            emoji = specpow
        elif gearabillity == 'Quick Respawn':
            emoji = qr
        elif gearabillity == 'Quick Super Jump':
            emoji = qsj
        elif gearabillity == 'Sub Power Up':
            emoji = subpow
        elif gearabillity == 'Ink Resistance Up':
            emoji = inkres
        elif gearabillity == 'Bomb Defense Up':
            emoji = bdef
        elif gearabillity == 'Cold-Blooded':
            emoji = cb
        elif gearabillity == 'Comeback':
            emoji = cbk
        elif gearabillity == 'Opening Gambit':
            emoji = og
        elif gearabillity == 'Last-Ditch Effort':
            emoji = lde
        elif gearabillity == 'Tenacity':
            emoji = tena
        elif gearabillity == 'Ninja Squid':
            emoji = ns
        elif gearabillity == 'Haunt':
            emoji = h
        elif gearabillity == 'Thermal Ink':
            emoji = therm
        elif gearabillity == 'Respawn Punisher':
            emoji = rp
        elif gearabillity == 'Stealth Jump':
            emoji = sj
        elif gearabillity == 'Object Shredder':
            emoji = os
        elif gearabillity == 'Drop Roller':
            emoji = dr
        em = discord.Embed(title=gearname)
        em.add_field(name='Price:', value='<:coin:476145275082244106>'+gearprice)
        em.add_field(name='Abillity:', value=emoji+gearabillity)
        em.set_thumbnail(url=link)
        em.set_footer(text="Data obtained from splatoon2.ink")
        channel = discord.utils.get(guilds.channels, name='splatnet')
        await channel.send(embed=em)
        await asyncio.sleep(60)

    async def alltypes_map_schedule(self, ctx, number):
        splatoonjson = await self.load_schedule()
        dict = splatoonjson
        regular = dict['modes']['regular']
        ranked  = dict['modes']['gachi']
        league  = dict['modes']['league']
        regmaps = regular[number]['maps']
        sch = dict['modes']['gachi'][1]
        rnk = ranked[number]
        lge = league[number]
        rnkmd = rnk['rule']['name']
        lgemd = lge['rule']['name']
        rnkmaps = rnk['maps']
        lgemaps = lge['maps']
        t1 = regmaps[0]
        t2 = regmaps[1]
        r1 = rnkmaps[0]
        r2 = rnkmaps[1]
        l1 = lgemaps[0]
        l2 = lgemaps[1]
        epoch = sch['startTime']
        #If we want to get the time remaining, we have to subtract the current epoch from the epoch recived
        timelef = gmtime(epoch-time.time())
        #now we have the time remaining
        hourlef = strftime('%H', timelef)
        minlef = strftime('%M', timelef)
        if int(hourlef) == 1:
            hour = strftime(" %H hour ", timelef)
        elif int(hourlef) == 0:
            hour = " "
        else:
            hour = strftime(" %H hours ", timelef)
        if int(minlef) == 1:
            mins = strftime("%M minute ", timelef)
        else:
            mins = strftime("%M minutes ", timelef)
        secs = strftime("%S seconds", timelef)
        if number == 0:
            titlename = f'For{hour}{mins}{secs}...'
        else:
            titlename = f'In{hour}{mins}{secs}...'
        desc = "**Ranked Battle** \n*__{0}:__* {1} and {2} \n".format(rnkmd, r1, r2) + "**League Battle** \n*__{0}:__* {1} and {2} \n".format(lgemd, l1, l2) + "**Regular Battle** \n*__Turf War:__* {0} and {1} \n".format(t1, t2)
        sched_embed = discord.Embed(title=titlename, description=desc, color=0x006AFF)
        sched_embed.set_footer(text="For the maps for the X rank season, do `,maps season`")
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)

    async def modetype_splatoon2_schedule(self, ctx, mode):
        ZONES_MAPS     = 'https://pbs.twimg.com/media/D0dgw9KVsAA4wrd.jpg'
        TOWER_MAPS     = 'https://pbs.twimg.com/media/D0dgyLrU4AUfWXi.jpg'
        RAINMAKER_MAPS = 'https://pbs.twimg.com/media/D0dgzK3VYAALZ8y.jpg'
        CLAM_MAPS      = 'https://pbs.twimg.com/media/D0dgzzKV4AAq-7v.jpg'
        splatoonjson = await self.load_schedule()
        dict = splatoonjson
        if mode == 'Ranked Battle':
            md = 'Ranked'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'League Battle':
            md = 'League'
            basebatt = 'league'
            co = 0xFF004C
        elif mode == 'Regular Battle':
            md = 'Regular Battle'
            basebatt = 'regular'
            co = 0x4DFF00
        elif mode == 'X rank':
            md = 'Xrank'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'Zones':
            md = 'Splat Zones'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'Tower':
            md = 'Tower Control'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'Rainmaker':
            md = 'Rainmaker'
            basebatt = 'gachi'
            co = 0xFF6F00
        elif mode == 'Clam':
            md = 'Clam Blitz'
            basebatt = 'gachi'
            co = 0xFF6F00
        else:
            log.info('something fucked up... fix it?')

        sch = dict['modes'][basebatt]
        sch1 = sch[0]
        sch2 = sch[1]
        sch3 = sch[2]
        schmd1 = sch1['rule']['name']
        schmd2 = sch2['rule']['name']
        schmd3 = sch3['rule']['name']
        sone1 = sch1['maps'][0]
        sone2 = sch1['maps'][1]
        stwo1 = sch2['maps'][0]
        stwo2 = sch2['maps'][1]
        sthr1 = sch3['maps'][0]
        sthr2 = sch3['maps'][1]
        #When will the rotation end? We'll find out by getting the epoch first
        epoch2 = sch2['startTime']
        epoch3 = sch3['startTime']
        #If we want to get the time remaining, we have to subtract the current epoch from the epoch recived
        time2 = gmtime(epoch2-time.time())
        time3 = gmtime(epoch3-time.time())
        #now we have the time remaining
        hour2 = strftime('%H', time2)
        hour3 = strftime('%H', time3)
        minlef = strftime('%M', time2)
        if int(hour2) == 1:
            hour = strftime("In %H hour ", time2)
        elif int(hour2) == 0:
            hour = "In "
        else:
            hour = strftime("In %H hours ", time2)
        if int(minlef) == 1:
            mins = strftime("%M minute ", time2)
        else:
            mins = strftime("%M minutes ", time2)
        secs = strftime("%S seconds", time2)
        tl2 = f"{hour}{mins}{secs}"
        tl3 = f"In {hour3} hours {mins}{secs}"
        tlx2 = strftime("%Hh & %Mm", time2)
        tlx3 = strftime("%Hh & %Mm", time3)

        if md == 'Xrank':
            if schmd1 == 'Splat Zones':
                imageurl = ZONES_MAPS
            elif schmd1 == 'Tower Control':
                imageurl = TOWER_MAPS
            elif schmd1 == 'Rainmaker':
                imageurl = RAINMAKER_MAPS
            elif schmd1 == 'Clam Blitz':
                imageurl = CLAM_MAPS
            else:
                imageurl = None
            sched_embed = discord.Embed(title='This Season for X rank', color=co)
            sched_embed.add_field(name='Schedule', value=f'Current: {schmd1}\n{tlx2}: {schmd2}\n{tlx3}: {schmd3}')
            sched_embed.add_field(name='Season maps', value='Maps for '+schmd1+' are in the image below')
            sched_embed.set_image(url=imageurl)
        elif md == 'Splat Zones':
            imageurl = ZONES_MAPS
            sched_embed = discord.Embed(title='The X rank maps for '+md+' are', color=co)
            sched_embed.set_image(url=imageurl)
        elif md == 'Tower Control':
            imageurl = TOWER_MAPS
            sched_embed = discord.Embed(title='The X rank maps for '+md+' are', color=co)
            sched_embed.set_image(url=imageurl)
        elif md == 'Rainmaker':
            imageurl = RAINMAKER_MAPS
            sched_embed = discord.Embed(title='The X rank maps for '+md+' are', color=co)
            sched_embed.set_image(url=imageurl)
        elif md == 'Clam Blitz':
            imageurl = CLAM_MAPS
            sched_embed = discord.Embed(title='The X rank maps for '+md+' are', color=co)
            sched_embed.set_image(url=imageurl)
        else:
            desc = f"**Current Rotation** \n*__{schmd1}:__* {sone1} and {sone2} \n**{tl2}** \n*__{schmd2}:__* {stwo1} and {stwo2} \n**{tl3}** \n*__{schmd3}:__* {sthr1} and {sthr2} \n"
            sched_embed = discord.Embed(title='Map Schedule for {} in Splatoon 2'.format(md), description=desc, color=co)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=sched_embed)


    async def splatnet_clock(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                if time.strftime('%H:%M',time.gmtime()) == '02:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '00:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '04:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '06:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '08:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '10:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '12:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '14:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '16:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '18:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '20:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '22:01':
                    await self.splatnet()
                elif time.strftime('%H:%M',time.gmtime()) == '24:01':
                    await self.splatnet()
                elif time.strftime('%M',time.gmtime()) == '17':
                    await self.splatnet()
                else:
                    await asyncio.sleep(10)
            except:
                pass

    
    async def festival(self,ctx,region):
        splatoonjson = await self.load_schedule()
        sch = splatoonjson['modes']['regular']
        if region == 'The United States':
            rg = 'na'
            basereg = 'na'
        elif region == 'Europe':
            rg = 'eu'
            basereg = 'eu'
        elif region == 'Japan':
            rg = 'jp'
            basereg = 'jp'
        else:
            log.info('something fucked up... fix it?')
        sch1 = sch[0]
        sch2 = sch[1]
        sch3 = sch[2]
        schmd1 = sch1['rule']['name']
        schmd2 = sch2['rule']['name']
        schmd3 = sch3['rule']['name']
        sone1 = sch1['maps'][0]
        sone2 = sch1['maps'][1]
        stwo1 = sch2['maps'][0]
        stwo2 = sch2['maps'][1]
        sthr1 = sch3['maps'][0]
        sthr2 = sch3['maps'][1]
        #When will the rotation end? We'll find out by getting the epoch first
        epoch2 = sch2['startTime']
        epoch3 = sch3['startTime']
        #If we want to get the time remaining, we have to subtract the current epoch from the epoch recived
        time2 = gmtime(epoch2-time.time())
        time3 = gmtime(epoch3-time.time())
        #now we have the time remaining
        tl2 = strftime("%Hh & %Mm", time2)
        tl3 = strftime("%Hh & %Mm", time3)
        festsch = await self.load_festival()
        dict = festsch
        curtime = time.time()
        basefest = dict[rg]['festivals'][0]
        times = dict[rg]['festivals'][0]['times']
        names = dict[rg]['festivals'][0]['names']
        alpha = names['alpha_short']
        bravo = names['bravo_short']
        teams = alpha + " vs " + bravo
        imageurl = 'https://splatoon2.ink/assets/splatnet' + dict[rg]['festivals'][0]['images']['panel']
        if times['result'] < curtime:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("No Splatfest for " + region + " has been announced.")
        elif times['end'] < curtime:
            festemb = discord.Embed(title="The Splatfest for " + region + " is over! Results will come soon!", description=teams)
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        elif times['start'] < curtime:
            festemb = discord.Embed(title="The Ongoing Splatfest for " + region + ".", description=teams)
            festemb.add_field(name='Schedule', value=f'**Current Maps**: \n{sone1}, {sone2} and Shifty Station \n**{tl2}**: \n{stwo1}, {stwo2} and Shifty Station \n**{tl3}**: \n{sthr1}, {sthr2} and Shifty Station')
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        elif times['announce'] < curtime:
            festemb = discord.Embed(title="The Upcomming Splatfest for " + region + ".", description=teams)
            festemb.set_image(url=imageurl)
            festemb.set_footer(text="Data obtained from splatoon2.ink")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=festemb)
        else:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("no splatfests are coming anymore...")

        #emb = discord.Embed(title="", description=)
        #emb.set_image(url=imageurl)
        #emb.set_footer(text="Data obtained from splatoon2.ink")


    async def sr_schedule(self,ctx):
        srsch = await self.load_sr()
        dict = srsch
        images = sr_mapredirect()
        basedets = dict['details']
        schsrtime = basedets['start_time']
        curtime = time.time()
        stagename = basedets['stage']['name']
        imageurl = images[stagename]['map']
        weapons = basedets['weapons']
        w1 = weapons[0]
        w2 = weapons[1]
        w3 = weapons[2]
        w4 = weapons[3]

        if w1 == None:
            wep1 = 'Mystery'
        else:
            wep1 = w1['weapon']['name']

        if w2 == None:
            wep2 = 'Mystery'
        else:
            wep2 = w2['weapon']['name']

        if w3 == None:
            wep3 = 'Mystery'
        else:
            wep3 = w3['weapon']['name']

        if w4 == None:
            wep4 = 'Mystery'
        else:
            wep4 = w4['weapon']['name']

        if schsrtime > curtime:
            keyword = "Upcomming"
        else:
            keyword = "Ongoing"
        emb = discord.Embed(title=keyword+" shift for Salmon Run", description=stagename, color=0xFF8C00)
        emb.set_image(url=imageurl)
        emb.set_footer(text="Data obtained from splatoon2.ink")
        emb.add_field(name='Weapons', value=wep1+'\n'+wep2+'\n'+wep3+'\n'+wep4)
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=emb)


    @commands.command(aliases=['maps'])
    async def schedule(self, ctx, *, type: mode_key = None):
        """Shows the current Splatoon 2 schedule."""
        if type is None:
            num = 0
            await self.alltypes_map_schedule(ctx, num)
        else:
            await self.modetype_splatoon2_schedule(ctx, type)

    @commands.command()
    async def nextmaps(self, ctx):
        """Shows the next Splatoon 2 maps."""
        num = 1
        await self.alltypes_map_schedule(ctx, num)

    @commands.command(aliases=['sr'])
    async def salmon(self, ctx):
        await self.sr_schedule(ctx)

    @commands.command(aliases=['c'])
    async def callouts(self, ctx, mapname):
        """Posts an image of callouts in a map of Splatoon 2, ",callouts list" for the entire list of callouts"""
        files = clouts()
        try:
            clout = files[mapname]['map']
            if clout is None:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send("That's nothing in my database.")
            else:
                await ctx.trigger_typing()
                await asyncio.sleep(1)
                await ctx.send(file=discord.File(clout))
    #making it an exception for ",callouts list"
        except KeyError:
            d = "reef \nfitness \nmoray \nmako \nblackbelly \ncanal \nstarfish \nhumpback \ninkblot \nmanta \nport \nsturgeon \ndome \nwalleye \narowana \nshellendorf \ngoby \npit \npitrm \ncamp \nwahoo \nhotel \nanchov \nskipper"
            em = discord.Embed(title='List of Map Callouts', description=d, color=0xFF8C00)
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(embed=em)

    @commands.command(hidden=True)
    async def dome(self, ctx):
        await ctx.send(file=discord.File('dome.png'))

    @commands.command()
    async def splatfest(self, ctx, *, type: region_key = None):
        """Shows information about the currently running Splatfests, if any. Defaults to us."""
        if type is None:
            await self.festival(ctx,'The United States')
        else:
            await self.festival(ctx,type)

    @commands.command(hidden=True)
    async def geartest(self,ctx):
        ss = '<:ss:464545843077316608>'
        swim = '<:ssu:464544776864137218>'
        run = '<:rsu:456283043640901633>'
        qr = '<:qr:456283022233305110>'
        rp = '<:rp:464544035667705877>'
        h = '<:haunt:456282919141376000>'
        iru = '<:iru:464545966154973205>'
        ism = '<:ism:456282944676429865>'
        iss = '<:iss:456282966877011968>'
        scu = '<:scu:456283060573437953>'
        subpow = '<:spu:464545070347976714>'
        qsj = '<:qsj:456283032765333504>'
        specpow = '<:spu:456283073881964544>'
        inkres = '<:inkres:456282934979330059>'
        bdef = '<:bdu:456282725033181190>'
        cb = '<:cb:456282763520245775>'
        og = '<:og:464543533748191232>'
        lde = '<:lde:456282978931310612>'
        tena = '<:tenacity:456283111710261248>'
        cbk = '<:comeback:456282893136691200>'
        ns = '<:ns:464544322071691274>'
        therm = '<:ti:464544226131312641>'
        sj = '<:sj:464544423485636610>'
        os = '<:os:456282995289227275>'
        dr = '<:dr:456282900627849226>'
        gearjson = await self.load_gear()
        dict = gearjson
        newgear = dict["merchandises"][5]
        gearname = newgear['gear']['name']
        gearthumb = newgear['gear']['image']
        gearprice = str(newgear['price'])
        gearabillity = newgear['skill']['name']
        assets = 'https://splatoon2.ink/assets/splatnet'
        link = assets + gearthumb
        #ids are kinda the key to show the abillity, thermal ink is 106
        if gearabillity == 'Ink Saver (Main)':
            emoji = ism
        elif gearabillity == 'Ink Saver (Sub)':
            emoji = iss
        elif gearabillity == 'Ink Recovery Up':
            emoji = iru
        elif gearabillity == 'Run Speed Up':
            emoji = run
        elif gearabillity == 'Swim Speed Up':
            emoji = swim
        elif gearabillity == 'Special Charge Up':
            emoji = scu
        elif gearabillity == 'Special Saver':
            emoji = ss
        elif gearabillity == 'Special Power Up':
            emoji = specpow
        elif gearabillity == 'Quick Respawn':
            emoji = qr
        elif gearabillity == 'Quick Super Jump':
            emoji = qsj
        elif gearabillity == 'Sub Power Up':
            emoji = subpow
        elif gearabillity == 'Ink Resistance Up':
            emoji = inkres
        elif gearabillity == 'Bomb Defense Up':
            emoji = bdef
        elif gearabillity == 'Cold-Blooded':
            emoji = cb
        elif gearabillity == 'Comeback':
            emoji = cbk
        elif gearabillity == 'Opening Gambit':
            emoji = og
        elif gearabillity == 'Last-Ditch Effort':
            emoji = lde
        elif gearabillity == 'Tenacity':
            emoji = tena
        elif gearabillity == 'Ninja Squid':
            emoji = ns
        elif gearabillity == 'Haunt':
            emoji = h
        elif gearabillity == 'Thermal Ink':
            emoji = therm
        elif gearabillity == 'Respawn Punisher':
            emoji = rp
        elif gearabillity == 'Stealth Jump':
            emoji = sj
        elif gearabillity == 'Object Shredder':
            emoji = os
        elif gearabillity == 'Drop Roller':
            emoji = dr
        em = discord.Embed(title=gearname)
        em.add_field(name='Price:', value='<:coin:476145275082244106>'+gearprice)
        em.add_field(name='Abillity:', value=emoji+gearabillity)
        em.set_thumbnail(url=link)
        em.set_footer(text="Data obtained from splatoon2.ink")
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Splatoon(bot))
