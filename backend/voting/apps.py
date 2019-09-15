from django.apps import AppConfig


class VotingConfig(AppConfig):
    name = "voting"

    def ready(self):
        import api.voting.converter  # noqa
