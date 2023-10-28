"""
    Service to send information through webhooks
"""
import os

from discord_webhook import DiscordWebhook, DiscordEmbed

ICON = "https://cdn.discordapp.com/attachments/1073180733369233430/1073612788469092463/Capture_decran_2023-02-10_a_15.33.51.png?ex=65328fd3&is=65201ad3&hm=8213c42738a7e2b26c5469779de18b6fd3c47d8d2af6e3642687dc54f8dffa44&"

allowed_mentions = {
    "users": ["223535717878464512"]
}

disc_webhook = DiscordWebhook(
    url=os.environ['WEBHOOK_URL'],
    rate_limit_retry=True,
    content="<@223535717878464512>",
    allowed_mentions=allowed_mentions
)


class Webhook:
    """
        Webhook class
    """

    @staticmethod
    def discord(code, message, url, user, payload, data='') -> None:
        """
            Send information to discord webhook

            Args:
                code (object): From Constants HttpResponseCodes Enum where
                    value: is the status code and
                    name: refers to error's name
                message (str): Message received from api_response
                url (str): url where the error has occurred
                user (str): the user that received the error
                payload (object): the payload that was sent
                data (str, optional): data returned by the api_response
        """
        embed = DiscordEmbed(
            title=f'⚠️ Jizo - Error {code.value} {code.name} ⚠️',
            description="🦊 Received a new error on Jizo 😭",
            color="FE1B00",
            url="https://www.youtube.com/watch?v=4Q9DWZLaY2U"
        )

        embed.set_author(name="Jizo Back End")

        embed.add_embed_field(name="User", value=user, inline=False)
        embed.add_embed_field(name="URL", value=url, inline=False)
        embed.add_embed_field(name="Message", value=message, inline=False)
        embed.add_embed_field(name="Payload", value=repr(payload), inline=False)
        embed.add_embed_field(name="Data", value=repr(data), inline=False)

        embed.set_footer(text="Petit message de Jizo: Axel c'est le meilleur Chef de Projet ❤️", icon_url=ICON)

        embed.set_thumbnail(url=ICON)
        disc_webhook.add_embed(embed)
        disc_webhook.execute(remove_embeds=True)
