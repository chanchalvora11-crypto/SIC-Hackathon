import sys
import os

sys.path.append(os.path.abspath("src"))
from services.storage import update_price, get_last_price, get_price_history
update_price("BLR-DEL", 6000)
update_price("BLR-DEL", 5800)

print(get_last_price("BLR-DEL"))
print(get_price_history("BLR-DEL"))