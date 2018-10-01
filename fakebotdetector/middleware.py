import re
import socket
from ipaddress import ip_address

from django.conf import settings
from django.http import HttpResponse

from fakebotdetector.signals import fake_bot_hit


class FakeBotDetectorMiddleware:
    BOTS = (
        # Bot signature string, bot verification regex
        ('baiduspider', re.compile(r'.*crawl\.baidu\.(com|jp)$')),
        ('googlebot', re.compile(r'.*(google|googlebot)\.com$')),
        ('bingbot', re.compile(r'.*search\.msn\.com$')),
        ('slurp', re.compile(r'.*crawl\.yahoo\.net$')),
        ('yandexbot', re.compile(r'.*yandex\.(ru|com|net)$')),
    )
    FAKE_BOT_DETECTOR_ENABLED = getattr(settings, 'FAKE_BOT_DETECTOR_ENABLED', True)
    FAKE_BOT_RESPONSE_CODE = getattr(settings, 'FAKE_BOT_RESPONSE_CODE', 403)
    FAKE_BOT_BLOCK_ON_FAILED_LOOKUP = getattr(settings, 'FAKE_BOT_BLOCK_ON_FAILED_LOOKUP', True)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.FAKE_BOT_DETECTOR_ENABLED:
            user_agent = request.META.get('HTTP_USER_AGENT')
            matched_sigs = [sig for sig in self.BOTS if sig[0].lower() in user_agent.lower()]

            # ignore the result unless precisely one signature matches
            if len(matched_sigs) == 1:
                bot_sig_string, bot_verification_regex = matched_sigs[0]

                # get the request IP
                client_ip = request.META.get('REMOTE_ADDR')
                if not client_ip:
                    raise RuntimeError("django-killbot cannot check any client IP addresses because "
                                       "request.META['REMOTE_ADDR'] is missing, your webserver may be misconfigured.")

                if not self.ipaddress_is_private(client_ip):
                    # run a reverse DNS lookup on the request IP
                    try:
                        bot_reverse_lookup = self.reverse_lookup(client_ip)
                    except socket.herror as e:
                        if e.errno == 1:  # "unknown host" i.e. no DNS record for this IP
                            return HttpResponse(status=self.FAKE_BOT_RESPONSE_CODE)
                    else:
                        # check if the reverse lookup result matches the expected search bot domain
                        is_fake_bot = bot_verification_regex.match(bot_reverse_lookup) is None

                        if is_fake_bot:
                            fake_bot_hit.send(sender=self.__class__, bot_ip=client_ip, bot_useragent=user_agent,
                                              fqdn_expected=bot_verification_regex, fqdn_received=bot_reverse_lookup)
                            return HttpResponse(status=self.FAKE_BOT_RESPONSE_CODE)

        return self.get_response(request)

    @staticmethod
    def reverse_lookup(ip):
        fqdn, _, _ = socket.gethostbyaddr(ip)
        return fqdn

    @staticmethod
    def ipaddress_is_private(ip):
        return ip_address(ip).is_private
