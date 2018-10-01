from django import dispatch

fake_bot_hit = dispatch.Signal(providing_args=["bot_ip", "bot_useragent", "fqdn_expected", "fqdn_received"])
