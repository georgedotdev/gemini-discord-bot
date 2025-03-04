import configs.DefaultConfig as DefaultConfig

#function to make sure the owner can execute and confirms the user has the owners id
def is_me(ctx):
    return ctx.author.id == int(DefaultConfig.DISCORD_OWNER_ID)

