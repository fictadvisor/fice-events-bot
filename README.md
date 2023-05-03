<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">FICE Events Bot</h3>

  <p align="center">
    <a href="https://github.com/fictadvisor/fice-events-bot">View Demo</a>
    ·
    <a href="https://github.com/fictadvisor/fice-events-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/fictadvisor/fice-events-bot/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* poetry
  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/fictadvisor/fice-events-bot
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
   _or poetry_
   ```sh
   poetry install
   ```
3. Rename `.env.dist` to `.env`, and enter your environment variables
   ```js
   TOKEN="BOT TOKEN"

   POSTGRES_HOST="POSTGRES_HOST"
   POSTGRES_USER="POSTGRES_USER"
   POSTGRES_PASSWORD="POSTGRES_PASSWORD"
   POSTGRES_DB="POSTGRES_DB"
   
   REDIS_HOST="REDIS_HOST"
   REDIS_PORT=PORT
   REDIS_USERNAME="REDIS_USERNAME"
   REDIS_PASSWORD="REDIS_PASSWORD"
   REDIS_DB=REDIS_DB
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
### Console
   ```sh
   python -m bot.main
   ```
### Docker
   Build
   ```sh
   docker build -t fice-events-bot .
   ```
   Run
   ```sh
   docker run fice-events-bot
   ```
### Docker-Compose
   ```sh
   docker-compose up
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/fictadvisor/fice-events-bot.svg?style=for-the-badge
[contributors-url]: https://github.com/fictadvisor/fice-events-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/fictadvisor/fice-events-bot.svg?style=for-the-badge
[forks-url]: https://github.com/fictadvisor/fice-events-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/fictadvisor/fice-events-bot.svg?style=for-the-badge
[stars-url]: https://github.com/fictadvisor/fice-events-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/fictadvisor/fice-events-bot.svg?style=for-the-badge
[issues-url]: https://github.com/fictadvisor/fice-events-bot/issues
[license-shield]: https://img.shields.io/github/license/fictadvisor/fice-events-bot.svg?style=for-the-badge
[license-url]: https://github.com/fictadvisor/fice-events-bot/blob/master/LICENSE.txt