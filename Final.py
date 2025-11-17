import matplotlib.pyplot as plt  # type: ignore

class User:
    """
    Saving Money Cat App
    Tracks daily, weekly, and monthly expenses against budgets.
    Provides cat moods, rewards, and visualizations.
    """

    def __init__(self, income, target_saving, days=30):
        # Core financial setup
        self.income = income
        self.target_saving = target_saving
        self.days = days

        # Budget calculations
        self.allowable_expenses = income - target_saving
        self.daily_budget = self.allowable_expenses / days
        self.weekly_budget = self.allowable_expenses / 4  # assume 4 weeks per month

        # Tracking variables
        self.balance = 0
        self.cat_state = "hungry"
        self.expenses_log = []       # list of dicts {day, category, amount}
        self.rewards = []            # unlocked rewards
        self.big_purchases = []      # record of large expenses

    # ---------------------------
    # Expense Logging
    # ---------------------------
    def log_expense(self, day, category, amount):
        """Log a daily expense by category."""
        self.expenses_log.append({"day": day, "category": category, "amount": amount})

    def log_big_purchase(self, day, item, amount):
        """Record a big purchase and recalculate budgets."""
        self.big_purchases.append({"day": day, "item": item, "amount": amount})
        self.allowable_expenses -= amount

        remaining_days = self.days - day
        if remaining_days > 0:
            self.daily_budget = self.allowable_expenses / remaining_days
            self.weekly_budget = self.allowable_expenses / 4

        print(f"\n⚡ Big Purchase: {item} for ${amount} on Day {day}.")
        print(f"New daily budget: ${self.daily_budget:.2f}, New weekly budget: ${self.weekly_budget:.2f}")

    # ---------------------------
    # Daily & Weekly Summaries
    # ---------------------------
    def end_of_day(self, day):
        """Check daily spending vs budget and update cat mood."""
        total = sum(e["amount"] for e in self.expenses_log if e["day"] == day)

        if total <= self.daily_budget:
            saved_today = self.daily_budget - total
            self.balance += saved_today
            self.cat_state = "happy"
            print(f"Day {day}: Spent ${total}, under budget! Saved ${saved_today:.2f}. Cat is {self.cat_state}. 😺")
        else:
            self.cat_state = "neutral"
            print(f"Day {day}: Spent ${total}, over budget. No savings today. Cat is {self.cat_state}. 😐")

        if day % 7 == 0:
            self.weekly_summary(day)

    def weekly_summary(self, day):
        """Summarize weekly spending and unlock rewards if within budget."""
        start = day - 6
        week_expenses = sum(e["amount"] for e in self.expenses_log if start <= e["day"] <= day)

        print(f"\n--- Week {day//7} Summary ---")
        print(f"Total spent: ${week_expenses:.2f} vs Weekly budget: ${self.weekly_budget:.2f}")

        if week_expenses <= self.weekly_budget:
            reward = f"Week {day//7} Toy"
            self.rewards.append(reward)
            print(f"🎉 Weekly success! Cat unlocks {reward}.")
        else:
            print("⚠️ Overspent this week. Try to recover next week.")

    # ---------------------------
    # Monthly Summary & Charts
    # ---------------------------
    def monthly_summary(self):
        """Summarize monthly performance, show rewards, and visualize data."""
        print("\n--- Monthly Summary ---")
        print(f"Income: ${self.income}")
        print(f"Target Saving: ${self.target_saving}")
        print(f"Actual Saved: ${self.balance:.2f}")

        # Category totals
        categories = {}
        for e in self.expenses_log:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

        print("\nExpense Breakdown by Category:")
        for cat, amt in categories.items():
            print(f" - {cat}: ${amt:.2f}")

        # Big purchases
        if self.big_purchases:
            print("\nBig Purchases:")
            for bp in self.big_purchases:
                print(f" - Day {bp['day']}: {bp['item']} (${bp['amount']})")

        # Rewards
        if self.balance >= self.target_saving:
            reward = "Spa Mode"
            self.rewards.append(reward)
            self.cat_state = "spa"
            print(f"🎉 Monthly target achieved! Cat unlocks {reward}! 🛁🐱")
        else:
            self.cat_state = "neutral"
            print("Target not met. Cat stays cozy but neutral.")

        print("\nUnlocked Rewards:")
        for r in self.rewards:
            print(f" - {r}")

        # Visualizations
        self.plot_weekly_expenses()
        self.plot_expenses(categories)

    # ---------------------------
    # Visualization
    # ---------------------------
    def plot_weekly_expenses(self):
        """Bar chart: weekly spending vs budget."""
        weeks = (self.days // 7)
        weekly_totals = []
        for w in range(weeks):
            start = w*7 + 1
            end = start + 6
            total = sum(e["amount"] for e in self.expenses_log if start <= e["day"] <= end)
            weekly_totals.append(total)

        plt.figure(figsize=(8,4))
        plt.bar(range(1, weeks+1), weekly_totals, color="skyblue", label="Weekly Spending")
        plt.axhline(y=self.weekly_budget, color="red", linestyle="--", label="Weekly Budget")
        plt.title("Weekly Spending vs Budget")
        plt.xlabel("Week")
        plt.ylabel("Amount Spent ($)")
        plt.legend()
        plt.show()

    def plot_expenses(self, categories):
        """Pie chart: expense breakdown by category."""
        plt.figure(figsize=(6,6))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expense Breakdown by Category")
        plt.show()


# ---------------------------
# Helper Functions
# ---------------------------
def safe_float_input(prompt, default=None):
    """Safely get a float input from user."""
    while True:
        try:
            value = input(prompt)
            if value == "" and default is not None:
                return default
            return float(value)
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def safe_int_input(prompt, default=None):
    """Safely get an integer input from user."""
    while True:
        try:
            value = input(prompt)
            if value == "" and default is not None:
                return default
            return int(value)
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")


# ---------------------------
# Menu System
# ---------------------------
def main_menu(user, categories):
    while True:
        print("\n--- Saving Money Cat Menu ---")
        print("1. Log daily expenses")
        print("2. View weekly summary")
        print("3. View monthly summary")
        print("4. Record big purchase")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            day = safe_int_input("Enter day number: ")
            for cat in categories:
                amount = safe_float_input(f"  {cat}: ")
                user.log_expense(day, cat, amount)
            user.end_of_day(day)

        elif choice == "2":
            day = safe_int_input("Enter last day of week: ")
            user.weekly_summary(day)

        elif choice == "3":
            user.monthly_summary()

        elif choice == "4":
            day = safe_int_input("Enter day number: ")
            item = input("Item name: ")
            amount = safe_float_input("Cost: ")
            user.log_big_purchase(day, item, amount)

        elif choice == "5":
            print("Goodbye! Cat waves 🐱👋")
            break

        else:
            print("❌ Invalid choice. Try again.")


# ---------------------------
# Program Start
# ---------------------------
income = safe_float_input("Enter your monthly income: ")
target = safe_float_input("Enter your monthly saving target: ")
days = safe_int_input("How many days in this month? (default 30): ", default=30)

user = User(income, target, days)
categories = ["Food", "Transport", "Entertainment", "Shopping", "Misc"]

main_menu(user, categories)

