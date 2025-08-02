source /home/app/.venv/bin/activate

echo "Fixing permissions"
chown -R app:app /tmp

exec su-exec app "$@"
