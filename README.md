[![refresh-data](https://github.com/PatrickJnr/my-steam-library/actions/workflows/refresh_data.yaml/badge.svg?branch=main)](https://github.com/PatrickJnr/my-steam-library/actions/workflows/refresh_data.yaml) [![pages-build-deployment](https://github.com/PatrickJnr/my-steam-library/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/PatrickJnr/my-steam-library/actions/workflows/pages/pages-build-deployment)
 
 # my-steam-library

[dbeley.github.io/my-steam-library](https://dbeley.github.io/my-steam-library)

This is a simple website to display my Steam library. The data is updated weekly thanks to a Github action.

The data can also be downloaded in various format (csv, xlsx, pdf) directly from the deployed website.

See also [steam_stats](https://github.com/dbeley/steam_stats) which is the utility used to extract the data from Steam.

## Create your own

If you want to create your own, follow those instructions:

- Fork this repository (at the top of this page)
- Add the following secrets to your repository settings (`Repository settings` > `Secrets and variables` > `Actions` > `New repository secret`)
    - `STEAM_API_KEY` with your Steam API key (Create one [here](https://steamcommunity.com/dev/apikey))
    - `STEAM_USER_ID` with your Steam User ID (Find it in your [Steam account page](https://store.steampowered.com/account/))
- Allow the Github Action to write on your repository (`Repository settings` > `Actions` > `General` > `Workflow permissions` > `Read and write`)
- Manually run the `refresh-data` Github Action on your repository (Tab `Actions` at the top of the page)
- Use Github Pages to deploy the `docs` folder (`Repository settings` > `Pages` > `Deploy from a branch` > `Select main branch` > `docs folder` > `Save`)
- The website will soon be available at `https://YOUR_USERNAME.github.io/my-steam-library`
- The Github Action should automatically run every week (see `.github/worklows/refresh_data.yaml` for the exact schedule)

Depending on the size of your library the data refresh can take a long time (~40 minutes for a library with ~1600 games).
