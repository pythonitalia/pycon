#!/usr/bin/env bash
# Copies the local backend DB from the old PG14 volume into the PG18 backend-db service.
# Usage: scripts/migrate-local-db-to-pg18.sh [-y]
set -euo pipefail

cd "$(dirname "$0")/.."

ASSUME_YES=false
[[ "${1:-}" == "-y" ]] && ASSUME_YES=true

PROJECT=$(docker compose config | sed -n 's/^name: //p' | head -n1)
OLD_VOL=${OLD_VOL:-${PROJECT}_pycon-backend-db-data}
DUMP_FILE=${DUMP_FILE:-/tmp/pycon-pg14.dump}
OLD_CONTAINER=pycon-pg14-old

if ! docker volume inspect "$OLD_VOL" >/dev/null 2>&1; then
  echo "Volume '$OLD_VOL' not found. Set OLD_VOL to the right name (docker volume ls | grep backend-db)." >&2
  exit 1
fi

echo "Old PG14 volume: $OLD_VOL"
echo "Dump file:       $DUMP_FILE"
echo "This replaces the 'pycon' database in the PG18 backend-db service."
if ! $ASSUME_YES; then
  read -r -p "Continue? [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]] || exit 1
fi

cleanup() { docker rm -f "$OLD_CONTAINER" >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "==> Stopping services that use the DB"
docker compose stop backend resonate-worker
docker compose up -d --wait backend-db

echo "==> Starting temporary PG14 on $OLD_VOL"
cleanup
docker run -d --name "$OLD_CONTAINER" -v "$OLD_VOL":/var/lib/postgresql/data postgres:14.5 >/dev/null
until docker exec "$OLD_CONTAINER" pg_isready -U pycon -q; do sleep 1; done

echo "==> Dumping PG14 database to $DUMP_FILE"
# PG18's pg_dump is used against the PG14 server, as recommended for major upgrades.
docker run --rm --network "container:$OLD_CONTAINER" -e PGPASSWORD=pycon postgres:18.6 \
  pg_dump -h 127.0.0.1 -U pycon -Fc pycon >"$DUMP_FILE"

echo "==> Restoring into PG18"
docker compose exec -T backend-db dropdb -U pycon --if-exists --force pycon
docker compose exec -T backend-db createdb -U pycon pycon
docker compose exec -T backend-db pg_restore -U pycon -d pycon --no-owner --no-privileges <"$DUMP_FILE"
docker compose exec -T backend-db vacuumdb -U pycon --analyze-only --quiet pycon

COUNT_SQL="select count(*) from django_migrations"
old_count=$(docker exec "$OLD_CONTAINER" psql -U pycon -d pycon -Atc "$COUNT_SQL")
new_count=$(docker compose exec -T backend-db psql -U pycon -d pycon -Atc "$COUNT_SQL")
echo "==> django_migrations rows: PG14=$old_count PG18=$new_count"
if [[ "$old_count" != "$new_count" ]]; then
  echo "Row counts differ, check the restore before using the DB." >&2
  exit 1
fi

echo "==> Starting services"
docker compose up -d

echo "Done. Once everything works you can delete the old volume: docker volume rm $OLD_VOL"
