from supabase import create_client, Client

import os

class Supabase:
    def __init__(self) -> None:
        self.client: Client = create_client(
            os.getenv('SUPABASE_ENDPOINT'),
            os.getenv('SUPABASE_KEY')
        )

    async def get_all(self, table: str) -> list[dict]:                                     return self.client.table(table).select('*').execute().data
    async def get_by_id(self, table: str, id: int) -> list[dict]:                          return self.client.table(table).select('*').eq('id', id).execute().data
    async def get_by_key(self, table: str, key: str, val: any) -> list[dict]:              return self.client.table(table).select('*').eq(key, val).execute().data
    async def update_by_id(self, table: str, id: int, data: dict[str, any]) -> list[dict]: return self.client.table(table).update(data).eq('id', id).execute()
    async def push(self, table: str, data: dict[str, any]) -> dict[str, any]: 
        if len(await self.get_by_id(table, data.get('id'))) != 0: return

        return self.client.table(table).insert(data).execute().data[0]

supabase: Supabase = Supabase()