# Deploying DailyQuest to Render (Recommended)

This guide walks through deploying your Flask app to Render and provisioning a managed PostgreSQL instance. It uses the existing `render.yaml` in the repo.

## Steps

1. Prepare repository

- Ensure your `rida` branch contains the changes you want to deploy (language selector etc.).

2. Push branch to GitHub (if not already)

```bash
cd "C:/Users/rida/Desktop/Final progect/FINAL_PROJECT"
# push local branch to remote
git push origin rida
```

3. Create a new Web Service on Render

- Go to https://render.com and sign in (or create account).
- Click "New" → "Web Service" → "Connect a repository" and choose `Rid62/DailyQuest`.
- For Branch, choose `rida` (or `master` as needed).
- Render will read `render.yaml` automatically; confirm the service settings (Python, Gunicorn command).

4. Add environment variables

In the Render service settings > Environment > Environment Variables, add:

- `SECRET_KEY` (a secure random string)
- `OPENAI_API_KEY` (your OpenAI key)
- `DATABASE_URL` (Render will supply after provisioning DB)

5. Add a Managed PostgreSQL Database

- In Render dashboard, click "New" → "PostgreSQL" → provision a free tier (hobby) instance.
- After creation, copy the DATABASE_URL and add it to your Web Service environment variables (or use the linked DB option).

6. Migrate / Initialize DB

- If your app includes `init_db.py`, use Render's Shell or run locally with `DATABASE_URL` set to your new Postgres URL to initialize schema and seed data.

Example local init (locally using production DB):

```bash
# set DATABASE_URL in environment or .env
set DATABASE_URL=postgresql://user:pass@host:port/dbname   # Windows PowerShell: $env:DATABASE_URL = "..."
python init_db.py
```

7. Deploy

- Click "Deploy" in Render or push new commits to trigger automatic deploys.
- Check service logs on Render for startup errors.

8. Post-deploy checks

- Visit your Render URL and register a user.
- Verify that the language selector works and that the app connects to PostgreSQL.
- Verify environment variables and static file serving.

## Notes & Tips

- Use `render.yaml` for consistent infrastructure-as-code deployment.
- Keep sensitive keys out of the repo; use Render environment variables.
- If you use SQLite locally, switch to PostgreSQL for production (as in `DATABASE_URL`).
- For OpenAI usage, monitor the quota and add usage limits as needed.

---

ملخص عربي (مختصر)

- أنصح بنشر التطبيق على Render لسهولة الربط مع GitHub ودعم PostgreSQL المدار.
- ادفع فرع `rida` إلى GitHub، ثم أنشئ Web Service على Render واربطه بالمستودع.
- أضف `OPENAI_API_KEY` و`SECRET_KEY` و`DATABASE_URL` في متغيرات البيئة.
- قم بتشغيل `init_db.py` مع `DATABASE_URL` الخاص بقاعدة Render لتهيئة الجداول.

---

If you want, I can now:
- push the local `rida` branch to GitHub for you, or
- prepare a small README snippet to run `init_db.py` against Render Postgres, or
- open a Render-ready checklist in `DEPLOYMENT.md`.
