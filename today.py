import os
import requests

TOKEN = os.getenv("METRICS_TOKEN")
USERNAME = "marcosmacedo-cs"

query = """
query($username: String!) {
  user(login: $username) {
    repositories(ownerAffiliations: OWNER, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
    }
  }
}
"""

def fetch_stats():
    if not TOKEN:
        print("⚠️ METRICS_TOKEN não encontrado! Usando valores zerados para testes locais.")
        return {"repos": 0, "stars": 0, "followers": 0, "commits": 0}
    
    headers = {"Authorization": f"bearer {TOKEN}"}
    res = requests.post(
        "https://api.github.com/graphql", 
        json={'query': query, 'variables': {'username': USERNAME}}, 
        headers=headers
    )
    
    if res.status_code == 200:
        data = res.json()["data"]["user"]
        repos = data["repositories"]["totalCount"]
        stars = sum(r["stargazerCount"] for r in data["repositories"]["nodes"])
        followers = data["followers"]["totalCount"]
        commits = data["contributionsCollection"]["totalCommitContributions"] + data["contributionsCollection"]["restrictedContributionsCount"]
        return {"repos": repos, "stars": stars, "followers": followers, "commits": commits}
    
    return {"repos": 0, "stars": 0, "followers": 0, "commits": 0}

stats = fetch_stats()

