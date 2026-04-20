from celery import Celery

# הגדרת Celery: 
# ה-Broker הוא המקום שבו המשימות מחכות בתור (Redis)
# ה-Backend הוא המקום שבו התוצאות נשמרות אחרי שהמשימה הסתיימה
celery_app = Celery(
    "fault_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def fetch_faults_task(subassembly_id):
    # כאן אנחנו מדמים פעולה כבדה מול ה-Database
    import time
    from backend.data_provider import DataProvider
    
    dp = DataProvider(db_url="postgresql://postgres:frolog@127.0.0.1:5432/faultsolver_db")
    
    # סימולציה של פעולה שלוקחת זמן (כדי לראות את ניהול התורים בפועל)
    time.sleep(3) 
    
    return dp.get_faults('subassembly', subassembly_id)