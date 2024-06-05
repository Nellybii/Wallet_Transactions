from django.apps import AppConfig


class LoadingWalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Loading_Wallet'

    def ready(self):
        from .views.load_wallet_views import register_urls
        register_urls()
