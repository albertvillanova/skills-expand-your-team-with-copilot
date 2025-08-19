"""
Database configuration and setup for Mergington High School API
"""

from argon2 import PasswordHasher

# In-memory database for development (fallback when MongoDB is not available)
class InMemoryCollection:
    def __init__(self):
        self.data = {}
    
    def find_one(self, query=None):
        if query is None:
            query = {}
        
        if '_id' in query:
            return self.data.get(query['_id'])
        
        # Simple search implementation
        for key, value in self.data.items():
            if all(value.get(k) == v for k, v in query.items() if k != '_id'):
                return value
        return None
    
    def find(self, query=None):
        if query is None:
            query = {}
        
        results = []
        for key, value in self.data.items():
            match = True
            for q_key, q_val in query.items():
                if q_key == '_id':
                    if key != q_val:
                        match = False
                        break
                elif isinstance(q_val, dict):
                    # Handle simple MongoDB-style queries like {'$in': [...]}
                    if '$in' in q_val:
                        if not (value.get(q_key.replace('.', '_')) in q_val['$in'] if '.' not in q_key else 
                               any(day in q_val['$in'] for day in value.get('schedule_details', {}).get('days', []))):
                            match = False
                            break
                    elif '$gte' in q_val:
                        val = value.get('schedule_details', {}).get(q_key.split('.')[-1]) if '.' in q_key else value.get(q_key)
                        if not (val and val >= q_val['$gte']):
                            match = False
                            break
                    elif '$lte' in q_val:
                        val = value.get('schedule_details', {}).get(q_key.split('.')[-1]) if '.' in q_key else value.get(q_key)
                        if not (val and val <= q_val['$lte']):
                            match = False
                            break
                else:
                    if value.get(q_key) != q_val:
                        match = False
                        break
            
            if match:
                results.append({**value, '_id': key})
        
        return results
    
    def insert_one(self, document):
        doc_id = document.get('_id')
        if doc_id:
            doc = document.copy()
            doc.pop('_id')
            self.data[doc_id] = doc
    
    def update_one(self, query, update):
        if '_id' in query:
            doc_id = query['_id']
            if doc_id in self.data:
                if '$set' in update:
                    self.data[doc_id].update(update['$set'])
                elif '$push' in update:
                    for field, value in update['$push'].items():
                        if field not in self.data[doc_id]:
                            self.data[doc_id][field] = []
                        self.data[doc_id][field].append(value)
                elif '$pull' in update:
                    for field, value in update['$pull'].items():
                        if field in self.data[doc_id] and isinstance(self.data[doc_id][field], list):
                            self.data[doc_id][field] = [x for x in self.data[doc_id][field] if x != value]
    
    def count_documents(self, query=None):
        return len(self.find(query or {}))
    
    def aggregate(self, pipeline):
        # Simple aggregation for getting unique days
        if len(pipeline) >= 2 and pipeline[0].get('$unwind') == '$schedule_details.days':
            days = set()
            for value in self.data.values():
                if 'schedule_details' in value and 'days' in value['schedule_details']:
                    for day in value['schedule_details']['days']:
                        days.add(day)
            return [{'_id': day} for day in sorted(days)]
        return []

# Use in-memory collections
activities_collection = InMemoryCollection()
teachers_collection = InMemoryCollection()

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

