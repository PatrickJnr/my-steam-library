from datetime import datetime
from html import escape
from string import Template

import pandas as pd


def read_template(file: str) -> Template:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return Template(content)


def format_hours(minutes: float, unit: str = "h", decimals: int = 1) -> str:
    """Format a minute count as hours, e.g. 480 -> '8.0 h'."""
    if not minutes:
        return "0 " + unit
    hours = minutes / 60
    if decimals == 0:
        return f"{round(hours):,} {unit}"
    return f"{round(hours, decimals):,.{decimals}f} {unit}"


def release_year(value) -> str:
    if isinstance(value, str) and len(value) >= 4 and value[-4:].isdigit():
        return value[-4:]
    return ""


def format_reviews(percentage: int) -> str:
    return "&mdash;" if percentage < 0 else f"{percentage}%"


def achievements_percentage(achieved, total) -> int:
    if pd.isna(achieved) or pd.isna(total) or not total:
        return -1
    return int(round(float(achieved) / float(total) * 100))


def render_card(row) -> str:
    name = str(row["name"]).strip()
    appid = int(row["appid"])
    url = row["url"]
    if pd.isna(url) or not str(url).startswith("http"):
        url = f"https://store.steampowered.com/app/{appid}/"
    url = escape(str(url), quote=True)
    year = release_year(row["release_date"])
    developers = "" if pd.isna(row["developers"]) else str(row["developers"])

    playtime = 0 if pd.isna(row["playtime"]) else float(row["playtime"])
    recent = 0 if pd.isna(row["playtime_2weeks"]) else float(row["playtime_2weeks"])
    reviews = 0 if pd.isna(row["total_reviews"]) else int(row["total_reviews"])
    positive = row["percentage_positive_reviews"]
    positive = -1 if pd.isna(positive) else int(round(float(positive) * 100))

    achievements = achievements_percentage(
        row["achieved_achievements"], row["total_achievements"]
    )

    meta = " &middot; ".join(
        escape(part) for part in (year, developers) if part
    )
    image_url = (
        f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
    )

    return (
        f'      <article class="game" data-name="{escape(name.lower())}"'
        f' data-devs="{escape(developers.lower())}"'
        f' data-year="{year}"'
        f' data-playtime="{int(playtime)}"'
        f' data-recent="{int(recent)}"'
        f' data-positive="{positive}"'
        f' data-reviews="{reviews}"'
        f' data-achievements="{achievements}">\n'
        f'        <a class="cover" href="{url}" tabindex="-1" aria-hidden="true">'
        f'<img src="{image_url}" alt="" width="460" height="215" loading="lazy">'
        "</a>\n"
        '        <div class="body">\n'
        f'          <h2><a href="{url}">{escape(name)}</a></h2>\n'
        f'          <p class="meta">{meta}</p>\n'
        '          <ul class="stats">\n'
        f'            <li><span>Playtime</span><strong>{format_hours(playtime)}</strong></li>\n'
        f'            <li><span>Reviews</span><strong>{format_reviews(positive)}</strong></li>\n'
        f'            <li><span>Achievements</span><strong>{format_reviews(achievements)}</strong></li>\n'
        "          </ul>\n"
        "        </div>\n"
        "      </article>"
    )


df_game_info = pd.read_csv("game_info.csv", sep="\t")
df_playtime = pd.read_csv("playtime.csv", sep="\t")
df = pd.merge(df_game_info, df_playtime, how="left", on=["appid"])

df = df.fillna({"release_date": ""})
df = df.sort_values("playtime", ascending=False)

df["percentage_positive_reviews"] = df["total_positive"].div(df["total_reviews"])
df.loc[df["percentage_positive_reviews"] == float("inf"), "percentage_positive_reviews"] = (
    float("nan")
)

total_playtime = df["playtime"].sum()
if total_playtime:
    quality_index = f"{round((df['percentage_positive_reviews'].fillna(0) * df['playtime']).sum() / total_playtime, 2):.2f}"
else:
    quality_index = "n/a"

cards = "\n".join(render_card(row) for _, row in df.iterrows())

formatted_message = read_template("template.html").safe_substitute(
    {
        "date_update": datetime.today().strftime("%Y-%m-%d"),
        "game_count": f"{len(df):,}",
        "cards": cards,
        "sum_playtime": format_hours(total_playtime, "hours", 0),
        "quality_index": quality_index,
        "sum_recent_playtime": format_hours(df["playtime_2weeks"].sum(), "hours", 0),
    }
)

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(formatted_message)

print(f"Wrote docs/index.html with {len(df)} games")
