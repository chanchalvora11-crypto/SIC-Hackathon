# services/notifier.py

class Notifier:
    """
    Notifier class handles all user alerts related to price changes.
    It detects price drops, increases, no change, and new tracking.
    """

    def notify(self, route, old_price, new_price):
        """
        Main method to decide which notification to trigger.
        """
        try:
            # Case 1: First time tracking (no previous price)
            if old_price is None:
                print("\n" + "="*40)
                print("🆕 NEW TRACKING STARTED")
                print("="*40)
                print(f"✈️ Route      : {route}")
                print(f"💰 Price      : ₹{new_price}")
                print("="*40 + "\n")
                return
            
            # Case 2: Price dropped
            if new_price < old_price:
                self.price_drop(route, old_price, new_price)
            
            # Case 3: Price increased
            elif new_price > old_price:
                self.price_increase(route, old_price, new_price)
            
            # Case 4: No change
            else:
                self.no_change(route, new_price)

        except Exception as e:
            # Safety: prevents crash during demo
            print("❌ Error in notification system:", e)

    # -------------------------------
    # Handles price drop scenario 📉
    # -------------------------------
    def price_drop(self, route, old_price, new_price):
        diff = old_price - new_price
        
        print('\a')  # 🔊 Beep sound for attention
        
        print("\n" + "="*40)
        print("🔥 PRICE DROP ALERT 🔥")
        print("="*40)
        print(f"✈️ Route      : {route}")
        print(f"💸 Old Price  : ₹{old_price}")
        print(f"💰 New Price  : ₹{new_price}")
        print(f"🎉 You Save   : ₹{diff}")
        print("👉 Best time to book!")
        print("="*40 + "\n")

    # -------------------------------
    # Handles price increase scenario 📈
    # -------------------------------
    def price_increase(self, route, old_price, new_price):
        diff = new_price - old_price
        
        print("\n" + "="*40)
        print("⚠️ PRICE INCREASED")
        print("="*40)
        print(f"✈️ Route      : {route}")
        print(f"💸 Old Price  : ₹{old_price}")
        print(f"💰 New Price  : ₹{new_price}")
        print(f"📈 Increased  : ₹{diff}")
        print("="*40 + "\n")

    # -------------------------------
    # Handles no price change scenario ℹ️
    # -------------------------------
    def no_change(self, route, price):
        print("\n" + "="*40)
        print("ℹ️ NO PRICE CHANGE")
        print("="*40)
        print(f"✈️ Route      : {route}")
        print(f"💰 Price      : ₹{price}")
        print("="*40 + "\n")