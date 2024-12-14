import json

import aiohttp
from datetime import datetime, timezone
WEB_ID = "8b9b4dbf-1ff8-4ad2-8520-07a1ac7c0f8a"
from dataclasses import dataclass


@dataclass
class AggregatedWorkoutMetrics:
    numWorkouts: int
    weightLifted: int
    caloriesBurned: int
    activeMinutes: int
def format_datetime_as_iso8601(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


class Tempo:
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.session = session
        self.access_token = None
        self.access_token_expiry =None
        self.refresh_token = None
        self.refresh_expiry = None
        self.last_refresh = None

    async def login(self):
        test = await self.session.post(url="https://api.trainwithpivot.com/oauth/token", data={
            "client_id": WEB_ID,
            "grant_type": "password",
            "password": self.password,
            "username": self.username})
        resp = await test.json()
        self.access_token = "Bearer " + resp["access_token"]
        self.access_token_expiry = resp["expires_in"]
        self.refresh_token = resp["refresh_token"]
        self.refresh_expiry = resp["refresh_expires_in"]
        self.last_refresh = datetime.now()

    async def me(self):
        # Dict of exercise name to current weight
        resp = await self.session.get("https://api.trainwithpivot.com/v1/me", headers={"authorization": self.access_token})
        r = await resp.json()
        data = {}
        for exercise in r['data']["performance"]["exercises"].values():
            data[exercise["exercise_name"]] = exercise["progress"][-1]["weight"]["value"]
        return data

    async def refresh(self):
        if (datetime.now() - self.last_refresh).total_seconds() > self.access_token_expiry / 2:
            resp = await self.session.post("https://api.trainwithpivot.com/oauth/token", data={
                "client_id": WEB_ID,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            })
            r = await resp.json()
            self.access_token = "Bearer " + r["access_token"]
            self.access_token_expiry = r["expires_in"]
            self.refresh_token = r["refresh_token"]
            self.refresh_expiry = r["refresh_expires_in"]
            self.last_refresh = datetime.now()

    async def get_stats(self, start:datetime,end: datetime):

        graphql_data = {
            "operationName": "getAggregatedWorkoutMetrics",
            "query": """
            query getAggregatedWorkoutMetrics($options: AggregatedWorkoutMetricsInput) {
                currentUser {
                    __typename
                    aggregatedWorkoutMetrics(options: $options) {
                        __typename
                        numWorkouts
                        weightLifted
                        caloriesBurned
                        activeMinutes
                    }
                }
            }
            """,
            "variables": {
                "options": {
                    "startDate": format_datetime_as_iso8601(start),
                    "endDate": format_datetime_as_iso8601(end),
                }
            }
        }

        resp = await self.session.post("https://api.trainwithpivot.com/v1/graphql", headers={"authorization": self.access_token},json=graphql_data)
        j = await resp.json()
        data = j["data"]["currentUser"]["aggregatedWorkoutMetrics"]
        return AggregatedWorkoutMetrics(numWorkouts=data["numWorkouts"], weightLifted=data["weightLifted"], activeMinutes=data["activeMinutes"], caloriesBurned=data["caloriesBurned"])
