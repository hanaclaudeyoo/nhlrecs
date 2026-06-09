import requests

BASE_URL = "https://www.nhl.com/scores/htmlreports"


def fetch_game(
    season: str,
    season_phase: str,
    game_id: str,
    session: requests.Session = None
) -> str | None:
    req_url = f"{BASE_URL}/{season}/PL{season_phase}{game_id}.HTM"
    if session is None:
        response = requests.get(req_url)
    else:
        response = session.get(req_url)

    if response.status_code == 404:
        print(f"No game available for {req_url}")
        return None
    if response.status_code != 200:
        raise RuntimeError(f"Unexpected response status {response.status_code} for {req_url}")
    
    return response.text
