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
        