def generate_svg(theme_bg, theme_fg):
    return f"""<svg fill="none" width="1080" height="580" viewBox="0 0 1080 580" xmlns="http://www.w3.org/2000/svg">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <style>
        .container {{
          background-color: {theme_bg};
          color: {theme_fg};
          font-family: monospace;
          font-size: 11.5px;
          white-space: pre;
          padding: 20px;
          display: flex;
          gap: 15px;
          border-radius: 8px;
          box-sizing: border-box;
          width: 100%;
          height: 100%;
        }}
        .header {{ color: #B3252C; font-weight: bold; }}
        .text-green {{ color: #2ea043; font-weight: bold; }} 
        .dots-wine {{ color: #B3252C; }}                   
        .val-white {{ color: {theme_fg}; }}                    
        .art {{ color: #2ea043; line-height: 1.1; }}
      </style>
      <div class="container">
        <div class="art">
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣲⣶⠒⠷⠶⠤⠴⠦⠤⠤⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣶⠚⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⢌⣛⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢚⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⡄⠙⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣀⠀⣀⣤⣧⠔⠛⠓⠲⠤⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣄⣠⣤⣴⣾⣿⣿⣾⡗⠀⢀⣀⢤⠐⠠⠤⣉⠓⠦⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠒⠶⠶⢾⣿⡿⠛⢻⣻⠛⢻⣿⣿⠟⣋⣺⣿⠏⠀⠴⠿⠹⠋⠀⠀⠀⠀⠈⠀⠨⠳⣄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢐⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⠤⠄⠐⢾⣿⣝⠤⣀⢀⡠⣱⣿⣿⣿⣿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀
⠀⠀⠀⠀⠀⠀⢠⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⣛⣺⣿⣾⣛⣽⣿⡟⠁⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀
⠀⠀⠀⠀⠀⠐⡟⠀⠀⠀⠀⡠⠖⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⠀⡈⠉⢉⡽⠿⢛⡿⢛⠯⠭⣒⣚⣩⣭⣭⣤⡤⠭⠭⢭⣥⣀⣉⣑⣒⢵⡀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⣰⠃⠀⢀⡔⠋⠀⠀⠀⣠⡴⠋⠀⠀⠀⠀⣠⣤⡴⠋⠀⠀⠀⠀⠀⠾⢶⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠳⡀⠀⣸⠃
⠀⠀⠀⠀⢰⠟⢀⣴⠏⠀⡀⢀⣴⡿⠋⠀⠀⠀⢀⡴⠟⠋⠁⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣇⠔⠁⠀
⠀⠀⠀⠀⣞⣴⣿⠃⢠⣾⣴⣿⠋⠀⠀⠀⠀⠐⠋⠀⠀⠀⠀⠀⢐⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣧⣶⣿⣿⣿⠗⠁⠀⡠⠂⠀⢀⠀⠀⠀⠀⠂⢉⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⡟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⠼⢻⣿⣿⣿⣿⣿⣿⠁⢀⣴⠏⢀⣠⠞⠁⢀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⣿⣿⣿⣿⣿⣿⣧⣾⡿⣡⣾⣿⠃⣠⡾⠁⠀⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠂⠀⢻⣍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⣽⣿⣿⣿⣿⣿⣿⡟⠉⣰⣿⡿⣡⣾⣿⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢻⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⣿⣿⣿⣿⣿⣿⣿⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣱⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⢸⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠐⠛⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⣿⠏⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⡄⠀⣿⣿⡏⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣴⡿⢋⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠁⠀⡿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⢿⡿⠁⣿⠏⠘⢿⣿⣿⣿⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠿⠋⣿⡿⠋⣸⠟⠁⠀⣾⣿⣿⣿⣿⣿⠟⠁⠈⠀⠀⠹⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠉⠀⠀⠰⠿⣿⣿⠿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡏⠀⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        </div>
        <div>
<span class="header">- marcos@macedo -----------------------------</span>

<span class="text-green">Name</span><span class="dots-wine">:..........</span> <span class="text-green">Marcos Vinícius</span>
<span class="text-green">Education</span><span class="dots-wine">:.....</span> <span class="text-green">Computer Engineering</span>
<span class="text-green">Location</span><span class="dots-wine">:......</span> <span class="text-green">Minas Gerais, Brazil</span>

<span class="text-green">OS</span><span class="dots-wine">:............</span> <span class="text-green">Windows / Kali Linux</span>
<span class="text-green">Host</span><span class="dots-wine">:..........</span> <span class="text-green">Computer Engineering @ UNIFEI</span>
<span class="text-green">Focus</span><span class="dots-wine">:.........</span> <span class="text-green">Cybersecurity Research</span>
<span class="text-green">Member</span><span class="dots-wine">:........</span> <span class="text-green">HawkSec</span>

<span class="header">- GitHub Metrics --------------------------</span>

<span class="text-green">Repositories</span><span class="dots-wine">:..</span> <span class="text-green">{stats['repos']}</span>
<span class="text-green">Total<span class="dots-wine">.</span>Commits</span><span class="dots-wine">:.</span> <span class="text-green">{stats['commits']}</span>
<span class="text-green">Stars<span class="dots-wine">.</span>Earned</span><span class="dots-wine">:..</span> <span class="text-green">{stats['stars']}</span>
<span class="text-green">Followers</span><span class="dots-wine">:.....</span> <span class="text-green">{stats['followers']}</span>

<span class="text-green">Languages<span class="dots-wine">.</span>Programming</span><span class="dots-wine">:.</span> <span class="text-green">C, Python, Bash</span>
<span class="text-green">Languages<span class="dots-wine">.</span>Real</span><span class="dots-wine">:........</span> <span class="text-green">Portuguese, English, French</span>
<span class="text-green">Tools</span><span class="dots-wine">:.........</span> <span class="text-green">Burp Suite, Wireshark, Docker</span>

<span class="header">- Contact ----------------------------------</span>

<span class="text-green">Email</span><span class="dots-wine">:.........</span> <span class="text-green">marcosmacedo-cs@proton.me</span>
<span class="text-green">LinkedIn</span><span class="dots-wine">:......</span> <span class="text-green">in/marcmacedo/</span>
<span class="text-green">Discord</span><span class="dots-wine">:.......</span> <span class="text-green">maarcolasx</span>
        </div>
      </div>
    </div>
  </foreignObject>
</svg>"""

# Gera o Dark Mode
with open("dark_mode.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg("#161b22", "#c9d1d9"))

# Gera o Light Mode
with open("light_mode.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg("#ffffff", "#24292e"))

print("✅ dark_mode.svg e light_mode.svg gerados com sucesso!")