"""Example usage of the LoL API."""
import argparse
import json
import urllib.request
import urllib.error


SUMMONER_PATH = "/lol/summoner/v4/summoners/by-name/{summonerName}"
MATCH_HISTORY_PATH = "/lol/match/v4/matchlists/by-account/{encryptedAccountId}"
MATCH_RESPONSE = "/lol/match/v4/matches/{matchId}"


def _riot_api(host_url, api_key):
    """Return a function that calls Riot API."""
    def _request(path):
        """Make a request to API path."""
        url = urllib.parse.urlunparse(("https", host_url, path, "", "", ""))

        request = urllib.request.Request(url, headers={"X-Riot-Token": api_key})  # noqa
        response = urllib.request.urlopen(request)
        return json.load(response)

    return _request


def main(host_url, api_key, summoner_name):
    """Run the queries."""
    # Retrieve summoner information
    riot_api = _riot_api(host_url, api_key)

    summoner_response = riot_api(
        SUMMONER_PATH.format(summonerName=summoner_name)
    )
    print(json.dumps(summoner_response, indent=2))

    history_response = riot_api(
        MATCH_HISTORY_PATH.format(encryptedAccountId=summoner_response["accountId"])  # noqa
    )
    print(json.dumps(history_response, indent=2))

    match_response = riot_api(
        MATCH_RESPONSE.format(matchId=history_response["matches"][0]["gameId"])
    )
    print(json.dumps(match_response, indent=2))


parser = argparse.ArgumentParser()
parser.add_argument("summoner_name")
parser.add_argument("--api_key", help="Riot games API key. "
                    "Retrieve from https://developer.riotgames.com/")
parser.add_argument("--host_url", default="na1.api.riotgames.com")


if __name__ == "__main__":
    args = parser.parse_args()
    main(**vars(args))
