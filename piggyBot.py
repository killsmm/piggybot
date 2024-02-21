import datetime
from discord.ext import commands
import discord.ext
import bookKeeper

ACCOUNTS = {
    'admin': '0012', #admin password is used to deposit and withdraw
    'shanshan': '1234',
    'yiyi': '1234',
    'baba': '1234',
    'mama': '1234',
}

class PiggyBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.bookkeeper = bookKeeper.BookKeeper()
        for account, password in ACCOUNTS.items():
            if not self.bookkeeper.get_account(account):
                self.bookkeeper.create_account(account, password)


    async def on_command_error(self, context, error) -> None:
        return await super().on_command_error(context, error)
        
    def check_password(self, username, password):
        account = self.bookkeeper.get_account(username)
        if account is None:
            return False
        return account.password == password

    @staticmethod
    def get_instance():
        bot = PiggyBot(command_prefix='.')

        @bot.hybrid_command
        async def ping(ctx):
            await ctx.send('pong')

        # @bot.hybrid_command()
        # async def create_account(ctx, username, password):
        #     bot.bookkeeper.create_account(username, password)
        #     await ctx.send(f'Account {username} created')

        # @bot.hybrid_command()
        # async def delete_account(ctx, username):
        #     if not bot.bookkeeper.get_account(username):
        #         await ctx.send(f'Account {username} does not exist')
        #         return
        #     bot.bookkeeper.delete_account(username)
        #     await ctx.send(f'Account {username} deleted')
        
        @bot.hybrid_command()
        async def check_balance(ctx, username):
            if not bot.bookkeeper.get_account(username):
                await ctx.send(f'Account {username} does not exist')
                return
            balance = bot.bookkeeper.get_balance(username)
            await ctx.send(f'Balance: {balance}')

        @bot.hybrid_command()
        async def deposit(ctx, username, amount, admin_password, note):
            if not bot.bookkeeper.get_account(username):
                await ctx.send(f'Account {username} does not exist')
                return
            if not bot.check_password('admin', admin_password):
                await ctx.send(f'Password is incorrect')
                return
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            bot.bookkeeper.deposit(username, amount, date, note)
            await ctx.send(f'{username}: Deposit of {amount} made')

        @bot.hybrid_command()
        async def withdraw(ctx, username, amount, admin_password, note):
            if not bot.bookkeeper.get_account(username):
                await ctx.send(f'Account {username} does not exist')
                return
            if not bot.check_password('admin', admin_password):
                await ctx.send(f'Password is incorrect')
                return
            balance = bot.bookkeeper.get_balance(username)
            if balance < float(amount):
                await ctx.send(f'Insufficient balance: you only have {balance}')
                return
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            bot.bookkeeper.withdraw(username, amount, date, note)
            await ctx.send(f'{username}: Withdrawal of {amount} made')

        @bot.hybrid_command()
        async def check_balance_all(ctx):
            accounts = bot.bookkeeper.get_all_accounts()
            text = ''
            for account in accounts:
                balance = bot.bookkeeper.get_balance(account)
                text += f'{account}: {balance}\n'
            await ctx.send(text)


        @bot.event
        async def on_ready():
            print(f'logged in successfully as {bot.user.name} ({bot.user.id}, ')
            await bot.tree.sync()

        return bot
    
    
