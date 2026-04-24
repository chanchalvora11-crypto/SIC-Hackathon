# test_notifier.py

from services.notifier import Notifier

notifier = Notifier()

# Test cases
notifier.notify("BLR-DEL", 6000, 5000)  # drop
notifier.notify("BLR-DEL", 5000, 6500)  # increase
notifier.notify("BLR-DEL", 5000, 5000)  # same
notifier.notify("BLR-DEL", None, 5500)  # first time