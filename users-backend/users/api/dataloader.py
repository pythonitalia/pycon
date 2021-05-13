from strawberry.dataloader import DataLoader

from users.db import get_engine, get_session
from users.domain.entities import User
from users.domain.repository import UsersRepository


async def load_users(ids: list[int]) -> list[User]:
    try:
        engine = get_engine()
        async with get_session(engine) as session:
            users = await UsersRepository(session).get_batch_by_ids(ids)
            users_by_id = {user.id: user for user in users}
            return [users_by_id.get(id) for id in ids]
    finally:
        await engine.dispose()


users_dataloader = DataLoader(load_fn=load_users)
