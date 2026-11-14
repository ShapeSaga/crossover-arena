# Crossover Arena — installation du robot (une seule fois, ≈ 30 min)

Même principe que Shape Saga. Tu ne donnes **aucune clé dans le chat** : tu les ranges toi-même aux endroits indiqués.

## 1. Créer le bot Telegram (≈ 3 min)
1. Dans Telegram, ouvre **@BotFather** → `/newbot` → nom : `Crossover Arena Robot` → pseudo : par ex. `crossover_arena_robot` (doit finir par `bot`).
2. Garde le **jeton** qu'il donne (ligne `123456:ABC…`).
3. Ouvre ton nouveau bot et appuie sur **Démarrer** (sinon il ne peut pas t'écrire).
4. Ton **identifiant** Telegram : le même que pour Shape Saga ; sinon ouvre **@userinfobot**, il l'affiche (`Id`).

## 2. Clé Buffer du 2e compte (≈ 2 min)
Connecte-toi au **2e compte Buffer** (celui de Crossover Arena) et crée une clé d'API comme pour Shape Saga.

## 3. Mettre le dépôt sur GitHub (≈ 5 min)
1. **GitHub Desktop** → File → **Add local repository** → `D:\ZONE IA\CLAUDE_DB\CrossoverArena\crossover-arena`.
2. Message `Crossover Arena : robot` → **Commit to main** → **Publish repository**.
3. **Décoche « Keep this code private »** : le dépôt doit être **public** (c'est lui qui héberge les vidéos pour Buffer ; il ne contient aucun secret).

## 4. Ranger les clés du robot sur GitHub (≈ 5 min)
Sur github.com, dépôt `crossover-arena` → **Settings → Secrets and variables → Actions → New repository secret** :

| Nom (exact) | Valeur |
|---|---|
| `TELEGRAM_BOT_TOKEN` | jeton de @BotFather (étape 1) |
| `TELEGRAM_CHAT_ID` | ton identifiant Telegram |
| `BUFFER_API_KEY` | clé du 2e compte Buffer |
| `CLOUDFLARE_API_TOKEN` | Cloudflare → My Profile → API Tokens → Create Token → modèle **Edit Cloudflare Workers** (même compte Cloudflare que Shape Saga) |

## 5. Clé du PC (≈ 3 min)
Le PC doit pouvoir déposer les vidéos dans le dépôt :
1. github.com → photo de profil → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Nom `PC Crossover Arena` · Expiration : 1 an · **Repository access : Only select repositories → crossover-arena**
   · **Permissions → Contents : Read and write** → Generate.
3. Ouvre `D:\ZONE IA\CLAUDE_DB\CrossoverArena\secrets_pc.env` avec le Bloc-notes et remplis les 4 lignes (jeton GitHub, dépôt, jeton du bot, identifiant). Enregistre.

## 6. Allumer et tester
1. github.com → **Actions** → **Installer le réceptionniste** → Run workflow. Tu reçois « ✅ Réceptionniste installé » sur Telegram.
2. **Actions → Tester les connexions** → Run workflow : `Telegram ✅`, `Buffer ✅ … tiktok, youtube, instagram`, `Hébergement GitHub ✅`.
3. Dis « c'est fait » à James : il fabrique une vidéo de **TEST** sur le PC et lance le cycle. Tu la reçois sur Telegram,
   tu appuies sur ✅ : Buffer crée **3 brouillons** (rien n'est publié). Tu les supprimes à la main dans Buffer.
4. Ensuite seulement, la vraie semaine est fabriquée.
