from django.core.management.base import BaseCommand, CommandError
import os
from app.bot import run

class Command(BaseCommand):
    help = 'Runs the discord bot'

    def add_arguments(self, parser):
        parser.add_argument('--token', help="The token for your bot", type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Bot] - Bot has started..."))

        if "token" in options and options["token"]:
            run(options["token"])
        elif 'DISCORDBOT_TOKEN' in os.environ:
            run(os.environ.get('DISCORDBOT_TOKEN'))
        else:
            self.stdout.write(self.style.ERROR("[Bot] - No TOKEN found!"))

        self.stdout.write(self.style.SUCCESS("[Bot] - Bot has been terminated!"))
