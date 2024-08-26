import discord
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.context import ComponentContext, MenuContext
import Winsy

async def main(slash, all_guilds, conn, error_channel):
	print('Slash starting')
	@slash.slash(
    name='youtube',
    description=
    'Choose the file format and quality of a YT video which you desire to download',
    guild_ids=all_guilds,
    options=[
        create_option(
          name='url',
          description='URL of the video',
          required=True,
          option_type=3
        )
    ])
	async def _yt(ctx: SlashContext, url: str):
		await Winsy.yt(ctx=ctx, url=url)

	@slash.slash(name='insta',
             description='Download instagram media in simplest ways',
             guild_ids=all_guilds,
             options=[
                 create_option(
                  name='url',
                  description='URL of the post/media',
                  required=True,
                  option_type=3
                )
      ])
	async def _insta(ctx: SlashContext, url: str):
		await Winsy.insta(ctx=ctx, url=url)

	@slash.slash(
    name='update_error_msg',
    description='Update the insta error msg',
    guild_ids=all_guilds,
    options=[
        create_option(
          name='msg',
          description='Dialogue of the msg',
          required=True,
          option_type=3
        ),
        create_option(
          name='emoji',
          description=
          'Emoji which will be used at the end of the message (optional)',
          required=False,
          option_type=3
        )
    ])
	async def error_msg_update(ctx, msg: str, emoji=None):
		if ctx.author.id == Winsy.my_id:
			cursor = conn.cursor()
			try:
				if emoji == None:
					cursor.execute(
						"""UPDATE insta_error SET Dialogue = ?, Emoji = ? WHERE type = ?""",
						[msg, 0, 'main'])
				else:
					cursor.execute(
						"""UPDATE insta_error SET Dialogue = ?, Emoji = ? WHERE type = ?""",
						[msg, emoji.split(":")[-1][:-2], 'main'])
				conn.commit()
				cursor.close()
				await ctx.send("Database updated successfully ✅")
			except Exception as e:
				await ctx.send(
					"There was an error updating the database, please check error logs"
				)
				embed = discord.Embed(
					title='Error raised during a process',
					description=
					"Couldn't update the database of `insta error_msg`, the error being:\n{}"
					.format(e),
					color=0xe80e32)
				await error_channel.send(embed=embed)

	@slash.slash(
    name='remove_godmute_command_owner',
    description=
    'Remove a member from being able to Godmute others\nCan only be used by Owner',
    guild_ids=all_guilds,
    options=[
        create_option(name='user',
                      description='Select the User',
                      required=True,
                      option_type=6)
    ])
	async def removegodmuteowner(ctx: SlashContext, user: discord.Member):
		guild_id = ctx.guild.id
		if guild_id not in Winsy.ignored.guilds:
			Winsy.ignored.addguild(guild_id)
		if ctx.author.id in Winsy.ignored.guilds[guild_id]:
			return
		else:
			if ctx.author.id != Winsy.my_id:
				await ctx.send("You can't use this command.")
				return
			if not Winsy.Godmute.is_present(id=user.id, _as='owner'):
				await ctx.send("The user is not an Owner.")
				return

			Winsy.Godmute.owners.pop(Winsy.Godmute.owners.index(user))
			await ctx.send("User is no longer an ignore command owner.")

	@slash.slash(
		name='make_godmute_command_owner',
		description='Make a member able to Godmute others\nCan only be used by Owner',
		guild_ids=all_guilds,
		options=[create_option(name='user',
					description='Select the User',
					required=True,
					option_type=6)
		]
	)
	async def godmuteowner(ctx: SlashContext, user: discord.Member):
		guild_id = ctx.guild.id
		if guild_id not in Winsy.ignored.guilds:
			Winsy.ignored.addguild(guild_id)
		if ctx.author.id in Winsy.ignored.guilds[guild_id]:
			return
		else:
			if ctx.author.id != Winsy.my_id:
				await ctx.send("You can't use this command.")
				return
			if Winsy.Godmute.is_present(id=user.id, _as='owner'):
				await ctx.send("The user is already an Owner.")
				return

			if Winsy.Godmute.is_present(id=user.id, _as='member'):
				await ctx.send('The person is currently Godmuted, unmute them first to make em the Owner')
				return

			Winsy.Godmute.add_user(member=user, _as='owner')
			await ctx.send("The member was successfully added as a Godmute cmd `owner`.")

	@slash.slash(
		name='clear_Godmute_list',
		description='Clear the list of Godmute users.',
		guild_ids=all_guilds
	)
	async def clear_Godmute(ctx: SlashContext):
		if Winsy.Godmute.is_present(id=ctx.author.id, _as='owner'):
			Winsy.Godmute.members.clear()
			await ctx.send('Cleared✅')

	@slash.slash(
		name='ping',
		description='Check bot latency',
		guild_ids=all_guilds
	)
	async def _ping(ctx: SlashContext):
		await Winsy.ping(ctx)

	@slash.slash(
		name='purge',
		description='Delete some clutter from your channel',
		guild_ids=all_guilds,
		options=[
			create_option(
				name="amount",
				description="Mention the amount of messages you wanna clear",
				required=True,
				option_type=4
			)
		]
	)
	async def _purge(ctx: SlashContext, amount: int=None):
		await Winsy.purge(ctx, amount=amount, slash=True)

	@slash.slash(
		name='spam',
		description='Spam a user for 10 times.',
		guild_ids=all_guilds,
		options=[
			create_option(
				name="user",
				description="Select the user to be spammed",
				required=True,
				option_type=6
			),
			create_option(
				name="message",
				description='Write the message (optional)',
				required=False,
				option_type=3
			)
		]
	)
	async def _spam(ctx: SlashContext, user: discord.Member, message: str=""):
		await Winsy.spam(ctx, member=user, message=message)

	@slash.slash(
		name='ignore_owner_list',
		description='Check out the list of owners of `ignore` command.',
		guild_ids=all_guilds
	)
	async def _ignoreownerlist(ctx: SlashContext):
		await Winsy.ignoreownerlist(ctx)

	@slash.slash(
		name='ignored_members_list',
		description="Check out the list of members who don't have access of bot's commands",
		guild_ids=all_guilds
	)
	async def _ignorelist(ctx: SlashContext):
		await Winsy.ignorelist(ctx)

	@slash.slash(
		name='ignore',
		description='Add a user in the "ignored" list (you need to be an ignored command owner).',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the user.',
				required=True,
				option_type=6
			)
		]
	)
	async def _ignore(ctx: SlashContext, user: discord.Member):
		await Winsy.ignore(ctx, member=user)

	@slash.slash(
		name='unignore',
		description='Remove a user from the ignored members list',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the user.',
				required=True,
				option_type=6
			)
		]
	)
	async def _unignore(ctx: SlashContext, user: discord.Member):
		await Winsy.unignore(ctx, member=user)

	@slash.slash(
		name='clear_ignorelist',
		description='Clear the entire ignored list.',
		guild_ids=all_guilds
	)
	async def _clearignorelist(ctx: SlashContext):
		await Winsy.clearignorelist(ctx)

	@slash.slash(
		name='roast',
		description='Roast someone :P',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the user to roast.',
				required=True,
				option_type=6
			)
		]
	)
	async def _roast(ctx: SlashContext, user: discord.Member):
		await Winsy.roast(ctx, member=user)

	@slash.slash(
		name='laugh_at',
		description='Laugh at someone',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the user to laugh at.',
				required=True,
				option_type=6
			)
		]
	)
	async def _laugh(ctx: SlashContext, user: discord.Member):
		await Winsy.laugh(ctx,at='at', member=user)

	@slash.slash(
		name='mute',
		description='Mute some chumps😎',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the chump to mute.',
				required=True,
				option_type=6
			)
		]
	)
	async def _mute(ctx: SlashContext, user: discord.Member):
		await Winsy.mute(ctx, member=user)

	@slash.slash(
		name='unmute',
		description='Unmute those poor souls',
		guild_ids=all_guilds,
		options=[
			create_option(
				name='user',
				description='Choose the poor soul to unmute.',
				required=True,
				option_type=6
			)
		]
	)
	async def _unmute(ctx: SlashContext, user: discord.Member):
		await Winsy.unmute(ctx, member=user)
		
	print('Slash registered')