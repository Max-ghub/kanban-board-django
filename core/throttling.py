import time

from rest_framework.permissions import SAFE_METHODS
from rest_framework.throttling import SimpleRateThrottle


class ExtendedSimpleRateThrottle(SimpleRateThrottle):
    _extended_units = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
    }

    def parse_rate(self, rate):
        if rate is None:
            return None

        try:
            num, period = rate.split("/")
        except ValueError:
            return super().parse_rate(rate)

        if period and period[-1] in self._extended_units and period[:-1].isdigit():
            return int(num), int(period[:-1]) * self._extended_units[period[-1]]
        return super().parse_rate(rate)


class SlowdownThrottleMixin:
    slowdown_delay = 1.5
    slowdown_threshold = 5

    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        if (
            allowed
            and self.num_requests is not None
            and self.slowdown_delay > 0
            and self.slowdown_threshold >= 0
        ):
            history = getattr(self, "history", None)
            if history is not None:
                remaining = self.num_requests - len(history)
                if remaining <= self.slowdown_threshold:
                    time.sleep(self.slowdown_delay)
        return allowed


class SlowUserRateThrottle(SlowdownThrottleMixin, ExtendedSimpleRateThrottle):
    scope = "user"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        ident = request.user.pk
        return self.cache_format % {"scope": self.scope, "ident": ident}


class SlowAnonRateThrottle(SlowdownThrottleMixin, ExtendedSimpleRateThrottle):
    scope = "anon"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class WriteOnlyThrottle(SimpleRateThrottle):
    def allow_request(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class AuthThrottle(
    WriteOnlyThrottle, SlowdownThrottleMixin, ExtendedSimpleRateThrottle
):
    scope = "auth"


class RegisterThrottle(
    WriteOnlyThrottle, SlowdownThrottleMixin, ExtendedSimpleRateThrottle
):
    scope = "register"
