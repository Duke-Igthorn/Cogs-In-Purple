@commands.command(name="msgmvr")
async def move_messages(self, ctx, dest_channel: discord.TextChannel):
    await ctx.send("Please provide the message IDs or ranges to move (separated by commas):")
    msg_ids_input = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    msg_ids = []
    for msg_id in msg_ids_input.content.split(','):
        if '-' in msg_id:
            range_start, range_end = msg_id.split('-')
            try:
                range_start = int(range_start)
            except ValueError:
                await ctx.send(f"Invalid range start value: {range_start}")
                continue
            try:
                range_end = int(range_end)
            except ValueError:
                await ctx.send(f"Invalid range end value: {range_end}")
                continue
            msg_ids += [i for i in range(range_start, range_end+1)]
        else:
            try:
                msg_ids.append(int(msg_id))
            except ValueError:
                await ctx.send(f"Invalid message ID: {msg_id}")
                continue

    for msg_id in msg_ids:
        message = await ctx.channel.fetch_message(msg_id)
        if message is None:
            await ctx.send(f"Message with ID {msg_id} not found.")
            continue

        embed = discord.Embed(
            description=message.content,
            timestamp=message.created_at
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)

        await dest_channel.send(embed=embed)
        await message.delete()

    await ctx.send("Messages moved successfully.")
