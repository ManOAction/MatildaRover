# Log Rotate Setup
sudo nano /etc/logrotate.d/matilda_tests

# Value
/home/ubuntu/MatildaRover/ros2_ws/logs/tests_package.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 ubuntu ubuntu
    sharedscripts
    postrotate
        systemctl restart matilda_tests.service > /dev/null 2>/dev/null || true
    endscript
}

## Test Using This
sudo logrotate -d /etc/logrotate.d/matilda_tests
