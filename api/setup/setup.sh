python3 -m venv /home/richie/PasswordManagerAPI/.venv
/home/richie/PasswordManagerAPI/.venv/bin/python -m pip install -r /home/richie/PasswordManagerAPI/requirements.txt

sudo -u postgres psql -c "CREATE DATABASE password_manager;"

echo "[Unit]
Description=Password Manager API
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/richie/PasswordManagerAPI/
User=root
Group=root
ExecStart=/home/richie/PasswordManagerAPI/.venv/bin/python3.10 /home/richie/PasswordManagerAPI/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target" >> /lib/systemd/system/password-manager-api.service
systemctl start password-manager-api
systemctl enable password-manager-api
