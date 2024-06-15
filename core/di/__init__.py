from pythondi import Provider, configure

from app.user.repository.user import UserPostgresRepo, UserRepository


def init_di():
    provider = Provider()
    provider.bind(UserRepository, UserPostgresRepo)
    configure(provider=provider)
