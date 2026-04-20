from datetime import date, datetime

def make_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

def task_reward(priority):
    if priority == "High":
        return "8"
    if priority == "Medium":
        return "5"
    return "2"

def refresh_level(data):
    data["level"] = max(1, (int(data["coins"] // 50) + 1))

def spent_total(data):
    return sum(float(item.get("amount", 0)) for item in data["expenses"])

def pending_tasks(data):
    return [task for task in data["tasks"] if not task.get("done")]

def urgency_score(task):
    priority_map = {"Low": 1, "Medium": 2, "High": 3}
    score = priority_map.get(task.get("priority", "Low"), 1)
    deadline = task.get("deadline", " ")

    if not deadline:
        return score 
    
    try:
        target = datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return score
    
    days = (target - datetime.now()).days

    if days < 0:
        return 100 + score
    if days == 0:
        return 90 + score
    if days == 1:           
        return 70 + score
    
    return max(1, 20 - days) + score


def today_plan(data):
    plan = []
    tasks = pending_tasks(data)
    tasks.sort(key=urgency_score, reverse=True)
    
    if tasks:
        plan.append(f"**Tops Quest today: {tasks[0]['title']}**")
    else:
        plan.append("No pending quests! Enjoy your day! or add some quests to your schedule.")

    budget = float(data.get("daily_budget", 0))
    spent = spent_total(data)
    left = budget - spent

    if budget > 0 and left <= budget * 0.25:
        plan.append("**You are Broke!** Consider cutting down on expenses or finding ways to earn more coins.")
    else:
        plan.append("Your budget still looks good. Keep managing your coins wisely!")

    mood = data.get("mood", "Okay")
    if mood == "Focused":
        plan.append("Your mood is great for tackling quests! Stay in the zone and make the most of it.")
    elif mood in ["Stressed", "Tired"]:
        plan.append("Your mood suggests you might need a break. Consider taking short rests between quests to recharge.")
    else:
        plan.append("keep steady and positive! Your mood is good for handling your quests.")
    
    if str(data.get("tomorrow_needs", "")).strip():
        plan.append(f"Don't forget to check your quests: {data['tomorrow_needs'].strip()}")
