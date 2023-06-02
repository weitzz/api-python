from core.config import setting
from core.database import engine


async def create_tables() -> None:
    import models.__all_models
    print('criando as tabelas no db')

    async with engine.begin() as conn:
        await conn.run_sync(setting.DBBaseModel.metadata.drop_all)
        await conn.run_sync(setting.DBBaseModel.metadata.create_all)
        print('tabelas criadas com sucesso')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())
