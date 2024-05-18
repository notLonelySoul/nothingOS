import psutil

batter = psutil.sensors_battery()

print({"percent": batter.percent, "status": batter.power_plugged})
